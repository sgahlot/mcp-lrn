from init_employees import init_db
import asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', level=logging.INFO)


async def main():
  logger.info("Invoking init to initialize the db...")
  await init_db()


if __name__ == "__main__":
  asyncio.run(main())
