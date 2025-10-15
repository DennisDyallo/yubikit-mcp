#!/usr/bin/env python3
"""
YubiKey MCP Server - Hello World
A basic MCP server that lists connected YubiKeys.
"""

import subprocess
from typing import Any, Literal

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP server
mcp = FastMCP("yubikey-hello-world")

# Type aliases for response structures
ResponseStatus = Literal["success", "error", "no_devices"]


class SerialSchema(BaseModel):
    """Schema for eliciting user input."""
    serial_number: int = Field(
        description="The serial number of the YubiKey"
    )


# ============================================================================
# Helper Functions
# ============================================================================

def run_ykman_command(args: list[str]) -> subprocess.CompletedProcess:
    """Execute a ykman command and return the result.

    Args:
        args: Command arguments (e.g., ["list"], ["info"], ["--device", "123", "info"])

    Returns:
        CompletedProcess instance with stdout/stderr

    Raises:
        FileNotFoundError: If ykman is not installed
        subprocess.CalledProcessError: If command fails
    """
    cmd = ["ykman"] + args
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )


def build_response(
    status: ResponseStatus,
    message: str,
    **extra_fields: Any
) -> dict[str, Any]:
    """Build a standardized response dictionary.

    Args:
        status: Response status code
        message: Human-readable message
        **extra_fields: Additional fields to include in response

    Returns:
        Response dictionary with status, message, and any extra fields
    """
    return {
        "status": status,
        "message": message,
        **extra_fields
    }


async def prompt_for_serial(ctx: Context) -> int | None:
    """Prompt the user to provide a YubiKey serial number.

    Args:
        ctx: MCP context for eliciting user input

    Returns:
        Serial number if user provides one, None if cancelled
    """
    elicit_result = await ctx.elicit(
        message="Multiple YubiKeys detected. Please provide the serial number of the YubiKey you want to query.",
        schema=SerialSchema
    )
    if elicit_result.action == "accept" and elicit_result.data:
        return elicit_result.data.serial_number
    return None


def get_ykman_info(serial_number: int | None = None) -> str:
    """Call ykman info command and return output.

    Args:
        serial_number: Optional serial number to query specific device

    Returns:
        Raw info output from ykman

    Raises:
        FileNotFoundError: If ykman is not installed
        subprocess.CalledProcessError: If command fails
    """
    args = []
    if serial_number is not None:
        args.extend(["--device", str(serial_number)])
    args.append("info")

    result = run_ykman_command(args)
    return result.stdout.strip()


def handle_ykman_error(error_msg: str, serial_number: int | None = None) -> dict[str, Any]:
    """Parse ykman error and return appropriate response.

    Args:
        error_msg: Error message from ykman stderr
        serial_number: Optional serial number that was queried

    Returns:
        Error response dictionary
    """
    error_lower = error_msg.lower()

    if "no device found" in error_lower or "failed connecting" in error_lower:
        serial_suffix = f" with serial number {serial_number}" if serial_number else ""
        return build_response(
            "no_devices",
            f"No YubiKey found{serial_suffix}",
            info=None
        )

    return build_response(
        "error",
        f"ERROR running ykman: {error_msg}",
        info=None
    )


# ============================================================================
# MCP Tools
# ============================================================================

# @mcp.tool()
async def list_yubikeys() -> dict[str, Any]:
    """List all connected YubiKeys with their details."""
    try:
        result = run_ykman_command(["list"])

        # Parse output - each non-empty line is a device
        devices = [line for line in result.stdout.strip().split('\n') if line]

        if not devices:
            return build_response(
                "no_devices",
                "No YubiKeys detected",
                devices=[]
            )

        return build_response(
            "success",
            f"Found {len(devices)} YubiKey(s)",
            devices=devices
        )

    except subprocess.CalledProcessError as e:
        return build_response(
            "error",
            f"Error running ykman: {e.stderr}",
            devices=[]
        )
    except FileNotFoundError:
        return build_response(
            "error",
            "ykman not found. Please install yubikey-manager",
            devices=[]
        )


@mcp.tool()
async def get_yubikey_info(
    ctx: Context,
    serial_number: int | None = None
) -> dict[str, Any]:
    """Get detailed information about a specific YubiKey.

    Retrieves comprehensive information including firmware version, form factor,
    enabled applications (OTP, FIDO, CCID), and USB interfaces.

    Args:
        serial_number: The serial number of the YubiKey to query. If not provided
                      and only one YubiKey is connected, that device will be used.
                      If multiple devices are connected, serial_number is required.

    Returns:
        A dictionary containing:
            - status: "success", "error", or "no_devices"
            - message: Human-readable status message
            - info: Detailed device information (if successful)
            - serial_number: The serial number of the queried device (if successful)
    """
    try:
        info_text = get_ykman_info(serial_number=serial_number)

        if not info_text:
            return build_response(
                "no_devices",
                "No YubiKey information returned",
                info=None
            )

        return build_response(
            "success",
            "Successfully retrieved YubiKey information",
            info=info_text,
            serial_number=serial_number
        )

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)

        # Handle multiple devices case
        if "multiple yubikeys" in error_msg.lower():
            serial_number = await prompt_for_serial(ctx)

            if serial_number is None:
                return build_response(
                    "error",
                    "Operation cancelled or no serial number provided.",
                    info=None
                )

            # Retry with serial number
            try:
                info_text = get_ykman_info(serial_number=serial_number)
                return build_response(
                    "success",
                    "Successfully retrieved YubiKey information",
                    info=info_text,
                    serial_number=serial_number
                )
            except subprocess.CalledProcessError as retry_error:
                retry_msg = retry_error.stderr.strip() if retry_error.stderr else str(retry_error)
                return handle_ykman_error(retry_msg, serial_number)

        # Handle other errors
        return handle_ykman_error(error_msg, serial_number)

    except FileNotFoundError:
        return build_response(
            "error",
            "ykman not found. Please install yubikey-manager",
            info=None
        )


@mcp.tool()
async def hello_yubikey() -> str:
    """Say hello and check YubiKey availability."""
    try:
        result = subprocess.run(
            ["ykman", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        return f"Hello from YubiKey MCP Server! 🔑\n\nykman version: {version}\n\nUse 'list_yubikeys' to see connected devices."
    except FileNotFoundError:
        return "Hello from YubiKey MCP Server! ⚠️\n\nykman is not installed. Please install yubikey-manager:\n  pip install yubikey-manager"


def main():
    """Run the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
