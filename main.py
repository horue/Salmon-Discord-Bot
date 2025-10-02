import os
import discord
import datetime
import re
from discord.ext import commands
from discord import app_commands
from modules.firebase import link as firebase
from keys.tokens import bot_token
from modules.economy import *
from modules.general import *
from assets.colors import *
from modules.guide import *


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


def is_admin_or_has_role(role_name: str) -> str:
    async def predicate(ctx):
        is_admin = ctx.author.guild_permissions.administrator
        has_role = discord.utils.get(ctx.author.roles, name=role_name) is not None
        return is_admin or has_role
    return commands.check(predicate)

## Bot Connection ##


@bot.event
async def on_ready() -> None:
  now = datetime.datetime.now()
  formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
  await tree.sync()
  print(f'{GREY}{formatted_datetime}{RESET} {BLUE}{'INFO'}{RESET}     {GREEN}Success: {RESET}' + 'logged in with '+'{0.user}' . format(bot))



## Guide Functions ##
@bot.command()
async def guide(ctx='guide') -> None:
  content = await(Guide.starting())
  embed = discord.Embed(
            title=content[0],
            description=content[1],
            color=discord.Color.blurple()
        )
  await ctx.send(embed=embed)   






## Economy Functions ##


@bot.command()
async def wallet(ctx, target='') -> None:
  if target == '':
    u_id = ctx.message.author.id
  else:
    u_id = re.search(r'<@(\d+)>', target)
    u_id = u_id.group(1)
    print(target)
  s_id = ctx.message.guild.id
  await check_money(ctx=ctx, server_id=s_id, user_id=u_id)


@bot.command()
@is_admin_or_has_role("Bank Manager")
async def add(ctx, target='', value=0) -> None:
  if value == 0:
    await ctx.send("You can't add 0.")
    return
  if target == '':
    u_id = ctx.message.author.id
  else:
      match = re.search(r'<?@(\d+)>?', target)
      if match:
          u_id = int(match.group(1))
          print(target)
  s_id = ctx.message.guild.id
  await add_money(ctx=ctx, server_id=s_id, user_id=u_id, amount=value)


## Testing Functions ##


@tree.command(name='test', description="This is a test command.")
async def teste(interaction: discord.Interaction) -> None:
  await Test.testing(interaction)


@bot.command()
async def test(ctx='test') -> None:
  await Test.testing(ctx)



@tree.command(name='ping', description="This is the ping pong test!.")
async def teste(interaction: discord.Interaction) -> None:
  await Test.pong(interaction)


@bot.command()
async def ping(ctx='ping') -> None:
  await Test.pong(ctx)



## Error Handling ##

@bot.event
async def on_command_error(ctx, error) -> None :
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title="❌ Permission Error",
            description=f"You must be an admin or have the 'Bank Manager' role to use this command.",
            color=discord.Color.red()
        )
        
        message = await ctx.send(embed=embed)        
        await message.delete(delay=10)

def run_bot():
  os.system('cls')
  bot.run(bot_token)

run_bot()