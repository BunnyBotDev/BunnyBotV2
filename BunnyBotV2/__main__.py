import discord
from discord.ext import commands
import os
import time
from dotenv import load_dotenv
import cmds.debug as debug


#grabs my token
load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD = discord.Object(os.getenv("GUILD"))

print(GUILD)


#setting intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="bb", intents=intents)
bot.tree.add_command(debug.dinfo(bot), guild=GUILD)

#Starting BunnyBot, syncing commmands to guild, print ready

@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD)
    print("Bunnybot loaded! {} {}".format(bot.user.name,bot.user.id))

if __name__ == "__main__":
    bot.run(TOKEN)