from fastmcp import FastMCP
import asyncio  # We'll need this later for the client

# Instantiate the server, giving it a name
mcp = FastMCP(name="My First MCP Server")


def info_mcp(msg: str = None):
  print(f"{msg}\n -> {mcp}\n")


info_mcp("FastMCP server object created")


# -----------------------
# Expose some tools (functions exposed to the client)...
# -----------------------


@mcp.tool()
def greet(name: str) -> str:
  """Returns a simple greeting."""
  return f"Hello, {name}!"


@mcp.tool()
def add(a: int, b: int) -> int:
  """Adds two numbers together."""
  return a + b


info_mcp("Tools 'greet' and 'add' added.")


# -----------------------
# Expose some resources (expose data via a URI)...
# -----------------------
APP_CONFIG = {"theme": "dark", "version": "1.1", "feature_flags": ["new_dashboard"]}


# Static resource
@mcp.resource("data://config")
def get_config() -> dict:
  """Provides the application configuration."""
  return APP_CONFIG


info_mcp("Resource 'data://config' added.")

USER_PROFILES = {
  101: {"name": "Alice", "status": "active"},
  102: {"name": "Bob", "status": "inactive"},
}


# dynamic resource template (with param in the uri)
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
  """Retrieves a user's profile by their ID."""
  # The {user_id} from the URI is automatically passed as an argument
  return USER_PROFILES.get(user_id, {"error": "User not found"})


info_mcp("Resource template 'users://{user_id}/profile' added.")


# -----------------------
# Expose some prompts (for reusable interaction pattern)...
# -----------------------


@mcp.prompt("summarize")
async def summarize_prompt(text: str) -> list[dict]:
  """Generates a prompt to summarize the provided text."""
  return [
    {
      "role": "system",
      "content": "You are a helpful assistant skilled at summarization.",
    },
    {"role": "user", "content": f"Please summarize the following text:\n\n{text}"},
  ]


info_mcp("Prompt 'summarize' added.")


if __name__ == "__main__":
  print("\n--- Starting FastMCP Server via __main__ ---")
  # This starts the server, typically using the stdio transport by default
  mcp.run()
