from discord.ext import commands
from discord import Embed
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
        if ctx.channel.guild is None or ctx.webhook_id is not None:
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
    async def trigger_warnings(self, msg):
        if msg.author == self.bot.user or not await self.censorable(msg):
            return
        triggered_phrases = []
        for phrase in self.trigger_phrases:
            if phrase in msg.content.lower():
                triggered_phrases.append(phrase)
        if len(triggered_phrases) != 0:
            # link to message
            msg_link = f"https://discord.com/channels/{msg.channel.guild.id}/{msg.channel.id}/{msg.id}"
            # quote and command-separated str of phrases
            phrases = "\"" + "\", \"".join(triggered_phrases) + "\""
            # message text
            content = f"<@&{self.helper_role}> be advised, {msg.author.mention} said trigger word(s) {phrases} in {msg.channel.mention}."
            # build embed to send
            embed = Embed(description = msg.content, colour=0x000000)\
                .set_author(name="Message", url=msg_link)

            await self.bot.get_channel(self.trigger_channel).send(
                content = content,
                embed = embed
            )

def setup(bot):
    bot.add_cog(Censor(bot))
