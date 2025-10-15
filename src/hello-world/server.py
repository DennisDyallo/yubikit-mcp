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


class DeviceSelectionSchema(BaseModel):
    """Schema for eliciting device selection from user."""
    device_number: int = Field(
        description="The number of the YubiKey to select from the list (e.g., 1, 2, 3)",
        ge=1
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


async def prompt_for_device_selection(ctx: Context) -> int | None:
    """Prompt the user to select a YubiKey from a numbered list.

    Args:
        ctx: MCP context for eliciting user input

    Returns:
        Serial number of selected device, or None if cancelled/error
    """
    try:
        # Get list of connected devices
        result = run_ykman_command(["list"])
        devices = [line for line in result.stdout.strip().split('\n') if line]

        if not devices:
            await ctx.info("No YubiKeys detected")
            return None

        # Build numbered list message
        device_list = "\n".join([f"{i+1}. {device}" for i, device in enumerate(devices)])
        message = f"Multiple YubiKeys detected. Please select one:\n\n{device_list}\n\nEnter the number of the device you want to use:\n"

        # Prompt user for selection
        elicit_result = await ctx.elicit(
            message=message,
            schema=DeviceSelectionSchema
        )

        if elicit_result.action == "accept" and elicit_result.data:
            selected_index = elicit_result.data.device_number - 1

            # Validate selection
            if 0 <= selected_index < len(devices):
                # Extract serial number from device string
                # Format: "YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303"
                device_str = devices[selected_index]
                serial_str = device_str.split("Serial: ")[-1].strip()
                return int(serial_str)
            else:
                await ctx.info(f"Invalid selection: {elicit_result.data.device_number}")
                return None

        return None

    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
        await ctx.info(f"Error listing devices: {e}")
        return None


async def run_ykman_with_device_selection(
    ctx: Context,
    args: list[str],
    serial_number: int | None = None,
    retry_on_multiple: bool = True
) -> subprocess.CompletedProcess:
    """Execute a ykman command with automatic device selection on multiple devices.

    This wrapper handles the common pattern of:
    1. Try to run command with optional serial number
    2. If multiple devices error occurs, prompt user to select device
    3. Retry command with selected device

    Args:
        ctx: MCP context for user interaction
        args: Command arguments (e.g., ["info"], ["config", "usb", "--enable", "OATH"])
        serial_number: Optional serial number to target specific device
        retry_on_multiple: Whether to prompt for device selection on multiple device error

    Returns:
        CompletedProcess instance with stdout/stderr

    Raises:
        subprocess.CalledProcessError: If command fails
        ValueError: If user cancels device selection or no device selected
        FileNotFoundError: If ykman is not installed
    """
    try:
        # Build command with serial if provided
        full_args = []
        if serial_number is not None:
            full_args.extend(["--device", str(serial_number)])
        full_args.extend(args)

        return run_ykman_command(full_args)

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)

        # Handle multiple devices case
        if retry_on_multiple and "multiple yubikeys" in error_msg.lower():
            selected_serial = await prompt_for_device_selection(ctx)

            if selected_serial is None:
                raise ValueError("Operation cancelled or no device selected")

            # Retry with selected device (disable retry to prevent infinite loop)
            return await run_ykman_with_device_selection(
                ctx, args, selected_serial, retry_on_multiple=False
            )

        # Re-raise if not multiple devices or retry disabled
        raise


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
        result = await run_ykman_with_device_selection(ctx, ["info"], serial_number)
        info_text = result.stdout.strip()

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

    except ValueError as e:
        # User cancelled device selection
        return build_response(
            "error",
            str(e),
            info=None
        )

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
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
