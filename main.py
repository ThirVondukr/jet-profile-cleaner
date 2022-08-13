import asyncio

import dotenv


async def main():
    import app
    import settings

    bot = await app.create_app()
    async with bot:
        await bot.start(token=settings.bot.token)


if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())
