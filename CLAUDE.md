# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains an MCP (Model Context Protocol) server for YubiKey integration. The project brings hardware-backed cryptographic security to AI agent workflows through YubiKey hardware tokens.

**Backend**: Uses [yubikey-manager](https://github.com/Yubico/yubikey-manager) (ykman) as the underlying library/CLI tool for YubiKey operations.

## Design Philosophy

**Workflow-First Approach**: Design tools around complete user workflows rather than exposing low-level technical operations. Consolidate multi-step processes into single, cohesive tools.

**Example**: Instead of separate `get_certificate`, `sign_hash`, `verify_signature` tools, provide `sign_document` that handles the complete workflow.

## Core Architecture Principles

### Tool Organization
- **0-30 tools**: Use namespace organization with forward slashes (e.g., `files/read`, `database/query`)
- **30+ tools**: Implement dynamic toolset management, loading only relevant tools based on context
- **Enterprise scale**: Separate into multiple MCP servers by domain, permissions, or performance needs

### Tool Categories (Workflow-Oriented)
1. **Identity & Authentication**: `authenticate_to_service`, `generate_attestation_certificate`, `verify_identity_proof`
2. **Document Security**: `sign_document`, `encrypt_document`, `verify_document_signature`
3. **Communication Security**: `sign_message`, `encrypt_agent_communication`, `establish_secure_channel`
4. **Credential Management**: `provision_new_credential`, `rotate_expiring_credentials`, `audit_credential_usage`
5. **Two-Factor Operations**: `generate_otp_for_service`, `setup_totp_account`, `backup_oath_credentials`

### Resource Exposure (MCP Resources)
- `yubikey://device/capabilities` - Available YubiKey features and slots
- `yubikey://certificates/inventory` - Installed certificates and validity
- `yubikey://oath/accounts` - Configured OATH accounts
- `yubikey://audit/recent` - Recent security operations log

### Authentication Pattern
Follow OAuth 2.1 with JWT validation. The server acts as a Resource Server validating tokens from trusted Authorization Servers, not handling authentication directly. Use hardware token binding via YubiKey attestation.

## Natural Language Integration

Use intuitive tool names:
- `prove_identity_to_api` instead of `piv_authenticate`
- `secure_this_document` instead of `gpg_sign_detached`
- `setup_secure_comms_with_agent` instead of `exchange_public_keys`

Provide context-rich responses with security details and compliance information.

## YubiKey Protocol Support

- **PGP**: Message/file signing, encryption, decryption
- **PIV**: Certificate-based authentication, document signing, smart card operations
- **OATH**: TOTP/HOTP generation for 2FA workflows
- **FIDO2/WebAuthn**: Passwordless authentication
- **YubiHSM**: Hardware security module operations

## Target Use Cases

1. **Document Workflow Agents**: Automated signing of contracts, reports, legal documents
2. **API Security Agents**: Authentication to protected endpoints using PIV certificates
3. **Agent-to-Agent Communication**: Cryptographically signed messages between AI agents
4. **Compliance and Audit**: Hardware-backed security for regulatory requirements

## MCP Implementation Stack

### Technology Stack
- **MCP SDK**: Python MCP SDK (`mcp[cli]` package)
- **Server Framework**: FastMCP (high-level) or low-level Server for advanced use
- **Backend**: yubikey-manager (ykman) for YubiKey operations
- **Transport**: stdio (for Claude Desktop) or Streamable HTTP (for remote access)

### Project Structure
```
yubikit-mcp/
├── server.py              # Main MCP server implementation
├── pyproject.toml         # Python dependencies
└── README.md              # Usage documentation
```

## Implementation Backend: yubikey-manager

### Device Selection

**Critical**: When multiple YubiKeys are connected, ykman requires explicit device selection via `--device SERIAL`. Always handle this gracefully:

```bash
# List all devices
ykman list
# Output: YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303

# Target specific device
ykman --device 16021303 info
```

### Key ykman Command Structure

**Device & Configuration:**
- `ykman list` - List all connected YubiKeys with serials, firmware versions, enabled interfaces
- `ykman --device SERIAL info` - Show device type, firmware, form factor, enabled applications
- `ykman config {usb|nfc|set-lock-code|reset}` - Manage USB/NFC interfaces and lock codes

**OATH (TOTP/HOTP) - Two-Factor Authentication:**
- `ykman oath info` - Display OATH application status
- `ykman oath accounts code [QUERY]` - Generate OTP codes for matching accounts
- `ykman oath accounts add NAME SECRET [--touch]` - Add account with optional touch requirement
- `ykman oath access change` - Set/change OATH password protection

**PIV - Smart Card & Certificates:**
- `ykman piv info` - Display PIV application status
- `ykman piv keys generate --algorithm ECCP256 SLOT pubkey.pem` - Generate key pair
- `ykman piv certificates generate --subject "CN=name" SLOT pubkey.pem` - Generate self-signed cert
- `ykman piv access change-pin --pin OLD --new-pin NEW` - Change PIN

**OpenPGP - Email & Document Signing:**
- `ykman openpgp info` - Display OpenPGP status
- `ykman openpgp keys set-touch {aut|sig|enc} {on|off|fixed}` - Configure touch requirements
- `ykman openpgp access set-retries PIN RESET ADMIN` - Set retry limits

**FIDO - Passwordless Authentication:**
- `ykman fido info` - Display FIDO2 application status
- `ykman fido access change-pin --pin OLD --new-pin NEW` - Change FIDO2 PIN
- `ykman fido credentials list` - List discoverable credentials
- `ykman fido fingerprints` - Manage fingerprints (if supported)

**YubiOTP - Challenge-Response & Static Passwords:**
- `ykman otp info` - Display slot status
- `ykman otp chalresp --generate SLOT` - Program challenge-response credential
- `ykman otp static --generate SLOT --length 38` - Program static password
- `ykman otp calculate SLOT CHALLENGE` - Perform challenge-response operation

### Integration Approach

The MCP server wraps ykman functionality into workflow-oriented tools. Instead of exposing raw commands, consolidate operations into semantic, agent-friendly tools that handle complete workflows including device selection.

**Example Mapping:**
- High-level: `generate_otp_for_service(service_name, account, device_serial=None)`
- Backend: `ykman [--device SERIAL] oath accounts code {service_name}:{account}`

**Multi-Device Handling:**
1. If `device_serial` not provided, check if only one YubiKey connected
2. If multiple devices, either prompt for selection or return list of available devices
3. Cache device selection for session to avoid repeated prompts

### Platform Requirements

- **Python**: 3.10 or later (yubikey-manager dependency)
- **Linux**: Requires `pcscd` running for SmartCard interface
- **Installation**: `pip install yubikey-manager`
- **Permissions**: May need HID interface permissions on Linux

## MCP Server Development Guidelines

### Core MCP Concepts

**Three MCP Primitives:**
1. **Tools** (Model-controlled): Functions the LLM can actively call - used for actions like signing documents, generating OTPs
2. **Resources** (Application-controlled): Read-only data sources that provide context (device capabilities, certificates, OATH accounts)
3. **Prompts** (User-controlled): Pre-built templates for common workflows (document signing, compliance setup)

### FastMCP Server Pattern

```python
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("yubikey")

# Tool example: Generate OTP
@mcp.tool()
async def generate_otp(service: str, account: str, device_serial: str = None) -> str:
    """Generate TOTP/HOTP code for a service."""
    cmd = ["ykman"]
    if device_serial:
        cmd.extend(["--device", device_serial])
    cmd.extend(["oath", "accounts", "code", f"{service}:{account}"])
    # Execute command and return result

# Resource example: Device capabilities
@mcp.resource("yubikey://device/{serial}/capabilities")
def get_device_capabilities(serial: str) -> str:
    """Get YubiKey device capabilities and status."""
    # Return JSON with device info
```

### Critical MCP Implementation Rules

**Logging (CRITICAL for stdio transport):**
- ❌ NEVER use `print()` - corrupts JSON-RPC messages
- ✅ Use `logging` module which writes to stderr
- ✅ Use `await ctx.info()`, `await ctx.debug()` within tools

**Tool Design:**
- Use workflow-first approach: one tool = one complete workflow
- Example: `sign_document` handles certificate selection, signing, and verification - not separate tools
- Include device_serial parameter with smart defaults (auto-select if only one device)

**Context Usage:**
```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def long_operation(ctx: Context) -> str:
    await ctx.info("Starting operation")
    await ctx.report_progress(progress=0.5, total=1.0, message="Processing...")
    return "Complete"
```

**Error Handling:**
- Validate device_serial exists before operations
- Handle "Multiple YubiKeys detected" gracefully
- Return clear error messages for missing dependencies

### Running the Server

**Development/Testing:**
```bash
uv run mcp dev server.py
```

**Install in Claude Desktop:**
```bash
uv run mcp install server.py --name "YubiKey Security"
```

**Claude Desktop Config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "yubikey": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/server.py"]
    }
  }
}
```

### MCP Protocol Flow

1. **Initialization**: Client sends `initialize` with capabilities → Server responds with capabilities
2. **Tool Discovery**: Client sends `tools/list` → Server returns available tools with schemas
3. **Tool Execution**: Client sends `tools/call` with arguments → Server executes and returns results
4. **Notifications**: Server can send `notifications/tools/list_changed` when tools change

### Security Considerations

**OAuth 2.1 Pattern (for HTTP transport):**
- Server acts as Resource Server, validates JWT tokens
- Use `TokenVerifier` protocol for token validation
- Bind operations to specific YubiKey via attestation

**User Consent:**
- Implement clear confirmations for sensitive operations
- Use context elicitation for user approval: `await ctx.elicit(message, schema)`
