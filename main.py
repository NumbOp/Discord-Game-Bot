import discord
from core.bot import Bot
import config

bot = Bot()

bot.run(config.token)