import discord
from discord import app_commands as apc
import os
import time

class dinfo(apc.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
#Setup of commands, developer and debug
    @apc.command()
    async def version(self, interaction: discord.Interaction):
        """What Version I Am (Format: MajorVersion.MinorVersion.EmergencyPatch)"""
        await interaction.response.send_message("I am running version: DEV-1.0.0", ephemeral=True)
    
    @apc.command()
    async def ping(self, interaction: discord.Interaction):
        """retrieve ping of the bot!"""
        await interaction.response.send_message("Pong, {}ms! :ping_pong:".format(int(self.bot.latency*10000)/10.0), ephemeral=True)
        
    @apc.command()
    async def lastfileupdate(self, interaction: discord.Interaction):
        """display the last command ran on the bot"""
        await interaction.response.send_message("Debug Commands was created: , and was last updated:", ephemeral=True)

