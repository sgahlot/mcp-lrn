import asyncio
from fastmcp import Client

"""
Usage

1. Run the server first:
    uv run server.py

2. Then run the client (in another terminal):
    uv run client.py
"""

async def interact_with_server():
    print("--- Creating Client ---")

    client = Client("server.py")

    try:
        async with client:
            print("--- Client Connected ---")

            print('\n -> Getting tools list...')
            tools = await client.list_tools()
            print(f"\n   -> Available tools: {tools}")

            print('\n -> invoking random_string tool...')
            random_string_result = await client.call_tool("random_string", {"length": 10})
            print(f"\n   -> random_string result: {random_string_result}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("\n--- Client Interaction Finished ---\n")

if __name__ == "__main__":
    asyncio.run(interact_with_server())

