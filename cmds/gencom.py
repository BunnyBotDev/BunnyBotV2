import discord
from discord import app_commands as apc
import os

class gcom(apc.Group, name="general"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        
    @apc.command()
    async def avatar(self, interaction: discord.Interaction, user: discord.User):
        """grab someones avatar"""
        e = discord.Embed()
        e.set_image(url=str(user.avatar))
        await interaction.response.send_message("Heres is <@{}>'s avatar!".format(user.id), embed=e, ephemeral=True)
        