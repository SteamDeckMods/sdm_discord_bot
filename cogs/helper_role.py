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
            self.timeout_role = config["Discord"]["Roles"]["TIMEOUT"]

    async def cog_check(self, ctx):
        """
        Precheck that prevents anyone without the a apropriate role
        from using any commands in this cog. This does not need to be called.
        """
        return self.helper_role in [r.id for r in ctx.author.roles]

    @commands.command()
    async def sitdown(self, ctx):
        """Add a timeout role to a set of mentioned users"""
        # TODO: I think there should be a few sanity checks about who we're
        # muting. But what checks would be important?
        for user in ctx.message.mentions:
            try:
                await user.add_roles(
                    discord.utils.get(ctx.guild.roles, id=self.timeout_role)
                )
            except discord.Forbidden as e:
                ctx.send(f"Couldn't add the role to {user}! Error:\n{e}")
        ctx.send("Added Timeout Role")

    @commands.command()
    async def sitdownrelease(self, ctx):
        for user in ctx.message.mentions:
            try:
                await user.remove_roles(
                    discord.utils.get(ctx.guild.roles, id=self.timeout_role)
                )
            except discord.Forbidden as e:
                ctx.send(f"Couldn't remove the role from {user}! Error:\n{e}")
        ctx.send("Removed Timeout Role")


def setup(bot):
    bot.add_cog(HelperRole(bot))
