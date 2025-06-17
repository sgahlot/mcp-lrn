import asyncio
from fastmcp import Client

async def run():
  async with Client("db-server.py") as client:
    print('Listing resources and tools...\n')
    resources = await client.list_resources()
    print(f' -> all resources: {resources}')

    tools = await client.list_tools()
    print(f' -> all tools: {tools}')

    # Call the tool
    # print('\n -> invoking tool...')
    # result = await client.call_tool("echo_tool", {"message": "Remote Client"})
    # print(f"   -> echo tool result: {result}")

    # Read the resource
    print('\n -> invoking resource to get all the employees...')
    result = await client.read_resource("employees://all")
    print(f"   -> All employees: {result}")

    print('\n -> invoking resource to get employee with id=1')
    result = await client.read_resource("employees://1")
    print(f"   -> Employee with id=1: {result}\n")


if __name__ == '__main__':
  asyncio.run(run())
