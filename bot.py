from discord.ext import commands
import json

# Load json config file from working dir
with open('config.json') as c:
    conf = json.load(c)

bot = commands.Bot(command_prefix=conf["Discord"]["COMMAND_PREFIX"])

# Individual "Modules" that can be loaded/reloaded.
# Keeps things segregated and hopefully more sensible
# Format for a cog is folder.file_name
cogs = [
    'cogs.helper_role',
    'cogs.researcher_role'
]


@bot.event
async def on_ready():
    print("Steam Deck bot operational!")


if __name__ == '__main__':
    for extension in cogs:
        bot.load_extension(extension)
    bot.run(conf["Discord"]["API_KEY"])
