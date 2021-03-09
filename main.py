import os

import dotenv

from discordbot.bot import bot

dotenv.load_dotenv()

bot.run(os.getenv("BOT_TOKEN"))
