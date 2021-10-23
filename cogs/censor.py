from discord.ext import commands
from discord import Embed
import json
import re  # regex


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
            # TODO name these regex patterns, so it's obvious that e.g. "a$$h0le" warn is from "a.{0,2}\s*h[0o]le" pattern
            self.trigger_regexes = [re.compile(phrase, flags=re.I | re.M) for phrase in self.trigger_phrases]
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
        # search for phrase matches
        triggered_phrases = []
        for pattern in self.trigger_regexes:
            match = pattern.search(msg.content)
            if match is not None:
                triggered_phrases.append(match.group(0))
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
            # content max length is 2000, while description max is 4096 chars so this limit should never be hit

            await self.bot.get_channel(self.trigger_channel).send(
                content = content,
                embed = embed
            )

def setup(bot):
    bot.add_cog(Censor(bot))
