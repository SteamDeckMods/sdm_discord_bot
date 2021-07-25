import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix=config.prefix)

@bot.event
async def on_ready():
    print("Steam Deck bot operational.")

@bot.command()
async def scoopnotification(ctx):
    if(isResearcher(ctx)) and ctx.message.channel.id == config.research_channel:
        await ctx.send("Notified News Junkies in the Scoop channel.")
        await bot.get_channel(config.scoop_channel).send("<@&" + str(config.newsjunkie_role) + "> - a scoop has been posted below.")

def isHelper(ctx):
    targetrole = discord.utils.get(ctx.message.guild.roles, id=config.helper_role)
    return targetrole in ctx.message.author.roles

def isResearcher(ctx):
    targetrole = discord.utils.get(ctx.message.guild.roles, id=config.researcher_role)
    return targetrole in ctx.message.author.roles
    
bot.run(config.token)