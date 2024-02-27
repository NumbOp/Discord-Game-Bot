import discord
import asyncio, datetime, time, re
import typing
import typing as t
from typing import *
from core.bot import Bot
from discord.ext.commands import Converter
from discord.ext import commands
from discord.ui import Button, View
from io import BytesIO
import requests, aiohttp, psutil, sys
from datetime import datetime
from discord import app_commands
import math
import random

import config

img = "https://images-ext-1.discordapp.net/external/ym5AhmkbE3f86UT6bcCla0PFxrLv6XR9ydTMvK4b9Sc/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/1127538536804007996/91d0b5f75d0e4f3f096a8c5898c0081a.png?format=webp&quality=lossless&width=479&height=479"

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(embed=discord.Embed(description=f"You Can`t Use This Command. Use .**afk** To Run This Command", color=0x2f3136),ephemeral=True)
            return False
        elif interaction.user.id == "246469891761111051":
            return False
        return True



class HelpView(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=None)
        self.value = None

    @discord.ui.button(label="Prefix Commands", custom_id='prefix', style=discord.ButtonStyle.green)
    async def prefix(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed1 = discord.Embed(
            color=0x2f3136
        )
        embed1.add_field(name="**__General Commands__**",value="```+help, +ping, +stats, +botinfo```", inline=False)
        embed1.add_field(name="**__Games Commands__**", value="```+tictactoe, +rockpaperscissor, +guess, +akinator, +wordle, +typerace, +memory-game, +chess, +hangman```", inline=False)
        embed1.set_thumbnail(url=img)
        embed1.set_author(name="Astro™", icon_url=img)
        self.value = 'Prefix'
        await interaction.response.send_message(embed=embed1, ephemeral=True)
        await interaction.response.defer()

    @discord.ui.button(label="Slash Commands", custom_id='slash', style=discord.ButtonStyle.red)
    async def slash(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed2 = discord.Embed(
            color=0x2f3136
        )
        embed2.add_field(name="**__General Commands__**",value="```/help, /ping, /stats, /botinfo```", inline=False)
        embed2.add_field(name="**__Games Commands__**", value="```/tictactoe, /rockpaperscissor, /guess, /akinator, /wordle, /typerace, /memory-game, /chess, /hangman```", inline=False)
        embed2.set_thumbnail(url=img)
        embed2.set_author(name="Astro™", icon_url=img)
        self.value = 'Slash'
        await interaction.response.send_message(embed=embed2, ephemeral=True)
        await interaction.response.defer()




class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = 0x2e2e2e


    @commands.hybrid_command(name="help", help="Get a list of commands !", aliases=['h'])
    async def help(self, ctx):
        view = HelpView(ctx)
        embed = discord.Embed(color=self.color,
                              description=f"**:wave: Heya {ctx.author.mention} !\n> Use the buttons below to check all my prefix & slash commands !**")
        lol = await ctx.send(embed=embed, view=view)
        #await view.wait()
       # if view.value == "Prefix":
           # await lol.edit(embed=embed1)

        #if view.value == "Slash":
          #  await lol.edit(embed=embed2)





async def setup(bot):
    await bot.add_cog(Help(bot))
    print("Help Cog Loaded")