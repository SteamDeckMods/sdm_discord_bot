from discord.ext import commands
import discord
import json


class HelperRole(commands.Cog):
    """Manages all commands associated with the Helper Role"""

    def __init__(self, bot):
        self.bot = bot
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)
            self.helper_role = config["Discord"]["Roles"]["HELPER"]
            self.sitdown_role = config["Discord"]["Roles"]["SITDOWN"]

    async def cog_check(self, ctx):
        """
        Precheck that prevents anyone without an apropriate role
        from using any commands in this cog. This does not need to be called.
        """
        return self.helper_role in [r.id for r in ctx.author.roles]

    @commands.command()
    async def sitdown(self, ctx):
        """Add a sitdown role to a set of mentioned users"""
        for user in ctx.message.mentions:
            try:
                await user.add_roles(
                    discord.utils.get(ctx.guild.roles, id=self.sitdown_role)
                )
            except discord.Forbidden as e:
                await ctx.send(f"Couldn't put {user} in sit-down. Error:\n{e}")
            await ctx.send(f"Added {user} to sit-down")

    @commands.command()
    async def sitdownrelease(self, ctx):
        for user in ctx.message.mentions:
            try:
                await user.remove_roles(
                    discord.utils.get(ctx.guild.roles, id=self.sitdown_role)
                )
            except discord.Forbidden as e:
                await ctx.send(f"Couldn't remove {user} from sit-down. Error:\n{e}")
            await ctx.send(f"Released {user} from sit-down")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")


def setup(bot):
    bot.add_cog(HelperRole(bot))
