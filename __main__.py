import discord
from discord.ext import commands
import os
import time
from dotenv import load_dotenv
import cmds.debug as debug
import cmds.gencom as gencom


#grabs my token
load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD = discord.Object(os.getenv("GUILD"))

#custom activity
activity = discord.CustomActivity(
    name = "Your bunny maid is on firmware version: NM-1.1.0",
)

# using discord.Activity
activity = discord.Activity(
   type = discord.ActivityType.custom,
   name = "Custom Status",  # does nothing but is required
   state = "Your bunny maid is on firmware version: NM-1.1.0"
)


#setting intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="bb", intents=intents)
bot.tree.add_command(debug.dinfo(bot), guild=GUILD)
bot.tree.add_command(gencom.gcom(bot), guild=GUILD)
#Starting BunnyBot, syncing commmands to guild, print ready

@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD)
    print("Bunnybot loaded! {} {}".format(bot.user.name,bot.user.id))

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
            
@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)

if __name__ == "__main__":
    bot.run(TOKEN)