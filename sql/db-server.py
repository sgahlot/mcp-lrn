import aiosqlite
from fastmcp import FastMCP
from typing import List, Dict, Optional
 
mcp = FastMCP(name="Employees MCP Server")
 
DB_PATH = "db/employees.db"
TABLE_NAME = "employees"

@mcp.resource("employees://all")
async def get_all_employees() -> List[Dict]:
  """Returns all the employee records as a list of dictonaries"""

  async with aiosqlite.connect(DB_PATH) as conn:
    cursor = await conn.execute(f'SELECT * FROM {TABLE_NAME}')
    columns = [column[0] for column in cursor.description]
    employees = [dict(zip(columns, row)) async for row in cursor]
    await cursor.close()

  return employees


@mcp.resource("employees://{employee_id}")
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


if __name__ == '__main__':
  print(f"\n--- Starting {mcp} via __main__ ---")
  mcp.run(transport='stdio')
