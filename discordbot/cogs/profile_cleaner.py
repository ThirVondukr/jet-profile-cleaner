import io
import json

from discord import Attachment, DMChannel, File
from discord.ext import commands
from discord.ext.commands import Bot, Cog, CommandInvokeError, Context

import remove_duplicates
from templates import jinja_env


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
            response = remove_duplicates.clean(json.loads(await attachment.read()))
            message_template = jinja_env.get_template("clean.md")

            if response.profile_changed:
                str_io = io.BytesIO(json.dumps(response.profile, indent="\t", ensure_ascii=False).encode())
                await context.send(
                    message_template.render(response=response, ctx=context),
                    file=File(str_io, attachment.filename)
                )
            else:
                await context.send(message_template.render(response=response, ctx=context))

    @clean.error
    async def clean_error(self, ctx: Context, invoke_error: CommandInvokeError):
        error = invoke_error.original

        if isinstance(error, json.decoder.JSONDecodeError):
            await ctx.send(
                f'```py\n'
                f'{error.__class__.__name__}: {error}\n'
                f'```'
            )

    # @commands.check(no_dms_check)
    # @commands.command()
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
