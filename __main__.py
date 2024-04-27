import json
import logging
import logging.handlers
from pathlib import Path
from random import choice

import discord
from discord.ext import commands, tasks
from discord.utils import _ColourFormatter

from cmds import debug
from cmds import gencom
#from cmds import gamestats
from cmds import fun

class BunnyBot(commands.Bot):# pylint: disable=missing-class-docstring
    def __init__(self, cfg:dict[str,any], statuses:list[str]=None, changelog:str=None, **args):
        self.version = ("WC-2.4.0", "Waxing Crescent-2.4.0")
        self.cfg = cfg
        self.statuses = statuses or ["Hi there"]
        self.changelog = changelog
        self.logger = logging.getLogger('bunnybot')
        super().__init__(**args)

    async def on_message(self, message:discord.Message): # pylint: disable=arguments-differ
        if message.author == bot.user:
            return
        if "https://twitter.com" in message.content:
            await message.channel.send("message originally from message.author.mention:\n" +
                    message.content.replace("https://twitter.com/","https://fxtwitter.com/"),
                    silent=True)
            await message.delete()
        if "https://x.com/" in message.content:
            await message.channel.send("message originally from message.author.mention:\n" +
                    message.content.replace("https://x.com/","https://fxtwitter.com/"),
                    silent=True)
            await message.delete()

    async def on_ready(self):
        await self.add_cog(debug.Debug(bot), guild=GUILD)
        await self.add_cog(gencom.General(bot), guild=GUILD)
        #async self.add_cog(gamestats.gstats(bot), guild=GUILD)
        await self.add_cog(fun.Fun(bot), guild=GUILD)
        await self.tree.sync(guild=GUILD)
        self.status_changer.start() # pylint: disable=no-member
        self.logger.log(logging.INFO, "Bunnybot loaded! %s %s Version: %s",
                        bot.user.name, bot.user.id, bot.version[1])


    @tasks.loop(minutes=2)
    async def status_changer(self):
        await self.change_presence(activity=discord.CustomActivity(
            choice(self.statuses).format(bot=self)
            ))

#setting intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

#Sets up variables
with open(Path(__file__).parent / 'data' / 'config.json', encoding='utf-8') as f:
    config =json.load(f)
TOKEN = config.pop('token')
GUILD = discord.Object(config['guild_id'])

#load statuses
with open(Path(__file__).parent / 'data' / 'statuses.txt', encoding='utf-8') as f:
    STATUSES = f.readlines()

#load changelog TODO: improve this later if changelog becomes too large
with open(Path(__file__).parent / 'data' / 'changelog.txt', 'r', encoding='utf-8') as f:
    CHANGELOG = f.read()

#setup logging, add file handler
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(_ColourFormatter())

filehandler = logging.handlers.RotatingFileHandler(
    filename='logs/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}',
                              '%Y-%m-%d %H:%M:%S', style='{')
filehandler.setFormatter(formatter)

bunnybot_logger = logging.getLogger('bunnybot')
bunnybot_logger.setLevel(logging.DEBUG)
bunnybot_logger.addHandler(filehandler)
bunnybot_logger.addHandler(streamhandler)

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_logger.addHandler(filehandler)
discord_logger.addHandler(streamhandler)

bot = BunnyBot(config, STATUSES, CHANGELOG, command_prefix="bb ", intents=intents)
if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
