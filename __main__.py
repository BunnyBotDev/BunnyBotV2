import discord
from discord.ext import commands
import os
import time
import json
from dotenv import load_dotenv
import cmds.debug as debug
import cmds.gencom as gencom

#Sets up variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD = discord.Object(os.getenv("GUILD"))

#Json Loading
with open('variables.json') as var_file:
#Json variables
    pjson = json.load(var_file)
VSHORT = pjson['VSHORT']
VLONG = pjson['VLONG']


#custom activity
activity = discord.CustomActivity(
    name = f"Your bunny maid is on firmware version: {VSHORT}",
)


# using discord.Activity
activity = discord.Activity(
   type = discord.ActivityType.custom,
   name = "Custom Status",  # does nothing but is required
   state = f"Your bunny maid is on firmware version: {VSHORT}"
)

#setting intents
intents = discord.Intents.default()
intents.message_content = True

#registering the commands from attached files
bot = commands.Bot(command_prefix="bb", intents=intents)
bot.tree.add_command(debug.dinfo(bot), guild=GUILD)
bot.tree.add_command(gencom.gcom(bot), guild=GUILD)

#Starting BunnyBot, syncing commmands to guild, print ready

@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD)
    print("Bunnybot loaded! {} {}".format(bot.user.name,bot.user.id), f"Version: {VLONG}")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "https://twitter.com" in message.content:
        await message.channel.send(message.content.replace("https://twitter.com/","https://fxtwitter.com/"))
        await message.delete()
    if "https://x.com/" in message.content:
        await message.channel.send(message.content.replace("https://x.com/","https://fxtwitter.com/"))
        await message.delete()
        await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)