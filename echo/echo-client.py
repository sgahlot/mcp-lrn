import asyncio
from fastmcp import Client


async def interact_with_server():
  print("--- Creating Client ---")

  # Option 1: Connect to a server run via `python my_server.py` (uses stdio)
  client = Client("echo-server.py")

  try:
    async with client:
      print("--- Client Connected ---")

      print("\n -> Getting tools list...")
      tools = await client.list_tools()
      print(f"   -> Available tools: {tools}")

      # Call the tool
      print("\n -> invoking echo tool...")
      result = await client.call_tool("echo_tool", {"message": "Remote Client"})
      print(f"   -> echo tool result: {result}")

      # Read the resource
      print("\n -> invoking echo resource...")
      result = await client.read_resource("echo://Calling-Echo-Resource")
      print(f"   -> echo resource result: {result}")

      # Read prompt
      print("\n  -> Getting all the prompt...")
      prompts = await client.list_prompts()
      print(f"   -> Available prompts: {prompts}\n")

      print('\n  -> Getting "echo_prompt" prompt...')
      result = await client.get_prompt(
        "echo_prompt", arguments={"message": "testing the echo prompt"}
      )
      print(f"   -> echo prompt result: {result}\n")

  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    print("\n--- Client Interaction Finished ---\n")


if __name__ == "__main__":
  asyncio.run(interact_with_server())
