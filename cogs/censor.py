from discord.ext import commands
import json


class Censor(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("Censor.json", 'r') as config_file:
            self.censored = json.load(config_file)

        with open("config.json", 'r') as config_file:
            config = json.load(config_file)
            self.helper_role = config["Discord"]["Roles"]["HELPER"]

    async def censorable(self, ctx):
        return self.helper_role not in [r.id for r in ctx.author.roles]

    @commands.Cog.listener(name="on_message")
    async def censor(self, msg):
        # Since this is on_message put the check here instead of a cog_check
        if not await self.censorable(msg):
            return
        checking = msg.content
        for word in self.censored:
            if word in checking:
                await msg.delete()
                response = self.censored[word]
                if response != "":
                    await msg.channel.send(response)
                else:
                    await msg.channel.send("No")


def setup(bot):
    bot.add_cog(Censor(bot))
