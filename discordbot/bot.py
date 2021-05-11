from discord.ext import commands

from discordbot.cogs.profile_cleaner import ProfileCleanerCog

bot = commands.Bot(command_prefix="!!", case_insensitive=True)

bot.add_cog(ProfileCleanerCog(bot=bot))
