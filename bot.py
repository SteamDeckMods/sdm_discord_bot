import discord
from discord.ext import commands
import config

client = commands.Bot(command_prefix=config.prefix)

@client.event
async def on_ready():
    print("Steam Discord bot operational.")

@client.command()
async def hello(ctx):
    await ctx.send("Howdy")
    
client.run(config.token)