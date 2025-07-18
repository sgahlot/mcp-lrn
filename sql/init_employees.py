async def init_db(should_print: bool = True, base_db_dir: str = "") -> str:
  import sqlite3
  import os
  import logging

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', level=logging.INFO)

  base_database_dir = base_db_dir if base_db_dir != "" else os.getcwd()
  logger.info(f"Base database directory: {base_database_dir}")

  result: str = f"Creating database in {base_db_dir}/db..."

  # Create db directory if it doesn't exist
  os.makedirs(f"{base_database_dir}/db", exist_ok=True)

  conn = sqlite3.connect("db/employees.db")

  cursor = conn.cursor()

  TABLE_NAME = "employees"
  cursor.execute(f"""
  CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            department TEXT,
            salary REAL,
            hire_date TEXT
        )
    """)

  # Sample employee data
  employees = [
    (1, "John", "Doe", "john.doe@company.com", "Engineering", 85000, "2020-01-15"),
    (
      2,
      "Jane",
      "Smith",
      "jane.smith@company.com",
      "Marketing",
      78000,
      "2019-03-20",
    ),
    (
      3,
      "Michael",
      "Johnson",
      "michael.j@company.com",
      "Sales",
      92000,
      "2021-06-10",
    ),
    (4, "Emily", "Williams", "emily.w@company.com", "HR", 65000, "2022-02-28"),
    (
      5,
      "David",
      "Brown",
      "david.b@company.com",
      "Engineering",
      95000,
      "2018-11-05",
    ),
    (6, "Sarah", "Davis", "sarah.d@company.com", "Finance", 88000, "2021-09-15"),
    (7, "Robert", "Miller", "robert.m@company.com", "Sales", 89000, "2020-07-22"),
    (8, "Lisa", "Wilson", "lisa.w@company.com", "Marketing", 82000, "2019-12-01"),
    (
      9,
      "James",
      "Taylor",
      "james.t@company.com",
      "Engineering",
      91000,
      "2022-04-18",
    ),
    (
      10,
      "Jennifer",
      "Anderson",
      "jennifer.a@company.com",
      "HR",
      68000,
      "2021-11-30",
    ),
  ]

  cursor.executemany(
    f"""
      INSERT OR REPLACE INTO {TABLE_NAME}(id, first_name, last_name, email, department, salary, hire_date)
              VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    employees,
  )

  conn.commit()

  result += f"\n {len(employees)} {TABLE_NAME} inserted..."
  if should_print:
    logger.info(result)

  cursor.execute(f"SELECT * FROM {TABLE_NAME}")
  rows = cursor.fetchall()
  if should_print:
    for row in rows:
      logger.info(f" -> {row}")

  conn.close()

  return result
