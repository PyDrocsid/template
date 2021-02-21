from PyDrocsid.permission import BasePermission
from discord import Embed
from discord.ext import commands

from PyDrocsid.cog import Cog
from PyDrocsid.translations import translations
from cogs.contributor import Contributor
from colours import Colours


class CodeblocksCog(Cog, name="Codeblocks command"):
    CONTRIBUTORS = [Contributor.pohlium, Contributor.Defelo, Contributor.wolflu]
    PERMISSIONS = BasePermission

    @commands.command(name="codeblocks", aliases=["codeblock", "code", "c"])
    async def codeblocks(self, ctx):
        await ctx.send(
            embed=Embed(
                title=translations.codeblocks_title,
                description=translations.codeblocks_description,
                colour=Colours.CodeBlocks,
            )
        )