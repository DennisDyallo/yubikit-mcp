# YubiKey MCP Server

> Bringing hardware-backed cryptographic security to AI agents through the Model Context Protocol

---

## What is This?

An **MCP (Model Context Protocol) server** that lets AI assistants interact with YubiKey hardware security tokens. Think of it as a bridge between AI tools (like Claude, GitHub Copilot, or any MCP-compatible client) and your YubiKey device.

### The 30-Second Overview

**Without this project:**
- AI assistants can't interact with hardware security devices
- You manually use command-line tools to manage YubiKeys
- Security operations can't be automated with AI

**With this project:**
- AI assistants can discover and manage your YubiKeys through natural conversation
- Generate OpenPGP keys, configure applications, and set security policies via voice/text
- Enable or disable NFC, require touch for operations, manage PINs - all through AI
- Your YubiKey becomes accessible to AI workflows while maintaining hardware security
- Future: Sign documents, manage OTPs, use PIV certificates, and more

---

## What is MCP?

**Model Context Protocol (MCP)** is like a USB port for AI assistants - it's a standard way for AI tools to connect to external services and data.

Just like USB lets you plug any device into any computer, MCP lets you plug any tool (like your YubiKey) into any AI assistant that supports the protocol.

**MCP has three main concepts:**

1. **Tools** - Functions the AI can call (e.g., "list YubiKeys", "generate OTP")
2. **Resources** - Data the AI can read (e.g., available certificates, device info)
3. **Prompts** - Pre-built templates for common workflows

### Why Use MCP Instead of Direct CLI Access?

**Good question!** AI agents *could* technically use `ykman` commands directly. Here's why MCP is better:

#### Without MCP (Direct CLI)
```bash
# AI must figure out commands, parse text output, handle errors
ykman list
ykman --device 12345 oath accounts code "GitHub:user"
```

**Problems:**
- ❌ **No security** - Agent has full shell access (can run ANY command)
- ❌ **No discoverability** - Agent doesn't know what operations are available
- ❌ **Error-prone** - Must parse text output, guess command syntax
- ❌ **Platform-specific** - Different implementation for each AI tool

#### With MCP
```python
# AI discovers and calls structured functions
list_yubikeys() → {"status": "success", "devices": [...]}
generate_otp(service="GitHub", account="user") → {"code": "123456"}
```

**Benefits:**
- ✅ **Security & Sandboxing** - Agent can ONLY do what you explicitly allow
- ✅ **Discoverability** - AI automatically sees available tools and their parameters
- ✅ **Structured Data** - JSON responses instead of parsing text
- ✅ **Workflow Consolidation** - One tool = complete workflow (e.g., `sign_document` handles cert selection → signing → verification)
- ✅ **Platform Independence** - Same tools work in Claude Code, VS Code, Rider, web apps
- ✅ **Context Awareness** - Resources show what YOUR YubiKey can do before running commands

**Real-world analogy:** MCP is like providing a REST API with documented endpoints, versus giving root shell access and saying "figure it out." Both can accomplish tasks, but MCP is safer, clearer, and easier to use correctly.

---

## Quick Start

### Prerequisites

- **Python 3.10+** installed
- **[uv](https://github.com/astral-sh/uv)** package manager (or pip)
- **YubiKey** hardware (optional for testing, required for actual operations)
- **yubikey-manager** (`ykman`) installed:
  ```bash
  pip install yubikey-manager
  ```

### Installation & Testing

1. **Clone and navigate to the hello-world example:**
   ```bash
   cd src/hello-world
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Test with MCP Inspector:**
   ```bash
   uv run mcp dev server.py
   ```

   This opens a web interface where you can test the tools interactively.

### Integration with AI Tools

This MCP server works with multiple AI platforms:

#### Claude Code (CLI)
Configuration file: `.mcp.json` in project root
```json
{
  "mcpServers": {
    "yubikey-hello-world": {
      "command": "uv",
      "args": ["--directory", "/path/to/yubikit-mcp/src/hello-world", "run", "server.py"]
    }
  }
}
```

#### VS Code + GitHub Copilot
Configuration file: `.vscode/mcp.json`
```json
{
  "servers": {
    "yubikey-hello-world": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "/path/to/yubikit-mcp/src/hello-world", "run", "server.py"]
    }
  }
}
```

#### JetBrains Rider / IntelliJ
Go to: `Settings → Tools → AI Assistant → Model Context Protocol (MCP)` and add:
```json
{
  "mcpServers": {
    "yubikey-hello-world": {
      "command": "uv",
      "args": ["--directory", "/path/to/yubikit-mcp/src/hello-world", "run", "server.py"]
    }
  }
}
```

**See [`.vscode/Interesting file paths.md`](.vscode/Interesting%20file%20paths.md) for detailed config locations.**

---

## How It Works

### Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│   AI Assistant  │ ◄─MCP──►│  YubiKey MCP     │ ◄─CLI──►│   YubiKey   │
│ (Claude/Copilot)│         │  Server (Python) │         │   Hardware  │
└─────────────────┘         └──────────────────┘         └─────────────┘
```

1. **AI Assistant** (Claude Code, VS Code, Rider) sends MCP requests
2. **MCP Server** (this project) translates requests to `ykman` commands
3. **ykman** communicates with the YubiKey hardware
4. Results flow back through the chain to the AI

### Current Implementation

The `src/hello-world/server.py` provides a comprehensive set of tools organized by functionality:

#### 🔍 Device Discovery & Information
- **`hello_yubikey`** - Checks if ykman is installed and shows version
- **`list_yubikeys`** - Lists all connected YubiKey devices with details
- **`get_yubikey_info`** - Get detailed firmware version, form factor, and USB interface information
- **`list_yubikey_applications`** - View which applications (OATH, PIV, FIDO2, etc.) are enabled over USB and NFC

#### ⚙️ Device Configuration
- **`configure_yubikey_applications`** - Enable or disable applications (OATH, PIV, FIDO2, OTP, OpenPGP, etc.) over USB or NFC transports

#### 🔐 OpenPGP (Email & File Encryption)
- **`get_openpgp_info`** - View OpenPGP application status, PIN retry counters, and key slot information
- **`generate_openpgp_key`** - Generate RSA key pairs directly on the YubiKey for email signing and encryption
- **`set_openpgp_touch_policy`** - Require physical touch for signature, encryption, or authentication operations
- **`set_openpgp_pin_retries`** - Configure how many incorrect PIN attempts are allowed before lockout

### Example Usage

After configuring your AI assistant, you can have natural conversations about YubiKey operations:

**Example 1: Device Discovery**
```
You: "Can you list my connected YubiKeys?"

AI: Found 1 YubiKey(s):
    - YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303
```

**Example 2: Configure Applications**
```
You: "I want to enable OATH and PIV over NFC on my YubiKey"

AI: Successfully enabled OATH, PIV over NFC on YubiKey (Serial: 16021303)
```

**Example 3: OpenPGP Key Generation**
```
You: "Generate an OpenPGP key for john@example.com with name John Doe"

AI: Successfully generated rsa2048 OpenPGP key pair for John Doe <john@example.com>
    Key generation took 87 seconds. Your private keys never left the YubiKey!
```

**Example 4: Security Hardening**
```
You: "Require touch for all OpenPGP signing operations"

AI: Successfully set touch policy for SIG key to 'on'. You'll now need to
    physically touch your YubiKey every time you sign an email or file.
```

**Example 5: Complete Workflow - Encrypt Grandma's Secret Cookie Recipe** 🍪
```
You: "Encrypt grandma's secret cookie recipe"

AI: Let me help you encrypt that precious family recipe! First, let me check
    your YubiKey setup...

    ✓ Found YubiKey 5 NFC (Serial: 16021303)
    ✓ Checking OpenPGP application status...

    Hmm, I don't see an OpenPGP key on your YubiKey yet. Would you like me to
    generate one? This will create a hardware-backed encryption key that never
    leaves your YubiKey.

You: "Yes, generate one for me"

AI: Perfect! I'll generate a key for you. What's your name and email?

You: "Jane Doe, jane@familyrecipes.com"

AI: Great! Generating RSA-2048 key pair on your YubiKey...

    ⚠️  This will take about 90 seconds. Please don't remove your YubiKey!

    🔑 Key generation in progress...
    💡 You may need to touch your YubiKey if prompted...

    ✅ Success! Generated OpenPGP key for Jane Doe <jane@familyrecipes.com>

    Now encrypting "grandmas-secret-cookies.txt" to your public key...

    ✓ File encrypted → grandmas-secret-cookies.txt.gpg

    🎉 Your recipe is now protected by military-grade hardware encryption!
    Only your YubiKey can decrypt it. Even if someone steals your computer,
    they can't read it without physically having your YubiKey.

    Want me to test decryption to make sure it works?

You: "Yes, decrypt it!"

AI: Decrypting with your YubiKey...

    👆 Please touch your YubiKey to authorize decryption...

    ✅ Decrypted successfully! Here's the secret:

    "Grandma's Chocolate Chip Cookies 🍪
     - 2 cups butter (must be room temperature!)
     - 1 cup love
     - 3 cups chocolate chips (Grandma always adds extra)
     - SECRET INGREDIENT: A pinch of cinnamon ✨"

    Your recipe is safe! The encrypted file can only be opened with your
    YubiKey, even if you store it in the cloud or email it to yourself.
```

---

## Project Structure

```
yubikit-mcp/
├── .mcp.json                    # Claude Code MCP config
├── .vscode/
│   ├── mcp.json                 # VS Code/Copilot MCP config
│   └── Interesting file paths.md # Config reference guide
├── src/
│   ├── hello-world/
│   │   ├── server.py            # MCP server implementation
│   │   ├── pyproject.toml       # Python dependencies
│   │   └── README.md            # Detailed usage guide
│   └── mcp-store/               # Separate project: MCP Marketplace
│       └── README.md            # See marketplace docs
├── CLAUDE.md                    # Developer guide for AI assistants
└── README.md                    # This file
```

---

## Technical Deep Dive

### MCP Server Implementation

The server uses **FastMCP**, a high-level Python framework for building MCP servers:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yubikey-hello-world")

@mcp.tool()
async def list_yubikeys() -> dict:
    """List all connected YubiKeys"""
    result = subprocess.run(["ykman", "list"], ...)
    return {"status": "success", "devices": [...]}
```

**Key Implementation Details:**

- **Transport:** stdio (standard input/output) for local AI assistants
- **Backend:** Uses `ykman` CLI via subprocess
- **Protocol:** JSON-RPC 2.0 over stdio
- **Logging:** Uses Python `logging` module (never `print()` - corrupts stdio)

### Multi-Device Handling

When multiple YubiKeys are connected, tools accept optional `device_serial` parameter:

```python
# Auto-select if only one device
devices = get_devices()
if len(devices) == 1:
    use_device(devices[0])
else:
    # Prompt user or return list
    return {"error": "Multiple devices found", "devices": devices}
```

### Security Considerations

- **No authentication in hello-world** - Basic example only
- **Future:** OAuth 2.1 + JWT validation for production
- **Hardware binding:** Use YubiKey attestation to bind operations to specific devices
- **Audit logging:** Track all security operations

---

## Roadmap & Future Tools

### ✅ Already Implemented
- **Device Management**: List devices, get detailed info, configure applications
- **OpenPGP Operations**: Key generation, touch policies, PIN configuration
- **Multi-Device Support**: Automatic device selection prompts when multiple YubiKeys are connected

### 🚧 In Development
These workflow-oriented tools are planned for future releases:

#### 1. PIV (Smart Card & Document Security)
- `sign_document` - Sign PDFs, contracts, reports with PIV certificates
- `encrypt_document` - Hardware-backed document encryption
- `verify_document_signature` - Verify document authenticity
- `generate_piv_certificate` - Create X.509 certificates for identity
- `authenticate_to_service` - Use PIV for API authentication

#### 2. OATH (Two-Factor Authentication)
- `generate_otp_for_service` - Get TOTP/HOTP codes for specific services
- `setup_totp_account` - Add new 2FA accounts to YubiKey
- `list_oath_accounts` - View all stored OATH credentials
- `backup_oath_credentials` - Secure backup of TOTP secrets

#### 3. FIDO2/WebAuthn
- `register_fido2_credential` - Register passwordless login for websites
- `list_fido2_credentials` - View registered FIDO2 credentials
- `delete_fido2_credential` - Remove specific credentials

#### 4. Agent-to-Agent Security
- `sign_message` - Cryptographically sign AI agent messages
- `verify_agent_signature` - Verify signatures from other agents
- `encrypt_agent_communication` - Secure agent-to-agent channels
- `establish_secure_channel` - Set up trusted connections

#### 5. Enterprise & Compliance
- `audit_credential_usage` - Track all cryptographic operations
- `rotate_expiring_credentials` - Automated certificate rotation
- `generate_attestation` - Prove operations happened on genuine YubiKey hardware

---

## YubiKey Protocol Support

This project can support all YubiKey capabilities:

- **OATH** - TOTP/HOTP for two-factor authentication
- **PIV** - Smart card, certificates, document signing
- **OpenPGP** - Email signing, file encryption
- **FIDO2/WebAuthn** - Passwordless authentication
- **YubiOTP** - Challenge-response, static passwords

---

## Related Projects

This repository also contains **[MCP Marketplace](src/mcp-store/README.md)** - a discovery and monetization platform for MCPB extensions (like this YubiKey MCP server).

The YubiKey MCP server could be packaged as a `.mcpb` bundle and published to the marketplace for wider distribution.

---

## Resources & Documentation

- **[MCP Documentation](https://modelcontextprotocol.io/)** - Official MCP protocol docs
- **[FastMCP Python SDK](https://github.com/jlowin/fastmcp)** - Framework used in this project
- **[yubikey-manager](https://github.com/Yubico/yubikey-manager)** - Backend CLI tool
- **[CLAUDE.md](CLAUDE.md)** - Developer guide for Claude Code contributors
- **[src/hello-world/README.md](src/hello-world/README.md)** - Detailed usage and troubleshooting

---

## Contributing

This is an early-stage project! Contributions welcome:

1. **Add new tools** following patterns in `CLAUDE.md`
2. **Improve security** - Add authentication, audit logging
3. **Support more protocols** - PIV, OATH, FIDO2 workflows
4. **Documentation** - Improve guides and examples

---

## License

[Specify your license here]

## Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/yubikit-mcp/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/yubikit-mcp/discussions)
- **MCP Community:** [MCP Discord](https://discord.gg/modelcontextprotocol)

---

**Built with ❤️ using the Model Context Protocol**

*Bringing hardware-backed security to AI agent workflows*
