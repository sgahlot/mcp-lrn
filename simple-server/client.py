import asyncio
from fastmcp import Client

async def interact_with_server():
    print("--- Creating Client ---")

    # Option 1: Connect to a server run via `python my_server.py` (uses stdio)
    client = Client("server.py")

    # Option 2: Connect to a server run via `fastmcp run ... --transport sse --port 8080`
    """
    SG: THIS OPTION IS NOT WORKING (LAST TESTED ON JUNE 14, 2025)

    Failing with the following error (on the server):
    INFO:     127.0.0.1:63731 - "POST / HTTP/1.1" 404 Not Found

    Client has following output:
     -> invoking greet tool...
     An error occurred: Session terminated

    Server was started using the following command:
      fastmcp run server.py:mcp --transport sse --port 8080 --host 0.0.0.0
    """
    #client = Client("http://localhost:8080") # Use the correct URL/port

    # Next statement is giving the following error:
    # AttributeError: 'Client' object has no attribute 'target'
    #print(f"Client configured to connect to: {client.target}")

    try:
        async with client:
            print("--- Client Connected ---")

            print('\n -> Getting tools list...')
            tools = await client.list_tools()
            print(f"\n   -> Available tools: {tools}")
            # Call the 'greet' tool
            print('\n -> invoking greet tool...')
            greet_result = await client.call_tool("greet", {"name": "Remote Client"})
            print(f"\n   -> greet result: {greet_result}")

            # Read the 'config' resource
            print('\n -> invoking data://config resource...')
            config_data = await client.read_resource("data://config")
            print(f"\n   -> config resource: {config_data}")

            # Read user profile 102
            print('\n  -> invoking users://102/profile resource...')
            profile_102 = await client.read_resource("users://102/profile")
            print(f"\n   -> User 102 profile: {profile_102}\n")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("\n--- Client Interaction Finished ---\n")

if __name__ == "__main__":
    asyncio.run(interact_with_server())

