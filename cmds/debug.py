import discord
from discord import app_commands as apc
import os
import time

class dinfo(apc.Group, name="debugging"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
#Setup of commands, developer and debug
    @apc.command()
    async def version(self, interaction: discord.Interaction):
        """What Version BunnyBot is running (Format: Codename-MajorVersion.MinorVersion.EmergencyPatch)"""
        await interaction.response.send_message("I am running version: New Moon-1.1.0", ephemeral=True)
    
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
        """Whats happened!"""
        with open('cmds/changelog.txt') as f:
            await interaction.response.send_message(f.read(), ephemeral=True)

