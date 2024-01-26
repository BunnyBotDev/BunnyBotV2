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

class PagedChangelog(discord.ui.View):
    """Paged menu specifically made for the changelog"""
    def __init__(self, pages):
        super().__init__()
        self.page = 0
        self.pages = pages

    @discord.ui.button(label="Newer", custom_id='newer', disabled=True, row=0)
    async def newer_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -=1
        await self.update_page(interaction)

    @discord.ui.button(label="Older", custom_id='older', row=0)
    async def older_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        await self.update_page(interaction)

    async def update_page(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        for i in self.children:
            if i.custom_id == 'newer':
                i.disabled = True if self.page <= 0 else False
            elif i.custom_id == 'older':
                i.disabled = False if self.page < len(self.pages)-1 else True
            (i.custom_id)
            (i.disabled)
        await interaction.message.edit(content=f"```{self.pages[self.page]}```", view=self)

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
    
    @apc.command()
    async def changelog(self, interaction: discord.Interaction):
        """sends the full changelog text file as a message"""
        with open('cmds/changelog.txt', 'r', encoding='utf-8') as f:
            pages = f.read().split('\n\n')
            await interaction.response.send_message(f"```{pages[0]}```", view=PagedChangelog(pages))
            
    @apc.command()
    async def help(self, interaction: discord.Interaction):
        """sends the full list of commands as a message"""
        with open('cmds/commands.txt') as f:
            await interaction.response.send_message(f.read(), ephemeral=True)

    