from discord.ext import commands


class HelperRole(commands.Cog):
    """Manages all commands associated with the Helper Role"""

    def __init__(self):
        self.role = "Do this properly"

    async def cog_check(self, ctx):
        """
        Precheck that prevents anyone without the a apropriate role
        from using any commands in this cog. This does not need to be called.
        """
        return self.role == ctx.author.id


def setup(bot):
    bot.add_cog(HelperRole(bot))
