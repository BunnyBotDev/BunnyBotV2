import discord
from discord import app_commands as apc
import os
import pythonping
from pythonping import ping



class gcom(apc.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        
    @apc.command()
    async def avatar(self, interaction: discord.Interaction):
        """grab someones avatar"""
        await interaction.response.send_message("I dont work yet!", ephemeral=True)