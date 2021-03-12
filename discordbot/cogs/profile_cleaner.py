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
                    f"Duplicate ids found: {len(response.duplicate_items)}\n"
                    f"Removed {response.removed_items_count} items with duplicate ids\n"
                    f"Removed {len(response.removed_orphan_items)} orphan items.",
                    file=File(str_io, attachment.filename),
                )
            except Exception as exception:
                await context.send(f"Error processing attachment {attachment.filename}")
                await context.send(f"```py\n{traceback.format_exc()}```")
                raise exception

    @commands.check(no_dms_check)
    @commands.command()
    async def analyze(self, context: Context):
        for attachment in context.message.attachments:
            attachment: Attachment
            response = remove_duplicates.clean(json.loads(await attachment.read()))

            duplicate_items = "\n".join(response.duplicate_items)
            orphan_items = "\n".join(response.removed_orphan_items)

            string = "\n".join(
                [
                    "```",
                    f"Duplicate items ({len(response.duplicate_items)}):",
                    f"{duplicate_items}",
                    f"Orphan items ({len(response.removed_orphan_items)}):",
                    f"{orphan_items}",
                    "```",
                ]
            )
            await context.send(
                "There's your report:", file=File(io.BytesIO(string.encode()), filename="report.md")
            )
