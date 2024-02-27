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


def getNums(power,limit): #description generator for Guess Command
    return ', '.join([f"{i}" for i in range(limit) if i//power%2])

class GuessMenu(discord.ui.View):
    def __init__(self,ctx,limit):
        super().__init__(timeout=60)
        self.ctx=ctx
        self.limit=limit
        self.emb=discord.Embed()
        self.emb.set_author(name=ctx.author,icon_url=ctx.author.display_avatar.url)
    
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def yes(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.emb.title=f"Is your number among these numbers? (1/{int(math.log2(self.limit))+1})"
        self.emb.description=getNums(1,self.limit)
        self.emb.colour=0x2f3136
        self.emb.timestamp=datetime.now()
        await interaction.response.send_message(embed=self.emb,view=GuessGame(self.ctx,1,self.limit))
        self.stop()
    
    @discord.ui.button(label="No",style=discord.ButtonStyle.red)
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        self.emb.title="OK"
        self.emb.description="Cancelling the game"
        self.emb.colour=discord.Colour.red()
        self.emb.timestamp=datetime.now()
        await interaction.response.edit_message(embed=self.emb,view=None)
        self.stop()
    
    async def interaction_check(self, interaction):
        if interaction.user==self.ctx.author: return True
        else: await interaction.response.send_message(embed=discord.Embed(f"{config.error} Only {self.ctx.author.mention} can use that. maybe try using the command yourself?", color={config.red}), ephemeral=True)

    async def on_timeout(self):
        await self.ctx.reply(embed=discord.Embed(description=f"{config.error} The Game has been expired!", color={config.red}))


class GuessGame(discord.ui.View):
    def __init__(self,ctx,power,limit,answer=0):
        super().__init__(timeout=60)
        self.ctx=ctx
        self.power=power
        self.limit=limit
        self.answer=answer

    async def button_response(self,interaction:discord.Interaction,ctx,choice):
        emb=discord.Embed(color=0x2f3136)
        emb.set_author(name=ctx.author,icon_url=ctx.author.display_avatar.url)
        emb.timestamp=datetime.now()
        if choice:self.answer+=self.power
        self.power*=2
        if self.power<=self.limit: #game hasn't been finished
            emb.title=f"Is your number among these numbers? ({int(math.log2(self.power))+1}/{int(math.log2(self.limit))+1})"
            emb.description=getNums(self.power,self.limit)
            emb.colour=0x2f3136
            await interaction.response.edit_message(embed=emb)
        else:
            if self.answer<=self.limit: #gamee has finished with an expected answer
                emb.title="Your Number is"
                emb.description=f"{self.answer}"
            else: #game has finished with an unexpected answer
                emb.title="Play the game seriously !"
            emb.colour=discord.Colour.green()
            await interaction.response.send_message(embed=emb)
            self.stop()
        
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def yes(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.button_response(interaction,self.ctx,1)
    
    @discord.ui.button(label="No",style=discord.ButtonStyle.red)
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.button_response(interaction,self.ctx,0)

    async def interaction_check(self, interaction):
        if interaction.user==self.ctx.author: return True
        else: await interaction.response.send_message(embed=discord.Embed(description=f"{config.error} Only {self.ctx.author.mention} can use that. maybe try using the command yourself?",color={config.red}), ephemeral=True)

    async def on_timeout(self):
        await self.ctx.reply(embed=discord.Embed(description=f"{config.error} The Game has been expired!", color={config.red}))


class RPSMenu(discord.ui.View):
    def __init__(self,ctx,opponent):
        super().__init__(timeout=60)
        self.ctx=ctx
        self.opponent=opponent
    
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def yes(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message(f"Make Your Choice {self.ctx.author.mention} {self.opponent.mention}",view=RPSGame(self.ctx,self.opponent,[None,None]))
        self.stop()
    
    @discord.ui.button(label="No",style=discord.ButtonStyle.red)
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(description=f"{config.error} User Cancelled!", color={config.red}))
        self.stop()

    async def interaction_check(self, interaction):
        if interaction.user==self.opponent: return True
        else: await interaction.response.send_message(embed=discord.Embed(description=f"{config.error} Only {self.opponent.mention} can respond", color={config.red}), ephemeral=True)

    async def on_timeout(self):
        await self.ctx.reply(content=f"{self.opponent.mention}", embed=discord.Embed(description=f"{config.error} Took too long to respond. Bye Bye !", color={config.red}))


class RPSGame(discord.ui.View):
    def __init__(self,ctx,opponent:discord.Member,selection=[None,None]):
        super().__init__(timeout=60)
        self.ctx=ctx
        self.opponent=opponent
        self.selection=selection
    
    async def button_response(self,interaction,choice):
        if interaction.user == self.ctx.author: self.selection[0]=choice
        elif interaction.user == self.opponent: self.selection[1]=choice
        else:
            print("Error")
        if self.selection[0] and self.selection[1]:
            choices=('None','Rock','Paper','Scissors')
            await interaction.response.edit_message(content=f"""The Game has Concluded
{self.ctx.author.mention} chose `{choices[self.selection[0]]}`    
{self.opponent.mention} chose `{choices[self.selection[1]]}`
**The Winner is** {"Nobody" if self.selection[0]==self.selection[1] else self.ctx.author.mention if self.selection[0]==(self.selection[1])%3+1 else self.opponent.mention}""",view=None)
            self.stop()
        else:
            await interaction.response.edit_message(content=f"Make Your Choice {self.ctx.author.mention} {self.opponent.mention}"
            +''.join([f"\n{[self.ctx.author.mention,self.opponent.mention][i]} has made a choice." 
                      for i in range(2) if self.selection[i]]))

    @discord.ui.button(label="Rock",emoji='🪨')
    async def rock(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.button_response(interaction,1)
    
    @discord.ui.button(label="Paper",emoji='📄')
    async def paper(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.button_response(interaction,2)

    @discord.ui.button(label="Scissors",emoji='✂️')
    async def scissors(self,interaction:discord.Interaction,button:discord.ui.Button):
        await self.button_response(interaction,3)

    async def interaction_check(self, interaction):
        if interaction.user in (self.ctx.author,self.opponent): return True
        else: await interaction.response.send_message(embed=discord.Embed(description=f"{config.cross} Only {self.ctx.author.mention} and {self.opponent.mention} can use that. maybe try using the command yourself?", color={config.red}), ephemeral=True)

    async def on_timeout(self):
        await self.ctx.reply(embed=discord.Embed(description=f"{config.error} The Game has been expired!", color={config.red}))

class TicTacToeMenu(discord.ui.View):
    def __init__(self,ctx,opponent:discord.Member):
        super().__init__(timeout=60)
        self.ctx=ctx
        self.opponent=opponent
    
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def yes(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message(f"Its your turn {self.ctx.author.mention}",view=TicTacToeGame(self.ctx,self.opponent))
        self.stop()

    @discord.ui.button(label="No",style=discord.ButtonStyle.red)
    async def no(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(description=f"{config.error} User Cancelled!", color=0xe61111))
        self.stop()

    async def interaction_check(self, interaction):
        if interaction.user==self.opponent: return True
        else: await interaction.response.send_message(embed=discord.Embed(description=f"{config.cross} Only {self.opponent.mention} can use that. maybe try using the command yourself?", color={config.red}), ephemeral=True)

    async def on_timeout(self):
        await self.ctx.reply(embed=discord.Embed(description=f"{config.error} {self.opponent.mention} took too long to respond!", color={config.red}))

def TTTWinner(selection:list[int],author,opponent): 
    checks=(
        ([0,1,2],3), #vertical check
        ([0,3,6],1), #horizontal check
        ([0],4), # \ diagonal  check 
        ([2],2), # / diagonal check 
    ) # for each item in checks, the list in the 0 position contains the starting positions and the number in 1 position is the increment value
    for check in checks:
        for start in check[0]:
            if selection[start] == selection[start+check[1]] == selection[start+2*check[1]] and selection[start]:
                return (author,opponent)[selection[start]-1]
    if 0 in selection:
        return False
    return "Nobody"

class TTTButton(discord.ui.Button):
    def __init__(self,pos,selection,author,opponent):
        super().__init__(label='ㅤ',row=pos//3)
        self.author=author
        self.opponent=opponent
        self.disabled=False
        self.pos=pos
        self.selection=selection
    
    async def callback(self,interaction):
        assert self.view is not None
        view=self.view
        if view.selection[self.pos]==0:
            view.selection[self.pos]=view.turn+1
            self.label=('O','X')[view.turn]
            self.style=[discord.ButtonStyle.danger,discord.ButtonStyle.primary][view.turn]
            winner= TTTWinner(self.selection,self.author.mention,self.opponent.mention)
            if winner:
                await interaction.response.edit_message(content=f":tada: {winner} :tada:", embed=discord.EMbed(description=f":first_place: Wins the game !", color={config.color}),view=None)
                view.stop()
            else:
                view.turn=not view.turn
                await interaction.response.edit_message(content=f"Its your turn {(self.author.mention,self.opponent.mention)[self.view.turn]}",view=self.view)
        else:
            await interaction.response.send_message(embed=discord.Embed(description=f"{config.cross} That block is already occupied", color=0xe61111), ephemeral=True)


class TicTacToeGame(discord.ui.View):
    def __init__(self, ctx, opponent):
        super().__init__(timeout=60)
        self.ctx=ctx
        self.opponent=opponent
        self.selection=[0,0,0,0,0,0,0,0,0]
        self.turn=0

        for pos in range(9):
            button=TTTButton(pos,self.selection,ctx.author,opponent)
            self.add_item(button)

    async def interaction_check(self, interaction):
        if interaction.user == (self.ctx.author,self.opponent)[self.turn]: return True
        elif interaction.user == (self.ctx.author,self.opponent)[not self.turn]: 
            await interaction.response.send_message(f"Its not your turn",ephemeral=True)
        else: await interaction.response.send_message(embed=discord.Embed(description=f"{config.cross} Only {self.ctx.author.mention} and {self.opponent.mention} can use that. maybe try using the command yourself?", color={config.red}), ephemeral=True)

    async def on_timeout(self):
        await self.ctx.reply(embed=discord.Embed(description=f"{config.error} The Game has been expired!", color={config.red}))


async def is_valid_opponent(ctx,opponent):
    "Play TicTacToe with your Friends (if you have some)"
    if opponent==None: await ctx.reply(embed=discord.Embed(description=f"{config.cross} You must include an **Opponent** !!", color={config.red}).set_image(url="https://i.imgflip.com/6k6afr.jpg"))
    elif opponent.bot: await ctx.reply(embed=discord.Embed(description=f"{config.cross} Bots do not count as an **Opponent** !!", color=0xe61111).set_image(url="https://i.imgflip.com/6k6afr.jpg"))
    elif ctx.author==opponent: await ctx.reply(embed=discord.Embed(description=f" {config.cross} You can't play with **yourself** in this game !!", color={config.red}).set_image(url="https://i.imgflip.com/6k6afr.jpg"))
    else: return True




class Games(commands.Cog):
    """Some Games you can play with me or your Friends (Hopefully).
Most of the Games require me having permissions to Embed Links soo play these Games where they are supposed to."""
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(aliases=['ttt'], help="Play tictactoe and have fun", with_app_command=True)
    @commands.bot_has_permissions(send_messages=True)
    async def tictactoe(self,ctx,opponent:discord.Member|None):
        """Play Tic Tac Toe with your Friends (if you have some)"
        
        Parameters
        ----------
        Opponent : str, optional
            A Server Member."""
        if not await is_valid_opponent(ctx,opponent): return
        assert opponent is not None
        await ctx.send(content=f"{opponent.mention}", embed=discord.Embed(description=f"Do u want to play **Tic Tac Toe** against {ctx.author.mention} ?", color=0x2f3136),view=TicTacToeMenu(ctx,opponent))

    @commands.hybrid_command(aliases=['rps'], help="Play rock-paper-scissors.", with_app_command=True)
    @commands.bot_has_permissions(send_messages=True)
    async def rockpaperscissors(self,ctx,opponent:discord.Member|None):
        """Play Rock Paper Scissors with your Friends (if you have some)
        Parameters
        ----------
        Opponent : str, optional
            A Server Member."""
        if not await is_valid_opponent(ctx,opponent): return
        assert opponent is not None    
        await ctx.send(content=f"{opponent.mention}", embed=discord.Embed(description=f"Do u want to play **Rock Paper Scissors** against {ctx.author.mention} ?", color=0x2f3136),view=RPSMenu(ctx,opponent))

    @commands.hybrid_command()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def guess(self,ctx,limit:int=99):
        """A Single-Player Game where I try to guess your Number."""
        emb=discord.Embed(
            colour=0x2f3136,
            title=f"Welcome to guess the number.",
            description=f"""
In this game, The goal is for me to guess your secret number.

The rules are quite simple:
> 1. Your number must be a natural number lower than {limit}. the bigger, the better (TWSS). 
> 2. I will present you with a total of {int(math.log2(limit))+1} lists of numbers.
> 3. in each list, if your number is in a group. click Yes. if not, click No.

Do you want to start the game?"""
        )
        emb.set_author(name=ctx.author,icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=emb,view=GuessMenu(ctx,limit))

        
async def setup(bot):
    await bot.add_cog(Games(bot))
    print("Games Cog Loaded")

async def teardown(bot):
    print("Games Cog Unoaded")