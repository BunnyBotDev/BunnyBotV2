import json
import glob
import asyncio
import logging
import logging.handlers
from pathlib import Path
from random import choice
from typing import Union

import discord
from discord.ext import commands, tasks
from discord.utils import _ColourFormatter

# from cogs import debug
# from cogs import general
# #from cogs import gamestats
# from cogs import fun

class BunnyBot(commands.Bot):# pylint: disable=missing-class-docstring
    def __init__(self, cfg:dict[str,any], statuses:list[str]=None, changelog:str=None, **args):
        self.version = ("WC-2.5.0", "Waxing Crescent-2.5.0")
        self.cfg = cfg
        self.guild = discord.Object(cfg['guild_id'])
        self.statuses = statuses or ["Hi there"]
        self.changelog = changelog
        self.logger = logging.getLogger('bunnybot')
        super().__init__(**args)


    def load_data(self, filename: str):
        """helper function to load data for a module, returns None if data doesn't exist or fails to load."""
        try:
            with open(Path(__file__).parent / 'data' / (filename + '.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError: #silence filenotfound, handle this in the module to default values.
            return None
        except OSError as e:
            self.logger.error("Failed to open data file '%s': \n %s", filename, e)
            return None

    def save_data(self, filename: str, data: Union[dict, list]):
        """helper function to save data for a module, returns True if succeeded and False if it failed."""
        try:
            with open(Path(__file__).parent / 'data' / (filename + '.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f)
                return True
        except OSError:
            self.logger.error("Failed to write data file '%s':", filename, exc_info=True)
            return False

    async def on_message(self, message:discord.Message): # pylint: disable=arguments-differ
        if message.author.bot:
            return
        if "https://twitter.com" in message.content:
            await message.channel.send(f"message originally from {message.author.mention}:\n" +
                    message.content.replace("https://twitter.com/","https://fxtwitter.com/"),
                    silent=True)
            await message.delete()
        if "https://x.com/" in message.content:
            await message.channel.send(f"message originally from {message.author.mention}:\n" +
                    message.content.replace("https://x.com/","https://fxtwitter.com/"),
                    silent=True)
            await message.delete()

    async def on_ready(self):
        tg = asyncio.TaskGroup()
        async with tg: #schedule all the extensions to load at once.
            for i in glob.glob("cogs/*.py"):
                tg.create_task(self.load_extension(i.replace('\\', '.')[:-3]))

        await self.tree.sync(guild=self.guild)

        self.logger.log(logging.INFO, "Bunnybot loaded! %s %s Version: %s",
                        self.user.name, self.user.id, self.version[1])
        self.status_changer.start() # pylint: disable=no-member


    @tasks.loop(minutes=2)
    async def status_changer(self):
        await self.change_presence(activity=discord.CustomActivity(
            choice(self.statuses).format(bot=self)
            ))

def main():
    #setting intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True

    #Sets up variables
    with open(Path(__file__).parent / 'data' / 'config.json', encoding='utf-8') as f:
        config =json.load(f)
        TOKEN = config.pop('token')

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

    bot.run(TOKEN, log_handler=None)

if __name__ == "__main__":
    main()
