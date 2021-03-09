import io
import json
import traceback

from discord import Attachment, DMChannel, File
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context

import remove_duplicates


async def no_dms_check(context: Context):
    if isinstance(context.channel, DMChannel):
        await context.send("You're not allowed to use this command in direct messages.")
        return False
    return True


class ProfileCleanerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.check(no_dms_check)
    @commands.command()
    async def clean(self, context: Context):
        for attachment in context.message.attachments:
            attachment: Attachment
            try:
                response = remove_duplicates.clean(json.loads(await attachment.read()))
                str_io = io.BytesIO(json.dumps(response.profile, indent="\t", ensure_ascii=False).encode())

                await context.send(
                    f"Found {response.duplicate_ids} duplicate id(s), removed {response.items_removed} item(s).",
                    file=File(str_io, attachment.filename),
                )
            except Exception as exception:
                await context.send(f"Error processing attachment {attachment.filename}")
                await context.send(f"```py\n{traceback.format_exc()}```")
                raise exception
