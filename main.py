import discord
from discord.ext import commands
from discord import app_commands
from tokens import bot_token
from modules.general import *



## Bot Connection ##


intents = discord.Intents.default()
intents = discord.Intents.all()
bot = commands.Bot(
  command_prefix = 's!', 
  case_insensitive = True, 
  activity=discord.CustomActivity(name="Use s! for the commands"), 
  status=discord.Status.online, 
  intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
  await tree.sync()
  print('Entramos como {0.user}' . format(bot))



## Testing Functions ##


@tree.command(name='test', description="This is a test command.")
async def teste(interaction: discord.Interaction):
  await testing(interaction)


@bot.command()
async def test(ctx='test'):
  await testing(ctx)



@tree.command(name='ping', description="This is the ping pong test!.")
async def teste(interaction: discord.Interaction):
  await pong(interaction)


@bot.command()
async def ping(ctx='ping'):
  await pong(ctx)


bot.run(bot_token)