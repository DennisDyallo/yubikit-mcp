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
