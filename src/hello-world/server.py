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
    suggested_next_action: str | None = None,
    **extra_fields: Any
) -> dict[str, Any]:
    """Build a standardized response dictionary.

    Args:
        status: Response status code
        message: Human-readable message
        suggested_next_action: Optional suggestion for what the user should do next
        **extra_fields: Additional fields to include in response

    Returns:
        Response dictionary with status, message, optional suggestion, and any extra fields
    """
    response = {
        "status": status,
        "message": message,
    }

    if suggested_next_action:
        response["suggested_next_action"] = suggested_next_action

    response.update(extra_fields)
    return response


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
        subprocess.CalledProcessError: If command fails (includes full command in error)
        ValueError: If user cancels device selection or no device selected
        FileNotFoundError: If ykman is not installed
    """
    # Build command with serial if provided
    full_args = []
    if serial_number is not None:
        full_args.extend(["--device", str(serial_number)])
    full_args.extend(args)

    # Build full command string for logging/errors
    full_command = "ykman " + " ".join(full_args)

    try:
        await ctx.info(f"Executing: {full_command}")
        return run_ykman_command(full_args)

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)

        # Handle multiple devices case
        if retry_on_multiple and "multiple yubikeys" in error_msg.lower():
            selected_serial = await prompt_for_device_selection(ctx)

            if selected_serial is None:
                raise ValueError(f"Operation cancelled or no device selected. Command was: {full_command}")

            # Retry with selected device (disable retry to prevent infinite loop)
            return await run_ykman_with_device_selection(
                ctx, args, selected_serial, retry_on_multiple=False
            )

        # Enhance error message with full command
        enhanced_error = f"Command failed: {full_command}\nError: {error_msg}"

        # Create a new exception with enhanced message
        new_error = subprocess.CalledProcessError(
            e.returncode,
            ["ykman"] + full_args,
            output=e.output,
            stderr=enhanced_error
        )
        raise new_error


# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
async def list_yubikeys() -> dict[str, Any]:
    """List all connected YubiKeys with their details.

    Returns information about all YubiKeys currently connected to the system,
    including their model, firmware version, serial number, and enabled applications.

    Returns:
        A dictionary containing:
            - status: "success", "error", or "no_devices"
            - message: Human-readable status message
            - devices: List of device strings with full details (if successful)
            - count: Number of devices found (if successful)
    """
    try:
        result = run_ykman_command(["list"])

        # Parse output - each non-empty line is a device
        devices = [line for line in result.stdout.strip().split('\n') if line]

        if not devices:
            return build_response(
                "no_devices",
                "No YubiKeys detected",
                devices=[],
                count=0
            )

        return build_response(
            "success",
            f"Found {len(devices)} YubiKey(s)",
            suggested_next_action="Use 'get_yubikey_info' to see detailed information about a specific device, or 'list_yubikey_applications' to view application status",
            devices=devices,
            count=len(devices)
        )

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return build_response(
            "error",
            f"Error running ykman: {error_msg}",
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
            suggested_next_action="Use 'list_yubikey_applications' to see application status, or 'configure_yubikey_applications' to enable/disable applications",
            info=info_text,
            serial_number=serial_number
        )

    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as e:
        # ValueError: User cancelled device selection
        # CalledProcessError: Command failed (already enhanced with full command by wrapper)
        # FileNotFoundError: ykman not installed
        return build_response("error", str(e), info=None)


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


# ============================================================================
# Config Tools
# ============================================================================

@mcp.tool()
async def configure_yubikey_applications(
    ctx: Context,
    transport: str,
    enable_applications: list[str] | None = None,
    disable_applications: list[str] | None = None,
    serial_number: int | None = None
) -> dict[str, Any]:
    """Enable or disable YubiKey applications over USB or NFC.

    This tool allows you to control which applications are available on your YubiKey
    over different transports (USB or NFC). Common applications: OATH, PIV, FIDO2,
    FIDO (U2F), OTP, OpenPGP, HSMAUTH.

    Args:
        transport: Transport to configure ("usb" or "nfc")
        enable_applications: List of applications to enable (e.g., ["OATH", "PIV", "FIDO2", "OTP", "U2F", "OPENPGP", "HSMAUTH"])

        disable_applications: List of applications to disable (e.g., ["OATH", "PIV", "FIDO2", "OTP", "U2F", "OPENPGP", "HSMAUTH"])
        serial_number: Optional serial number of the YubiKey to configure

    Returns:
        Dictionary with status and message about the configuration changes

    Example:
        # Enable OATH and PIV over NFC
        configure_yubikey_applications(transport="nfc", enable_applications=["OATH", "PIV", "FIDO2", "OTP", "U2F", "OPENPGP", "HSMAUTH"])

        # Disable OTP over USB
        configure_yubikey_applications(transport="usb", disable_applications=["OATH", "PIV", "FIDO2", "OTP", "U2F", "OPENPGP", "HSMAUTH"])
    """
    if transport.lower() not in ["usb", "nfc"]:
        return build_response(
            "error",
            f"Invalid transport: {transport}. Must be 'usb' or 'nfc'."
        )

    if not enable_applications and not disable_applications:
        return build_response(
            "error",
            "Must specify at least one application to enable or disable"
        )

    try:
        force="--force"
        args = ["config", transport.lower()]

        # Add enable flags - each app needs its own --enable flag
        if enable_applications:
            for app in enable_applications:
                args.append("--enable")
                args.append(app.upper())

        # Add disable flags - each app needs its own --disable flag
        if disable_applications:
            for app in disable_applications:
                args.append("--disable")
                args.append(app.upper())

        args.append(force)

        result = await run_ykman_with_device_selection(ctx, args, serial_number)

        enabled_msg = f"enabled {', '.join(enable_applications)}" if enable_applications else ""
        disabled_msg = f"disabled {', '.join(disable_applications)}" if disable_applications else ""
        action_msg = " and ".join(filter(None, [enabled_msg, disabled_msg]))

        return build_response(
            "success",
            f"Successfully {action_msg} over {transport.upper()}",
            suggested_next_action="Use 'list_yubikey_applications' to verify the configuration changes took effect",
            output=result.stdout.strip() if result.stdout else None
        )

    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as e:
        return build_response("error", str(e))


@mcp.tool()
async def list_yubikey_applications(
    ctx: Context,
    serial_number: int | None = None
) -> dict[str, Any]:
    """List the enabled/disabled status of all applications on a YubiKey.

    This tool shows which applications are currently enabled over USB and NFC transports.

    Args:
        serial_number: Optional serial number of the YubiKey to query. If not provided
                      and only one YubiKey is connected, that device will be used.

    Returns:
        A dictionary containing:
            - status: "success", "error", or "no_devices"
            - message: Human-readable status message
            - applications: Dict with USB and NFC application status (if successful)
            - serial_number: The serial number of the queried device (if successful)
    """
    try:
        result = await run_ykman_with_device_selection(ctx, ["info"], serial_number)
        info_text = result.stdout.strip()

        if not info_text:
            return build_response(
                "no_devices",
                "No YubiKey information returned",
                applications=None
            )

        # Parse the info output to extract application status
        # The info output contains a table like:
        # Applications    USB             NFC
        # Yubico OTP      Enabled         Enabled
        # FIDO U2F        Enabled         Enabled
        # ...

        applications = {"usb": {}, "nfc": {}}
        in_app_section = False

        for line in info_text.split('\n'):
            line = line.strip()

            # Detect the applications table header
            if line.startswith("Applications"):
                in_app_section = True
                continue

            # Skip empty lines
            if not line:
                in_app_section = False
                continue

            # Parse application status lines
            if in_app_section and line:
                parts = line.split()
                if len(parts) >= 3:
                    # Handle multi-word app names (e.g., "Yubico OTP", "FIDO U2F")
                    # The last two parts are USB and NFC status
                    nfc_status = parts[-1]
                    usb_status = parts[-2]
                    app_name = " ".join(parts[:-2])

                    applications["usb"][app_name] = usb_status
                    applications["nfc"][app_name] = nfc_status

        return build_response(
            "success",
            "Successfully retrieved application status",
            suggested_next_action="Use 'configure_yubikey_applications' to enable or disable specific applications over USB or NFC",
            applications=applications,
            raw_info=info_text,
            serial_number=serial_number
        )

    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as e:
        return build_response("error", str(e), applications=None)


# ============================================================================
# OpenPGP Tools
# ============================================================================

@mcp.tool()
async def get_openpgp_info(
    ctx: Context,
    serial_number: int | None = None
) -> dict[str, Any]:
    """Get information about the OpenPGP application on a YubiKey.

    Shows PIN retry counters, key slot status, and configuration details
    for the OpenPGP smartcard application.

    Args:
        serial_number: Optional serial number of the YubiKey to query. If not provided
                      and only one YubiKey is connected, that device will be used.

    Returns:
        A dictionary containing:
            - status: "success", "error", or "no_devices"
            - message: Human-readable status message
            - info: OpenPGP application information (if successful)
            - serial_number: The serial number of the queried device (if successful)
    """
    try:
        result = await run_ykman_with_device_selection(ctx, ["openpgp", "info"], serial_number)
        info_text = result.stdout.strip()

        if not info_text:
            return build_response(
                "no_devices",
                "No OpenPGP information returned",
                info=None
            )

        return build_response(
            "success",
            "Successfully retrieved OpenPGP application information",
            suggested_next_action="Use 'set_openpgp_touch_policy' to require touch for key operations, or 'set_openpgp_pin_retries' to configure PIN attempt limits",
            info=info_text,
            serial_number=serial_number
        )

    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as e:
        return build_response("error", str(e), info=None)


@mcp.tool()
async def set_openpgp_touch_policy(
    ctx: Context,
    key_slot: str,
    policy: str,
    admin_pin: str | None = None,
    serial_number: int | None = None
) -> dict[str, Any]:
    """Set touch policy for OpenPGP keys.

    Require physical touch to use private keys for cryptographic operations.
    This adds an extra layer of security by ensuring that someone with physical
    access to the YubiKey must actively approve each use.

    Args:
        key_slot: Key slot to configure - "sig" (signature), "enc" (encryption),
                 "aut" (authentication), or "att" (attestation)
        policy: Touch policy to set:
               - "on": Touch required for each use
               - "off": No touch required (default)
               - "fixed": Touch required, cannot be disabled without deleting key
               - "cached": Touch required, cached for 15s after use
               - "cached-fixed": Touch required, cached for 15s, cannot be disabled
        admin_pin: Admin PIN for OpenPGP (if not provided, will be prompted)
        serial_number: Optional serial number of the YubiKey to configure

    Returns:
        Dictionary with status and message about the touch policy change

    Examples:
        # Require touch for authentication key
        set_openpgp_touch_policy(key_slot="aut", policy="on")

        # Enable cached touch for signature key (touch cached for 15s)
        set_openpgp_touch_policy(key_slot="sig", policy="cached")

        # Set fixed touch policy (cannot be undone without deleting key)
        set_openpgp_touch_policy(key_slot="enc", policy="fixed", admin_pin="12345678")
    """
    # Validate key slot
    valid_slots = ["sig", "enc", "aut", "att"]
    if key_slot.lower() not in valid_slots:
        return build_response(
            "error",
            f"Invalid key slot: {key_slot}. Must be one of: {', '.join(valid_slots)}"
        )

    # Validate policy
    valid_policies = ["on", "off", "fixed", "cached", "cached-fixed"]
    if policy.lower() not in valid_policies:
        return build_response(
            "error",
            f"Invalid policy: {policy}. Must be one of: {', '.join(valid_policies)}"
        )

    try:
        args = ["openpgp", "keys", "set-touch", key_slot.lower(), policy.lower(), "--force"]

        # Add admin PIN if provided
        if admin_pin:
            args.extend(["--admin-pin", admin_pin])

        result = await run_ykman_with_device_selection(ctx, args, serial_number)

        return build_response(
            "success",
            f"Successfully set touch policy for {key_slot.upper()} key to '{policy}'",
            suggested_next_action="Use 'get_openpgp_info' to verify the touch policy was applied correctly",
            output=result.stdout.strip() if result.stdout else None
        )

    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as e:
        return build_response("error", str(e))


@mcp.tool()
async def set_openpgp_pin_retries(
    ctx: Context,
    pin_retries: int,
    reset_code_retries: int,
    admin_pin_retries: int,
    admin_pin: str | None = None,
    serial_number: int | None = None
) -> dict[str, Any]:
    """Set the number of retry attempts for OpenPGP PINs.

    Configure how many times a user can enter incorrect PINs before they are
    blocked. After the retry count is exhausted, the PIN will be blocked and
    must be reset using the Reset Code or Admin PIN.

    Args:
        pin_retries: Number of retry attempts for the User PIN (1-127)
        reset_code_retries: Number of retry attempts for the Reset Code (1-127)
        admin_pin_retries: Number of retry attempts for the Admin PIN (1-127)
        admin_pin: Current Admin PIN (if not provided, will be prompted)
        serial_number: Optional serial number of the YubiKey to configure

    Returns:
        Dictionary with status and message about the retry configuration

    Examples:
        # Set all retry counts to 10 attempts
        set_openpgp_pin_retries(pin_retries=10, reset_code_retries=10, admin_pin_retries=10)

        # Set conservative retry limits
        set_openpgp_pin_retries(pin_retries=3, reset_code_retries=3, admin_pin_retries=5)

        # Set high retry limits for testing
        set_openpgp_pin_retries(pin_retries=127, reset_code_retries=127, admin_pin_retries=127)
    """
    # Validate retry counts
    if not (1 <= pin_retries <= 127):
        return build_response("error", f"PIN retries must be between 1 and 127, got {pin_retries}")

    if not (1 <= reset_code_retries <= 127):
        return build_response("error", f"Reset Code retries must be between 1 and 127, got {reset_code_retries}")

    if not (1 <= admin_pin_retries <= 127):
        return build_response("error", f"Admin PIN retries must be between 1 and 127, got {admin_pin_retries}")

    try:
        args = [
            "openpgp", "access", "set-retries",
            str(pin_retries),
            str(reset_code_retries),
            str(admin_pin_retries),
            "--force"
        ]

        # Add admin PIN if provided
        if admin_pin:
            args.extend(["--admin-pin", admin_pin])

        result = await run_ykman_with_device_selection(ctx, args, serial_number)

        return build_response(
            "success",
            f"Successfully set PIN retry limits: PIN={pin_retries}, Reset Code={reset_code_retries}, Admin PIN={admin_pin_retries}",
            suggested_next_action="Use 'get_openpgp_info' to verify the retry limits were applied correctly",
            output=result.stdout.strip() if result.stdout else None
        )

    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as e:
        return build_response("error", str(e))


def main():
    """Run the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
