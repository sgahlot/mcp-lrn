from init_employees import init_db
import asyncio

async def main():
  print('Invoking init to initialize the db...')
  await init_db()

if __name__ == '__main__':
  asyncio.run(main())
