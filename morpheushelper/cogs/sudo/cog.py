import sys

from discord import TextChannel, Message
from discord.ext import commands
from discord.ext.commands import check, Context, CheckFailure

from PyDrocsid.cog import Cog
from PyDrocsid.config import Config
from PyDrocsid.emojis import name_to_emoji
from PyDrocsid.events import call_event_handlers
from PyDrocsid.permission import permission_override
from .permissions import Permission
from ..contributor import Contributor


@check
def is_sudoer(ctx: Context) -> bool:
    if ctx.author.id != 370876111992913922:
        raise CheckFailure(f"{ctx.author.mention} is not in the sudoers file. This incident will be reported.")

    return True


class SudoCog(Cog, name="Sudo"):
    CONTRIBUTORS = [Contributor.Defelo]
    PERMISSIONS = Permission

    def __init__(self):
        self.sudo_cache: dict[TextChannel, Message] = {}

    async def on_command_error(self, ctx: Context, _):
        if ctx.author.id == 370876111992913922:
            self.sudo_cache[ctx.channel] = ctx.message

    @commands.command(hidden=True)
    @is_sudoer
    async def sudo(self, ctx: Context, *, cmd: str):
        message: Message = ctx.message
        message.content = ctx.prefix + cmd

        if cmd == "!!" and ctx.channel in self.sudo_cache:
            message.content = self.sudo_cache.pop(ctx.channel).content

        permission_override.set(Config.PERMISSION_LEVELS.max())
        await self.bot.process_commands(message)

    @commands.command()
    @Permission.reload.check
    async def reload(self, ctx: Context):
        await call_event_handlers("ready")
        await ctx.message.add_reaction(name_to_emoji["white_check_mark"])

    @commands.command()
    @Permission.stop.check
    async def stop(self, ctx: Context):
        await ctx.message.add_reaction(name_to_emoji["white_check_mark"])
        await self.bot.close()

    @commands.command()
    @Permission.kill.check
    async def kill(self, ctx: Context):
        await ctx.message.add_reaction(name_to_emoji["white_check_mark"])
        sys.exit(1)
