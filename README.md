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
- AI assistants can list connected YubiKeys
- Future: AI can help you sign documents, generate OTPs, manage certificates
- Your YubiKey becomes accessible to AI workflows while maintaining hardware security

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

### Current Implementation (Hello World)

The `src/hello-world/server.py` provides two basic tools:

- **`hello_yubikey`** - Checks if ykman is installed and shows version
- **`list_yubikeys`** - Lists all connected YubiKey devices with details

### Example Usage

After configuring your AI assistant, you can ask:

```
"Can you list my connected YubiKeys?"
```

The AI will use the MCP server to execute the command and respond with:
```json
{
  "status": "success",
  "message": "Found 1 YubiKey(s)",
  "devices": [
    "YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303"
  ]
}
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

### 1. Identity & Authentication
- `authenticate_to_service` - Use PIV for API authentication
- `generate_attestation_certificate` - Create identity certificates
- `verify_identity_proof` - Cryptographic identity verification

### 2. Document Security
- `sign_document` - Sign PDFs, contracts, reports
- `encrypt_document` - Hardware-backed encryption
- `verify_document_signature` - Verify authenticity

### 3. Two-Factor Operations (OATH)
- `generate_otp_for_service` - Get TOTP/HOTP codes
- `setup_totp_account` - Add new 2FA accounts
- `backup_oath_credentials` - Secure backup

### 4. Agent-to-Agent Security
- `sign_message` - Cryptographically sign AI messages
- `encrypt_agent_communication` - Secure agent channels
- `establish_secure_channel` - Set up trusted connections

### 5. Credential Management
- `provision_new_credential` - Create new certificates/keys
- `rotate_expiring_credentials` - Automated cert rotation
- `audit_credential_usage` - Compliance tracking

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
