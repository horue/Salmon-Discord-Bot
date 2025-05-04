import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from discord import Interaction

## Test Commands ##

async def testing(who):
    match who:
        case Interaction():
            await who.response.send_message("Testing!")
        case Context():
            await who.send("Testing!")

async def pong(who):
    match who:
        case Interaction():
            await who.response.send_message("pong!")
        case Context():
            await who.send("pong!")