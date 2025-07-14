from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP(name="Echo")


def info_mcp(msg: Optional[str] = None):
  print(f"{msg}\n -> {mcp}\n")


info_mcp("FastMCP server object created")


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
  """Echo a message as a resource"""
  return f"Resource echo: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
  """Echo a message as a tool"""
  return f"Tool echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
  """Create an echo prompt"""
  return f"Please process this message: {message}"


info_mcp("resource [echo://{message}] added")
info_mcp('tool for "echo" added')
info_mcp("prompt added")

if __name__ == "__main__":
  print("\n--- Starting echo Server via __main__ ---")
  # This starts the server, typically using the stdio transport by default
  mcp.run()
