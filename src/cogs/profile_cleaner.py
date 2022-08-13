import json
from json.decoder import JSONDecodeError
from typing import List

from discord import Attachment, DMChannel
from discord.ext import commands
from discord.ext.commands import Bot, Cog, CommandInvokeError, Context

import cleaning
from utils import dict_to_file


async def no_dms_check(context: Context):
    if isinstance(context.channel, DMChannel):
        await context.send("You can't use this command in dm's.")
        return False
    return True


class ProfileCleanerCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.check(no_dms_check)
    @commands.command(
        brief="Cleans the profile",
        description="Removes all duplicate items from attached profile.json file.",
    )
    async def clean(self, context: Context):
        if not context.message.attachments:
            await context.send(
                f"{context.message.author.mention}\n"
                "No attachments found!\n"
                "You should attach your profile file to the message.",
            )
            return

        attachment: Attachment = context.message.attachments[0]
        response = cleaning.duplicates.clean(json.loads(await attachment.read()))
        response.profile, broken_ammo_amount = cleaning.ammo.clean(response.profile)

        if any(
            [
                response.duplicate_items,
                response.removed_orphan_items,
                broken_ammo_amount,
            ]
        ):
            messages: List[str] = [f"{context.message.author.mention}"]
            if response.duplicate_items:
                messages.append(
                    f"Removed {len(response.duplicate_items)} duplicate item(s)."
                )
            if response.removed_orphan_items:
                messages.append(
                    f"Removed {len(response.removed_orphan_items)} orphan item(s)."
                )

            if broken_ammo_amount:
                messages.append(f"Removed {broken_ammo_amount} broken ammo stacks.")

            await context.send(
                "\n".join(messages),
                file=dict_to_file(response.profile, attachment.filename),
            )
        else:
            await context.send(
                f"{context.message.author.mention} No duplicate or broken items were found in profile"
            )

    @clean.error
    async def clean_error(self, ctx: Context, invoke_error: CommandInvokeError):
        error = invoke_error.original

        lines: List[str] = []
        if isinstance(error, JSONDecodeError):
            lines.extend(
                [
                    f"{ctx.message.author.mention}",
                    "Your profile seems to be not a valid json file, did you edit it manually?",
                ]
            )

        lines.extend(
            [
                "",
                "Error stacktrace:"
                f"```py\n"
                f"{error.__class__.__name__}: {error}\n```",
            ]
        )
        await ctx.send(content="\n".join(lines))
