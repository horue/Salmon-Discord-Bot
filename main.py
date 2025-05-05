import os
import discord
import datetime
from discord.ext import commands
from discord import app_commands
from modules.firebase import link as firebase
from keys.tokens import bot_token
from modules.economy import *
from modules.general import *
from assets.colors import *


## Bot configuration ##

intents = discord.Intents.default()
intents = discord.Intents.all()
bot = commands.Bot(
  command_prefix = 's!', 
  case_insensitive = True, 
  activity=discord.CustomActivity(name="Use s! for the commands"), 
  status=discord.Status.online, 
  intents=intents)
tree = bot.tree


## Bot Connection ##


@bot.event
async def on_ready():
  now = datetime.datetime.now()
  formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
  await tree.sync()
  print(f'{GREY}{formatted_datetime}{RESET} {BLUE}{'INFO'}{RESET}     {GREEN}Success: {RESET}' + 'logged in with '+'{0.user}' . format(bot))


## Economy Functions ##


@bot.command()
async def wallet(ctx):
  s_id = ctx.message.guild.id
  u_id = ctx.message.author.id
  await check_money(ctx=ctx, server_id=s_id, user_id=u_id)




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


def run_bot():
  os.system('cls')
  bot.run(bot_token)

run_bot()