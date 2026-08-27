import asyncio

from sqlalchemy import text

from stellar.config.database import engine


async def main():

    async with engine.connect() as connection:

        result = await connection.execute(
            text("SELECT 1")
        )

        print(result.scalar_one())

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())