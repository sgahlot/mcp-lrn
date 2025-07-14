import asyncio
from fastmcp import Client
from typing import List
import mcp
import json


async def get_all_employees(client: Client, extra_msg: str = ""):
  print(f"\n -> invoking resource to get all the employees{extra_msg}...")
  result = await client.read_resource("employees://all")
  await print_result(result, "All Employees")


async def get_one_employee(client: Client, employee_id: int, extra_msg: str = ""):
  print(f"\n -> invoking resource to get employee with id={employee_id}{extra_msg}")
  result = await client.read_resource(f"employee://{employee_id}")
  await print_result(result, f"Employee with id={employee_id}")


async def print_result(result: List[mcp.types.TextResourceContents], msg: str = ""):
  """
  Print the result of a resource call ONLY.
  Prints the URI of the resource that is ONLY available for a resource call, and the message.

  If the result is a list of TextResourceContents, print the contents of the first element.
  If the result is a single TextResourceContents, print the contents.
  If the result is a list of other types, print the result.
  """

  if len(result) > 0 and result[0] != None:
    contents: mcp.types.TextResourceContents = result[0]

    if contents != None:
      try:
        contents_json = json.dumps(json.loads(contents.text))
        print(f"    -> URI: {contents.uri}\n    -> {msg}: {contents_json}")
      except:
        print(f"    -> URI: {contents.uri}\n     -> {contents.text}")
    else:
      print(f"   -> {msg}: {result}")


async def delete_employee(client: Client, employee_id: int):
  print(f"\n -> invoking tool to delete employee with id={employee_id}")
  result = await client.call_tool("delete_employee", {"employee_id": employee_id})
  await print_text(result, "DELETE_EMPLOYEE result")


async def init_db(client: Client):
  print("\n -> Invoking init_db to initialize the Employees database from the client...")
  result = await client.call_tool("init_db")
  await print_text(result, "INIT_DB result")


async def print_text(result: List[mcp.types.TextResourceContents], msg: str = ""):
  """
  Print the result of a tool call ONLY.
  If the result is a list of TextResourceContents, print the contents of the first element.
  If the result is a single TextResourceContents, print the contents.
  If the result is a list of other types, print the result.
  """

  if len(result) > 0 and result[0] != None:
    print(f"    -> {msg}:")
    for row in result:
      contents: mcp.types.TextResourceContents = row
      try:
        contents_json = json.dumps(json.loads(contents.text))
        print(f"       - {contents_json}")
      except:
        print(f"       -> {contents.text}")
  else:
    print(f"   -> {msg}: {result}")


async def run():
  async with Client("db-server.py") as client:
    print("Listing resources and tools...\n")
    resources = await client.list_resources()
    print(" -> all resources:")
    for resource in resources:
      print(f"   -> {resource}")

    resource_templates = await client.list_resource_templates()
    print(" -> all resource templates:")
    for resource in resource_templates:
      print(f"   -> {resource}")

    tools = await client.list_tools()
    print(" -> all tools:")
    for tool in tools:
      print(f"   -> {tool}")

    await init_db(client)

    print(f"\n -> invoking tool to get all the employees...")
    result = await client.call_tool("get_employees")
    await print_text(result, "get_employees result (** from the tool **)")

    # Read the resource
    await get_all_employees(client)

    await get_one_employee(client, 1)

    print(f"\n -> invoking tool to get a singleemployee with id=1...")
    result = await client.call_tool("get_employee", {"employee_id": 1})
    await print_text(result, "get_employee result (** from the tool **)")

    await delete_employee(client, 1)

    await get_all_employees(client, " (AGAIN AFTER DELETING 1 Employee)")

    await get_one_employee(client, 1, " (SHOULD NOT BE FOUND AS THE Employee IS DELETED)")


if __name__ == "__main__":
  asyncio.run(run())
