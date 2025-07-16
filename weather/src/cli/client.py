import asyncio
from fastmcp import Client
import os

async def run():
  try:
    print("--- Creating Client ---")
    server_script_path = os.path.join(os.path.dirname(__file__), "../../server.py")
    async with Client(server_script_path) as client:
      print("Listing resources and tools...")

      resources = await client.list_resources()
      if resources and len(resources) > 0:
        print(" -> all resources:")
        for resource in resources:
          print(f"   -> {resource}")
      else:
        print("No resources found")

      resource_templates = await client.list_resource_templates()
      if resource_templates and len(resource_templates) > 0:
        print(" -> all resource templates:")
        for resource in resource_templates:
          print(f"   -> {resource}")
      else:
        print("No resources templates found")

      tools = await client.list_tools()
      if tools and len(tools) > 0:
        print(" -> all tools:")
        for tool in tools:
          print(f"   -> {tool}")
      else:
        print("No tools found")

  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    print("\n--- Client Interaction Finished ---\n")


if __name__ == "__main__":
  asyncio.run(run())
