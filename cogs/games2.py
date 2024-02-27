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
import discord_games as games
from discord_games import button_games as btn

import config

class Games2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twenty_48_emojis = {
            "0": "<:grey:821404552783855658>",
            "2": "<:twoo:821396924619161650>",
            "4": "<:fourr:821396936870723602>",
            "8": "<:eightt:821396947029983302>",
            "16": "<:sixteen:821396959616958534>",
            "32": "<:thirtytwo:821396969632169994>",
            "64": "<:sixtyfour:821396982869524563>",
            "128": "<:onetwentyeight:821396997776998472>",
            "256": "<:256:821397009394827306>",
            "512": "<:512:821397040247865384>",
            "1024": "<:1024:821397097453846538>",
            "2048": "<:2048:821397123160342558>",
            "4096": "<:4096:821397135043067915>",
            "8192": "<:8192:821397156127965274>",
        }


    @commands.hybrid_command(name="akinator", aliases=["aki"], help="Play a guess game with akinator !")
    async def akinator(self, ctx):
        game = btn.BetaAkinator()
        await game.start(ctx, timeout=None)



    @commands.hybrid_command(name="hangman", help="Play hangman game !")
    async def hangman(self, ctx):
        game = games.Hangman()
        await game.start(ctx, delete_after_guess=True)



    @commands.hybrid_command(name="chess", help="Play a chess with a member !")
    async def chess(self, ctx, member: discord.Member):
        game = games.Chess(
            white=ctx.author,
            black=member,
        )
        await game.start(ctx, timeout=60, add_reaction_after_move=True)



    @commands.hybrid_command(name="typeracce", help="Play a typerace game with you friends !")
    async def typerace(self, ctx):
        game = games.TypeRacer()
        await game.start(ctx, timeout=30)


    @commands.hybrid_command(name="memory-game", aliases=["memorygame"], help="Check how long you can store your memroy by playing memory game !")
    async def memory_game(self, ctx):
        game = btn.MemoryGame()
        await game.start(ctx)



    @commands.hybrid_command(name="wordle", help="Play wordle game !")
    async def wordle(self, ctx):
        game = btn.BetaWordle()
        await game.start(ctx)



async def setup(bot):
    await bot.add_cog(Games2(bot))