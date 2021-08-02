import datetime
from discord.ext import commands
import json
import discord


class ResearcherRole(commands.Cog):
    """Manages all commands associated with the Researcher Role"""

    def __init__(self, bot):
        self.bot = bot
        self.DELAY = datetime.timedelta(hours=1)
        self.last_scoop = datetime.datetime.now() - self.DELAY
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)

            # Load Relevant Roles
            self.newsjunkie_role = config["Discord"]["Roles"]["NEWSJUNKIE"]
            self.researcher_role = config["Discord"]["Roles"]["RESEARCHER"]

            # Load Relevant Channels
            self.scoop_channel = config["Discord"]["Channels"]["SCOOP"]
            self.research_channel = config["Discord"]["Channels"]["RESEARCH"]

    async def cog_check(self, ctx):
        """
        Precheck that prevents anyone without an appropriate role
        from using any commands in this cog. This does not need to be called.
        """
        return self.researcher_role in [r.id for r in ctx.author.roles]

    @commands.command()
    async def scoopnotification(self, ctx):
        """
        Sends a notification in the Scoop channel
        Has a delay associated with it.
        """
        scoop_wait = self.last_scoop + self.DELAY
        if ctx.message.channel.id == self.research_channel and scoop_wait > datetime.datetime.now():
            await ctx.send(f"Can't notify news junkies this soon after the last one. Please wait {(scoop_wait - datetime.datetime.now()).total_seconds()//60:.0f} minutes then try again.")
            return
        if ctx.message.channel.id == self.research_channel:
            try:
                await self.bot.get_channel(self.scoop_channel).send(
                    # TODO: There's a better way I'm just lazy
                    f"<@&{self.newsjunkie_role}> - a new scoop is here!"
                )
            except discord.Forbidden as e:
                await ctx.send(f"Failed to send notification to News Junkie.\n{e}")
                raise
            await ctx.send("Notified News Junkies in the scoop channel.")
            self.last_scoop = datetime.datetime.now()


def setup(bot):
    bot.add_cog(ResearcherRole(bot))
