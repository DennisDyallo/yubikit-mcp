# YubiKey MCP Server - Hello World

A basic Model Context Protocol (MCP) server that lists connected YubiKeys.

## Features

- **hello_yubikey**: Check server status and ykman availability
- **list_yubikeys**: List all connected YubiKey devices

## Requirements

- Python 3.10 or later
- yubikey-manager (ykman)
- uv (recommended) or pip

## Installation

### Using uv (recommended)

```bash
cd src/hello-world
uv sync
```

### Using pip

```bash
cd src/hello-world
pip install -e .
```

## Usage

### Development Mode (MCP Inspector)

Test the server with the MCP Inspector:

```bash
uv run mcp dev server.py
```

### Install in Claude Desktop

```bash
uv run mcp install server.py --name "YubiKey Hello World"
```

Or manually configure `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yubikey-hello": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/src/hello-world/server.py"]
    }
  }
}
```

### Direct Execution

```bash
uv run server.py
```

### VS Code Integration (with GitHub Copilot)

The project includes `.vscode/mcp.json` for VS Code integration. To use:

1. **Prerequisites:**
   - VS Code 1.102+ with GitHub Copilot installed
   - MCP support is built-in (no extensions needed)

2. **Enable in VS Code:**
   - Open Chat view (Ctrl+Shift+I / Cmd+Shift+I)
   - Enable Agent mode

3. **Use YubiKey tools in chat:**
   ```
   @workspace Can you list my connected YubiKeys?
   @workspace Check YubiKey status
   ```

The MCP server starts automatically when Copilot needs the tools.

## Testing in Claude Desktop

Once installed, try these prompts:

- "Say hello and check YubiKey status"
- "List all connected YubiKeys"
- "Show me my YubiKey devices"

## Tools Available

### hello_yubikey
Returns a greeting message and checks if ykman is installed and working.

**Returns:**
```
Hello from YubiKey MCP Server! 🔑

ykman version: 5.x.x

Use 'list_yubikeys' to see connected devices.
```

### list_yubikeys
Lists all connected YubiKey devices with their details.

**Returns:**
```json
{
  "status": "success",
  "message": "Found 2 YubiKey(s)",
  "devices": [
    "YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303",
    "YubiKey 5 NFC (5.4.3) [OTP+FIDO+CCID] Serial: 9681620"
  ]
}
```

## Troubleshooting

**"ykman not found" error:**
```bash
pip install yubikey-manager
```

**On Linux, if you get permission errors:**
- Ensure `pcscd` is running: `sudo systemctl start pcscd`
- Add udev rules for YubiKey access (see yubikey-manager documentation)

**View Claude Desktop logs:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```
