import aiosqlite
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional
import os

mcp = FastMCP(name="Employees MCP Server")
 
script_path = os.path.abspath(__file__)
base_database_dir = os.path.dirname(script_path)
DB_PATH = f"{base_database_dir}/db/employees.db"
TABLE_NAME = "employees"

@mcp.resource("employees://all")
async def get_all_employees() -> List[Dict]:
  """Returns all the employee records as a list of dictonaries"""

  try:
    async with aiosqlite.connect(DB_PATH) as conn:
      cursor = await conn.execute(f'SELECT * FROM {TABLE_NAME}')
      columns = [column[0] for column in cursor.description]
      employees = [dict(zip(columns, row)) async for row in cursor]
      await cursor.close()

    return employees
  except Exception as ex:
    return [{"error": f'Encountered an unexpected error while getting all the employees: {ex}\nDB_PATH used={DB_PATH}'}]


@mcp.tool("get_employees")
async def get_employees() -> List[Dict]:
  """
  Returns all the employee records as a list of dictonaries.
  Provided as a tool to run from inside Claude Desktop
  """
  return await get_all_employees()


@mcp.resource(uri="employee://{employee_id}", mime_type="application/json")
async def get_employee(employee_id: int) -> Optional[Dict]:
  """Returns a single employee record based on the given employee_id"""

  async with aiosqlite.connect(DB_PATH) as conn:
    cursor = await conn.execute(f'SELECT * FROM {TABLE_NAME} WHERE id = ?', (employee_id,))
    row = await cursor.fetchone()
    if row:
      columns = [column[0] for column in cursor.description]
      result = dict(zip(columns, row))
    else:
      result = None

    await cursor.close()
  
  return result


@mcp.tool("get_employee")
async def get_employee_by_id(employee_id: int) -> Optional[Dict]:
  """
  Returns a single employee record based on the given employee_id
  Provided as a tool to run from inside Claude Desktop
  """
  return await get_employee(employee_id)


@mcp.tool()
async def delete_employee(employee_id: int) -> bool:
  """Deletes an employee record based on the given employee_id. Returns True if successful"""

  async with aiosqlite.connect(DB_PATH) as conn:
    try:
      cursor = await conn.execute(f'DELETE FROM {TABLE_NAME} WHERE id = ?', (employee_id,))
      await conn.commit()
      success = cursor.rowcount > 0
      await cursor.close()
    except:
      success = False

  return success

@mcp.tool()
async def init_db(base_db_dir: str = '') -> str:
  """Initializes the Employee database by creating the database and inserting a few records in it"""

  # print('Initializing the database (OUTSIDE try/except)...')
  try:
    from init_employees import init_db
    # print('Initializing the database...')
    result = await init_db(False, base_db_dir)
  except Exception as ex:
    result = f'Encountered an unexpected error while initializing the db: {ex}'

  return result


if __name__ == '__main__':
  print(f"\n--- Starting {mcp} via __main__ ---")
  mcp.run(transport='stdio')
