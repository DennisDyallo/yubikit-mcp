# Debugging the YubiKey MCP Server

## Overview

This document explains how to debug the MCP server using VS Code's debugger.

## Two Debugging Approaches

### Approach 1: Launch Mode (Standalone Testing)
Use this when you want to test the server independently without Claude Code.

**How it works:**
- VS Code starts the server directly
- No MCP client connected
- Good for testing individual functions

**Usage:**
1. Open Debug panel (Ctrl+Shift+D)
2. Select "Debug YubiKey MCP Server (Launch)"
3. Set breakpoints in `server.py`
4. Press F5

**Limitation:** Server won't receive actual MCP requests since no client is connected.

---

### Approach 2: Attach Mode (Debug Live Server)
Use this when you want to debug the server while Claude Code (or any MCP client) is actively using it.

**How it works:**
1. Claude Code starts the server via `.mcp.json`
2. Server opens a debug port (5678)
3. VS Code attaches to the running server
4. You can debug actual MCP requests from Claude Code

**Usage:**

#### Step 1: Enable Debug Mode in `.mcp.json`

Add the `ENABLE_DEBUGPY` environment variable:

```json
{
  "mcpServers": {
    "yubikey-server-debug": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/dyallo/Code/y/yubikit-mcp/src/hello-world",
        "run",
        "server.py"
      ],
      "env": {
        "ENABLE_DEBUGPY": "1"
      }
    }
  }
}
```

#### Step 2: Restart Claude Code
Restart Claude Code so it picks up the new environment variable and starts the server with debugging enabled.

The server will **pause and wait** for the debugger to attach (because of `debugpy.wait_for_client()`).

#### Step 3: Attach VS Code Debugger
1. Open Debug panel (Ctrl+Shift+D)
2. Select "Attach to MCP Server"
3. Press F5

The server will now continue and you can debug live requests!

#### Step 4: Use the Server in Claude Code
1. In Claude Code, ask to use a YubiKey tool (e.g., "List my YubiKeys")
2. VS Code will hit your breakpoints
3. Step through the code, inspect variables, etc.

---

## Understanding the Code Changes

### `server.py` Changes

```python
def main():
    """Run the MCP server."""
    import os

    # Enable remote debugging if ENABLE_DEBUGPY is set
    if os.environ.get("ENABLE_DEBUGPY") == "1":
        try:
            import debugpy
            debugpy.listen(("localhost", 5678))  # Open debug port
            debugpy.wait_for_client()            # WAIT for VS Code to attach
            print("Debugger attached!", flush=True)
        except ImportError:
            print("debugpy not installed, skipping debug setup", flush=True)
        except Exception as e:
            print(f"Failed to setup debugpy: {e}", flush=True)

    mcp.run(transport='stdio')
```

**Key points:**
- `debugpy.listen(5678)` - Opens port 5678 for debugger connection
- `debugpy.wait_for_client()` - **Blocks** until VS Code attaches
  - Remove this line if you don't want the server to wait
  - Useful if you want to attach debugger mid-execution
- Only activates when `ENABLE_DEBUGPY=1` is set
- Gracefully handles missing debugpy package

### `.vscode/launch.json` Configurations

**Launch Mode:**
```json
{
  "name": "Debug YubiKey MCP Server (Launch)",
  "type": "debugpy",
  "request": "launch",  // VS Code STARTS the server
  "program": "${workspaceFolder}/src/hello-world/server.py",
  ...
}
```

**Attach Mode:**
```json
{
  "name": "Attach to MCP Server",
  "type": "debugpy",
  "request": "attach",  // VS Code CONNECTS to running server
  "connect": {
    "host": "localhost",
    "port": 5678  // Must match debugpy.listen() port
  },
  ...
}
```

---

## Why This Works

**The Problem:**
- MCP servers use stdio transport (stdin/stdout for communication)
- You can't run two instances simultaneously (Claude Code + VS Code debugger)

**The Solution:**
- Claude Code starts the server
- Server opens a **separate debug channel** on port 5678
- VS Code connects via TCP (not stdio)
- Stdin/stdout remain dedicated to MCP communication

**Result:**
- Claude Code talks to server via stdio
- VS Code debugger talks to server via TCP port 5678
- No conflicts!

---

## Alternative: MCP Inspector

If attach mode is too complex, use the official MCP Inspector instead:

```bash
npx @modelcontextprotocol/inspector \
  uv --directory /home/dyallo/Code/y/yubikit-mcp/src/hello-world run server.py
```

**Benefits:**
- Web UI at http://localhost:6274
- Test tools without writing MCP client code
- View logs and responses
- No debugger attachment needed

**Best for:**
- Quick testing
- Exploring tools
- Debugging tool behavior

**VS Code debugger is best for:**
- Setting breakpoints
- Stepping through code
- Inspecting variables
- Deep debugging

---

## Troubleshooting

**"debugpy could not be resolved" in VS Code:**
- Install debugpy: `uv add debugpy --dev`
- Or: Add it to `pyproject.toml` dev dependencies

**Server hangs on startup:**
- Check if `debugpy.wait_for_client()` is enabled
- Attach the VS Code debugger quickly
- Or comment out that line to make waiting optional

**Port 5678 already in use:**
- Change port in both `server.py` and `launch.json`
- Kill existing debugpy processes: `lsof -ti:5678 | xargs kill -9`

**No breakpoints hit:**
- Ensure `ENABLE_DEBUGPY=1` is set in `.mcp.json`
- Verify VS Code attached successfully (check Debug Console)
- Confirm you're using "Attach to MCP Server" configuration
