
import os
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
import requests, random, datetime, time, sys
import jishaku
from typing import Optional
import sqlite3
import aiohttp, threading, logging


os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;129m[\x1b[0m%(asctime)s\x1b[38;5;129m]\x1b[0m -> \x1b[38;5;129m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",)



class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            sync_commands=True,
            shard_count=1,
            case_insensitive=True,
            command_prefix="+",
            intents=discord.Intents.all()
        )
        owner_ids = [1020693089851027457]
        self.owner_ids = owner_ids
        self.remove_command('help')
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        self.session = aiohttp.ClientSession()

    def dbms(self):
        dbt = threading.Thread(target=self.database_connect)
        dbt.start()
        dbt.join()

    def database_connect(self):
        with sqlite3.connect('db/database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS data (userid INTEGER, username TEXT)''')
        logging.info("Sucessfully Loaded Database (SQLITE3)")

    async def on_ready(self) -> None:
        logging.info(f"Successfully {(self.user.display_name)} is Loaded.")
        logging.info("All The Systems Are Ready.")

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        logging.info(f"Successfully Loaded Jishaku.")
        self.dbms()
        for filename in os.listdir('./cogs'):
            try:
                if filename.endswith('.py') and filename not in ['__init__.py']:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logging.info(f'Sucessfully Loaded Cog: `{filename[:-3]}`')
            except Exception as e:
                logging.info(e)




    async def on_guild_join(self, guild: discord.Guild) -> None:
        o = guild.owner_id
        us = self.get_user(o)
        img = "https://images-ext-2.discordapp.net/external/MyPLM_ynvL-XB3ixc25NpeUB6kfPGx8n11wlzIJI7eE/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1127538536804007996/91d0b5f75d0e4f3f096a8c5898c0081a.png?format=webp&quality=lossless&width=479&height=479"
        if us:
            e = discord.Embed(
                color=0x2e2e2e,
                description=f"Thanks for adding me to **{guild.name}**\n> My default prefix is `.`\n> Feel free to join our [support server](https://discord.gg/demonhq) for any help or support you need."
            )
            e.set_author(name=guild.owner.display_name, icon_url=guild.owner.avatar)
            e.set_thumbnail(url=guild.icon)
            e.set_footer(text=f"Thanks For Choosing GameX", icon_url=img)
            await us.send(embed=e)
        else:
            logging.info("Problem In Bot.py GuildJoin Event.")