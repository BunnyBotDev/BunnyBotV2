from datetime import datetime
import discord
from discord import app_commands as apc
from discord.ext import commands

class PagedChangelog(discord.ui.View):
    """Paged menu specifically made for the changelog"""
    def __init__(self, pages):
        super().__init__()
        self.page = 0
        self.pages = pages

    def embed(self):
        lines = self.pages[self.page].split('\n')
        e = discord.Embed()
        e.title = lines[0].split(": ")[1]
        e.timestamp = datetime.strptime(lines[1].split(": ")[1], "%m/%d/%y")
        e.description = '\n'.join(lines[2:])
        return e

    @discord.ui.button(label="Newer", custom_id='newer', disabled=True, row=0, emoji="◀")
    async def newer_page(self, interaction: discord.Interaction, _):
        self.page -=1
        await self.update_page(interaction)

    @discord.ui.button(label="Older", custom_id='older', row=0, emoji="▶")
    async def older_page(self, interaction: discord.Interaction, _):
        self.page += 1
        await self.update_page(interaction)

    async def update_page(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        for i in self.children:
            if i.custom_id == 'newer':
                i.disabled = True if self.page <= 0 else False
            elif i.custom_id == 'older':
                i.disabled = False if self.page < len(self.pages)-1 else True
        await interaction.message.edit(embed=self.embed(), view=self)

class Debug(commands.Cog, name="debugging"):
    """Debugging cog for bunnybot."""
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

#Setup of commands, developer and debug
    @apc.command()
    async def version(self, interaction: discord.Interaction):
        """What Version BunnyBot is running (Format: Codename-MajorVersion.MinorVersion.EmergencyPatch)"""
        await interaction.response.send_message(f"I am running version: {self.bot.version[1]}", ephemeral=True)

    @apc.command()
    async def ping(self, interaction: discord.Interaction):
        """retrieve ping of the bot!"""
        await interaction.response.send_message(f"Pong, {int(self.bot.latency*10000)/10.0}ms! :ping_pong:", ephemeral=True)

    @apc.command()
    async def changelog(self, interaction: discord.Interaction):
        """sends the full changelog text file as a message"""
        pages = self.bot.changelog.split('\n\n')
        paged = PagedChangelog(pages)
        await interaction.response.send_message(embed=paged.embed(), view=paged)


async def setup(bot: commands.bot):
    await bot.add_cog(Debug(bot), guild=bot.guild)