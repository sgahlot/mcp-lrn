import asyncio
from fastmcp import Client
from typing import List

async def get_all_employees(client: Client, extra_msg: str = ''):
  print(f'\n -> invoking resource to get all the employees{extra_msg}...')
  result = await client.read_resource("employees://all")

  if len(result) > 0:
    contents: mcp.types.TextResourceContents = result[0]

    if contents != None and contents.text != None:
      try:
        import json
        contents_json = json.dumps(json.loads(contents.text))
        print(f'    -> URI: {contents.uri}\n    -> All Employees: {contents_json}')
      except:
        print(f'    -> URI: {contents.uri}\n     -> {contents.text}')
    else:
      # Backup print
      print(f"   -> All employees: {result}")
  else:
    print(f'    -> Employees NOT FOUND...')


async def get_one_employee(client: Client, employee_id: int, extra_msg: str = ''):
  print(f'\n -> invoking resource to get employee with id={employee_id}{extra_msg}')
  result = await client.read_resource(f"employee://{employee_id}")
  if len(result) > 0:
    contents: mcp.types.TextResourceContents = result[0]

    if contents != None and contents.text != None:
      import json

      # print(f'Type of text={type(contents.text)}')
      try:
        contents_json = json.dumps(json.loads(contents.text))
        print(f'    -> URI: {contents.uri}\n    -> Employee with id={employee_id}: {contents_json}')
        # contents_json = json.dumps(json.loads(contents.text), indent=2)
      except:
        print(f'    -> URI: {contents.uri}\n     -> {contents.text}')
    else:
      # Backup print
      print(f"   -> Employee with id={employee_id}: {result}\n")
  else:
    print(f'    -> Employee with id={employee_id} NOT FOUND...')


async def delete_employee(client: Client, employee_id: int):
  print(f'\n -> invoking tool to delete employee with id={employee_id}')
  result = await client.call_tool("delete_employee", {'employee_id': employee_id})
  if len(result) > 0:
    contents: mcp.types.TextResourceContents = result[0]

    if contents != None:
      print(f'    -> Deleted: {contents.text}')
    else:
      print(f"   -> Deletion result: {result}")
  else:
    print(f"   -> Deletion result: {result}")


async def init_db(client: Client):
  print('\n -> Invoking init_db to initialize the Employees database from the client...')
  result = await client.call_tool('init_db')
  await print_text(result, 'INIT_DB result')


async def print_text(result: List[mcp.types.TextResourceContents], msg: str=''):
  if len(result) > 0 and result[0] != None:
    contents: mcp.types.TextResourceContents = result[0]
    print(f'    -> {msg}: {contents.text}')
  else:
    print(f"   -> {msg}: {result}")


async def run():
  async with Client("db-server.py") as client:
    print('Listing resources and tools...\n')
    resources = await client.list_resources()
    print(' -> all resources:')
    for resource in resources:
      print(f'   -> {resource}')

    resource_templates = await client.list_resource_templates()
    print(' -> all resource templates:')
    for resource in resource_templates:
      print(f'   -> {resource}')

    tools = await client.list_tools()
    print(' -> all tools:')
    for tool in tools:
      print(f'   -> {tool}')

    await init_db(client)
    #print('\n -> Invoking init_db to initialize the Employees database from the client...')
    #result = await client.call_tool('init_db')
    #print(f'    -> INIT_DB result: {result}')

    # Read the resource
    await get_all_employees(client)

    await get_one_employee(client, 1)

    await delete_employee(client, 1)

    await get_all_employees(client, ' (AGAIN AFTER DELETING 1 Employee)')

    await get_one_employee(client, 1, ' (SHOULD NOT BE FOUND AS THE Employee IS DELETED)')


if __name__ == '__main__':
  asyncio.run(run())
