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
            self.trigger_channel = config["Discord"]["Channels"]["TRIGGER"]

        try:
            with open("TriggerPhrases.json", 'r') as trigger_wordfile:
                self.trigger_phrases = json.load(trigger_wordfile)
        except FileNotFoundError:
            print("File for trigger phrases not found")

    async def censorable(self, ctx):
        if ctx.message.guild is None or ctx.message.webhook_id:
            return False
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
                try:
                    response = response.format(mention=msg.author.mention)
                except KeyError:
                    pass
                if response != "":
                    await msg.channel.send(response)
                else:
                    await msg.channel.send("No")

    @commands.Cog.listener(name="on_message")
    async def triger_warnings(self, msg):
        if msg.author == self.bot.user:
            return
        for phrase in self.trigger_phrases:
            if phrase in msg.content.lower():
                await self.bot.get_channel(
                    self.trigger_channel).send(
                    f"<@&{self.helper_role}> be advised, {msg.author.mention} said trigger word \"{phrase}\" in #{msg.channel.mention}."
                )


def setup(bot):
    bot.add_cog(Censor(bot))
