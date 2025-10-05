# MCP Configuration File Paths

## Project-Level Configurations

- **`.mcp.json`** (project root)
  - **Platform:** Claude Code
  - **Path:** `/home/dyallo/Code/y/yubikit-mcp/.mcp.json`
  - **Scope:** This project only

- **`.vscode/mcp.json`**
  - **Platform:** VS Code + GitHub Copilot
  - **Path:** `/home/dyallo/Code/y/yubikit-mcp/.vscode/mcp.json`
  - **Scope:** This project only

## User-Level Configurations

- **Claude Code Global Settings**
  - **Platform:** Claude Code (all projects)
  - **Path:** `~/.claude.json` (contains `mcpServers` section)
  - **Scope:** All projects globally

- **JetBrains/IntelliJ GitHub Copilot MCP**
  - **Platform:** Rider, IntelliJ, PyCharm, etc.
  - **Path:** `/home/dyallo/.config/github-copilot/intellij/mcp.json`
  - **Scope:** All JetBrains IDEs with GitHub Copilot

## Configuration Format Differences

### Claude Code (`.mcp.json` or `~/.claude.json`)
```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"]
    }
  }
}
```

### VS Code (`.vscode/mcp.json`)
```json
{
  "servers": {
    "server-name": {
      "type": "stdio",
      "command": "executable",
      "args": ["arg1", "arg2"]
    }
  }
}
```

### JetBrains/Rider
```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "cwd": "/optional/working/directory"
    }
  }
}
```