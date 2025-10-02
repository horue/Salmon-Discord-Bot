import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from discord import Interaction

## Guide Functions ##


class Guide:
    async def starting() -> list:
        introduction: str = "This is a guide on how to use the bot. Here you will find on how to use the basics and how to interact with the bot."
        first_steps: str = "First of all, by using Salmoney, you must know that all your data, such as discord user id and server id, will be stored on a FireBase server."
        guide_list: list = [introduction, first_steps]
        return guide_list

    async def pong(who) -> None:
        match who:
            case Interaction():
                await who.response.send_message("pong!")
            case Context():
                await who.send("pong!")