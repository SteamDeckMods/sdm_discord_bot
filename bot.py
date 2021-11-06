from discord.ext import commands
import json

# Load json config file from working dir
with open('config.json') as c:
    conf = json.load(c)
    try:
        bot_Dev_role = conf["Discord"]["Roles"]["BOT_DEV"]
    except ValueError:
        pass  # We don't care if this doesn't exist.
bot = commands.Bot(command_prefix=conf["Discord"]["COMMAND_PREFIX"])

# Individual "Modules" that can be loaded/reloaded.
# Keeps things segregated and hopefully more sensible
# Format for a cog is folder.file_name
cogs = [
    'cogs.helper_role',
    'cogs.researcher_role',
    'cogs.censor',
    'cogs.giveaways',
]


@bot.command()
async def reload(ctx):
    """Development Command to reload extensions for texting"""
    if bot_Dev_role not in [r.id for r in ctx.author.roles]:
        return
    await ctx.send("Module reloaded successfully.")
    try:
        bot.reload_extension(ctx.message.content.split(" ")[1])
    except commands.ExtensionNotFound:
        await ctx.send("Couldn't find extension.")
    except commands.ExtensionFailed as e:
        await ctx.send(f"Extension failed to load. Error:\n{e}")
        raise
    except commands.ExtensionNotLoaded as e:
        await ctx.send(f"Extension was not loaded to begin with. Error:\n{e}")
        raise


@bot.event
async def on_ready():
    print("Steam Deck Bot online.")


if __name__ == '__main__':
    for extension in cogs:
        bot.load_extension(extension)
    bot.run(conf["Discord"]["API_KEY"])
