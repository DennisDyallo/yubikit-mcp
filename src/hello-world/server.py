#!/usr/bin/env python3
"""
YubiKey MCP Server - Hello World
A basic MCP server that lists connected YubiKeys.
"""

import subprocess
from typing import Any

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("yubikey-hello-world")


@mcp.tool()
async def list_yubikeys() -> dict[str, Any]:
    """List all connected YubiKeys with their details."""
    try:
        # Run ykman list command
        result = subprocess.run(
            ["ykman", "list"],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse output
        devices = []
        for line in result.stdout.strip().split('\n'):
            if line:
                # Example line: "YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303"
                devices.append(line)

        if not devices:
            return {
                "status": "no_devices",
                "message": "No YubiKeys detected",
                "devices": []
            }

        return {
            "status": "success",
            "message": f"Found {len(devices)} YubiKey(s)",
            "devices": devices
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Error running ykman: {e.stderr}",
            "devices": []
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "ykman not found. Please install yubikey-manager",
            "devices": []
        }


@mcp.tool()
async def get_yubikey_info(serial_number: int | None = None) -> dict[str, Any]:
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
        # Build command arguments
        cmd = ["ykman"]

        if serial_number is not None:
            cmd.extend(["--device", str(serial_number)])

        cmd.append("info")

        # Run ykman info command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        info_text = result.stdout.strip()

        if not info_text:
            return {
                "status": "no_devices",
                "message": "No YubiKey information returned",
                "info": None
            }

        return {
            "status": "success",
            "message": "Successfully retrieved YubiKey information",
            "info": info_text,
            "serial_number": serial_number
        }

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)

        # Handle specific error cases
        if "multiple devices" in error_msg.lower():
            return {
                "status": "error",
                "message": "Multiple YubiKeys detected. Please specify a serial_number.",
                "info": None
            }
        elif "no device found" in error_msg.lower() or "failed connecting" in error_msg.lower():
            return {
                "status": "no_devices",
                "message": f"No YubiKey found{f' with serial number {serial_number}' if serial_number else ''}",
                "info": None
            }
        else:
            return {
                "status": "error",
                "message": f"Error running ykman: {error_msg}",
                "info": None
            }

    except FileNotFoundError:
        return {
            "status": "error",
            "message": "ykman not found. Please install yubikey-manager",
            "info": None
        }


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
