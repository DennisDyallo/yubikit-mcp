Developer Guide: Creating YubiKey MCP Server
Based on comprehensive analysis of the Model Context Protocol documentation, here's everything a developer needs to create a proper MCP server for YubiKey integration.

MCP Overview and Architecture
What is MCP: The Model Context Protocol (MCP) is an open-source standard that enables AI applications to connect to external data sources and tools. It acts like "USB-C for AI applications," providing a standardized way to integrate external systems with language models.

Key Architecture Components:

MCP Host: AI application (like Claude Desktop) that coordinates connections

MCP Client: Component that maintains connection to MCP servers

MCP Server: Programs that provide context and capabilities (what you'll build)

Core MCP Capabilities
MCP servers can provide three main types of capabilities:

1. Tools (Model-Controlled)
Functions that AI models can actively call and decide when to use based on user requests. Tools enable actions like:

Signing documents with YubiKey certificates

Generating OTPs for 2FA

Encrypting/decrypting data

Authenticating to services

2. Resources (Application-Driven)
Read-only data sources that provide context, such as:

YubiKey device capabilities and status

Installed certificates and their validity

OATH accounts configuration

Audit logs of recent operations

3. Prompts (User-Controlled)
Pre-built templates that guide users through workflows:

Document signing workflows

Compliance audit setup

Secure communication initialization

Protocol Specifications
Core Protocol Details
Format: JSON-RPC 2.0 messages over UTF-8 encoding

Architecture: Stateful connections with capability negotiation

Lifecycle: Initialize → Negotiate capabilities → Operate → Shutdown

Current Version: 2025-06-18

Transport Mechanisms
stdio transport (recommended): Communication via standard input/output

Streamable HTTP transport: HTTP POST with optional Server-Sent Events

Implementation Requirements
1. Server Initialization
Every MCP server must implement the initialization handshake:

python
# Server capabilities declaration
capabilities = {
    "tools": {"listChanged": True},
    "resources": {"subscribe": True, "listChanged": True}, 
    "prompts": {"listChanged": True}
}
2. Tool Implementation Pattern
python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yubikey")

@mcp.tool()
async def sign_document(document_path: str, key_slot: int) -> str:
    """Sign a document using YubiKey PIV certificate"""
    # Validate inputs using JSON Schema
    # Perform YubiKey operation
    # Return structured response
    return f"Document signed successfully with slot {key_slot}"
3. Resource Implementation
python
@mcp.resource("yubikey://device/capabilities") 
def get_device_capabilities() -> str:
    """Expose YubiKey device capabilities as a resource"""
    return json.dumps({
        "piv_slots": ["9a", "9c", "9d", "9e"],
        "oath_accounts": 15,
        "firmware_version": "5.7.1"
    })
4. Protocol Message Handling
Tool Discovery:

json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
Tool Execution:

json
{
  "jsonrpc": "2.0", 
  "method": "tools/call",
  "params": {
    "name": "sign_document",
    "arguments": {
      "document_path": "/path/to/contract.pdf",
      "key_slot": 9
    }
  },
  "id": 2
}
Security and Safety Requirements
MCP emphasizes security as a core principle:

1. User Consent and Control
Users must explicitly consent to all data access and operations

Implement clear UIs for reviewing and authorizing activities

Provide human-in-the-loop confirmations for sensitive operations

2. Tool Safety
Tools represent arbitrary code execution and must be treated with caution

Obtain explicit user consent before invoking any tool

Validate all inputs and implement proper access controls

3. Implementation Guidelines
Build robust consent and authorization flows

Implement appropriate access controls and data protections

Follow security best practices in integrations

Consider privacy implications in feature designs

Development Best Practices
1. Logging Guidelines
Critical: For stdio-based servers, never write to stdout - this corrupts JSON-RPC messages

python
# ❌ Bad (breaks protocol)
print("Processing request")

# ✅ Good (proper logging) 
import logging
logging.info("Processing request")
2. Error Handling
Implement two error reporting mechanisms:

Protocol Errors: Standard JSON-RPC errors for unknown tools, invalid arguments

Tool Execution Errors: Reported in results with isError: true

3. Content Types
Support multiple content types in responses:

Text content for natural language responses

Image content for visual data (base64 encoded)

Resource links for additional context

Structured content for typed data

YubiKey-Specific Implementation Considerations
1. Tool Categories for YubiKey Server
python
# Identity & Authentication
@mcp.tool()
async def authenticate_to_service(service_url: str, auth_method: str, credentials_slot: int):
    """Authenticate to a service using YubiKey credentials"""

# Document Security  
@mcp.tool()
async def sign_document(document_path: str, signature_format: str, key_slot: int):
    """Cryptographically sign documents with hardware security"""

# Two-Factor Operations
@mcp.tool() 
async def generate_otp_for_service(service_name: str, account: str):
    """Generate TOTP/HOTP for 2FA workflows"""
2. Resource Exposure
python
# Device status and capabilities
@mcp.resource("yubikey://device/capabilities")
def device_capabilities(): 
    """Current YubiKey features and available slots"""

# Certificate inventory
@mcp.resource("yubikey://certificates/inventory")
def certificate_inventory():
    """Installed certificates and their validity periods"""

# OATH account management  
@mcp.resource("yubikey://oath/accounts")
def oath_accounts():
    """Configured OATH accounts for 2FA"""
3. Prompt Templates
python
@mcp.prompt("document_signing_workflow")
def document_signing_prompt(document_type: str):
    """Guide users through secure document signing process"""
    return {
        "messages": [{
            "role": "user",
            "content": {
                "type": "text", 
                "text": f"Please review and sign this {document_type} using your YubiKey..."
            }
        }]
    }
Getting Started
1. SDK Installation
bash
# Python (recommended for YubiKey integration)
pip install "mcp[cli]"

# Or use uv for faster development
uv add "mcp[cli]" pyscard  # For smart card operations
2. Basic Server Structure
python
from mcp.server.fastmcp import FastMCP
from typing import Any
import asyncio

# Initialize server
mcp = FastMCP("yubikey")

# Add your tools, resources, and prompts here

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
3. Testing with Claude Desktop
Configure Claude Desktop by editing ~/Library/Application Support/Claude/claude_desktop_config.json:

json
{
  "mcpServers": {
    "yubikey": {
      "command": "python",
      "args": ["/path/to/your/yubikey_server.py"]
    }
  }
}
Advanced Features
1. Notifications
Send real-time updates when YubiKey state changes:

python
# Notify clients when device is inserted/removed
await mcp.notify("notifications/tools/list_changed")
2. Progress Tracking
For long-running operations like key generation:

python
async def generate_keypair(key_type: str):
    # Report progress during key generation
    await ctx.report_progress(completed=50, total=100)
3. Structured Output
Define schemas for consistent data exchange:

python
from pydantic import BaseModel

class SigningResult(BaseModel):
    success: bool
    signature: str
    timestamp: str
    certificate_subject: str

@mcp.tool()
async def sign_data(data: str) -> SigningResult:
    # Return structured, validated data
    return SigningResult(...)
This comprehensive guide provides all the technical specifications, security requirements, and implementation patterns needed to build a production-ready YubiKey MCP server that integrates seamlessly with AI applications while maintaining the hardware security guarantees that make YubiKeys trusted in enterprise environments.
