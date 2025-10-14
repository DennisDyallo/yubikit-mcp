#!/usr/bin/env python3
"""
YubiKey MCP Server - Hello World
A basic MCP server that lists connected YubiKeys.
"""

from pydantic import BaseModel, Field
from mcp.server.fastmcp import Context, FastMCP

# Initialize FastMCP server

mcp = FastMCP("hello-world")

class ParamSchema(BaseModel):
    """Schema for eliciting user input."""
    name: str | None = Field(
        description="Your name",
        examples=["Alice", "Bob"]
    )

@mcp.tool()
async def hello_world(ctx: Context) -> str:
    """A simple hello world function."""

    elicit_result = await ctx.elicit(
            message="Please provide your name",
            schema=ParamSchema
        )
    if elicit_result.action == "accept" and elicit_result.data:
        name = elicit_result.data.name
    else:
        return "Operation cancelled or declined."
    return f"Hello, {name}!"

def main():
    """Run the MCP server."""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()