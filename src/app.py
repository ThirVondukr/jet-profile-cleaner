import discord
from discord.ext import commands

import settings
from cogs.profile_cleaner import ProfileCleanerCog


async def create_app():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(
        command_prefix=settings.bot.prefix,
        intents=intents,
        case_insensitive=True,
    )
    await bot.add_cog(ProfileCleanerCog(bot=bot))

    return bot
