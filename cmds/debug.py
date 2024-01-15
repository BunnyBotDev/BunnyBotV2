import discord
from discord import app_commands as apc
import os
import time
import json

#Json Loading
with open('variables.json') as var_file: 
#Json variables
    pjson = json.load(var_file)
VSHORT = pjson['VSHORT']
VLONG = pjson['VLONG']
LASTADDED = pjson['LASTADDED']

class dinfo(apc.Group, name="debugging"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot

#Setup of commands, developer and debug
    @apc.command()
    async def version(self, interaction: discord.Interaction):
        """What Version BunnyBot is running (Format: Codename-MajorVersion.MinorVersion.EmergencyPatch)"""
        await interaction.response.send_message(f"I am running version: {VSHORT}", ephemeral=True)
    
    @apc.command()
    async def ping(self, interaction: discord.Interaction):
        """retrieve ping of the bot!"""
        await interaction.response.send_message("Pong, {}ms! :ping_pong:".format(int(self.bot.latency*10000)/10.0), ephemeral=True)
        
#    @apc.command()    
#    async def lastcommand(self, interaction: discord.Interaction):
#        """display the last command ran on the bot"""
#        await interaction.response.send_message("I dont work yet!", ephemeral=True)

    @apc.command()
    async def changelog(self, interaction: discord.Interaction):
        """The changelog from the last update"""
        await interaction.response.send_message(f"Last changes to the bot were: ```{LASTADDED}```", ephemeral=True)
        
    @apc.command()
    async def fullchangelog(self, interaction: discord.Interaction):
        """sends the full changelog text file as a message"""
        with open('cmds/changelog.txt') as f:
            await interaction.response.send_message(f.read(), ephemeral=True)

