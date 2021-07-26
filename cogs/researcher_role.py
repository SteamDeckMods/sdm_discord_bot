from discord.ext import commands
import json
import discord


class ResearcherRole(commands.Cog):
    """Manages all commands associated with the Helper Role"""

    def __init__(self, bot):
        self.bot = bot
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)

            # Load Relevant Roles
            self.news_role = config["Discord"]["Roles"]["NEWS"]
            self.researcher_role = config["Discord"]["Roles"]["RESEARCHER"]

            # Load Relevant Channels
            self.news_channel = config["Discord"]["Channels"]["NEWS"]
            self.research_channel = config["Discord"]["Channels"]["RESEARCH"]

    async def cog_check(self, ctx):
        """
        Precheck that prevents anyone without an apropriate role
        from using any commands in this cog. This does not need to be called.
        """
        return self.researcher_role in [r.id for r in ctx.author.roles]

    @commands.command()
    async def scoopnotification(self, ctx):
        """Sends a notification in the Scoop channel"""
        if ctx.message.channel.id == self.research_channel:
            try:
                await self.bot.get_channel(self.news_channel).send(
                    # TODO: There's a better way I'm just lazy
                    f"<@&{self.news_role}> - a scoop has been posted below."
                )
            except discord.Forbidden as e:
                await ctx.send(f"Failed to send message!\n{e}")
                raise
            await ctx.send("Notified News Junkies in the Scoop channel.")


def setup(bot):
    bot.add_cog(ResearcherRole(bot))
