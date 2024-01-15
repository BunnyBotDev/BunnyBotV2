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
        
    @apc.command()
    async def userinfo(self, interaction: discord.Interaction, user: discord.User):
        e = discord.Embed(title=user.display_name+"'s info", description="Heres what I could find!", color=user.accent_color)
        e.add_field(name='Title', value=user.name)
        e.add_field(name='User ID', value=user.id)
        e.add_field(name='Status', value=user.status)
        e.add_field(name='Highest Role', value=user.top_role)
        e.add_field(name='Join Date', value=user.joined_at)
        e.add_field(name='Registration Date', value=user.created_at)
        e.add_field(name='Profile Picture', value=user.avatar)
        e.set_image(url=str(user.avatar))
        await interaction.response.send_message("Heres is <@{}>'s info!".format(user.id), embed=e, ephemeral=False)
        
    @apc.command()
    async def roll(self, interaction: discord.Interaction, expression: str):
        """🎲 rolls dice expressions."""
        from dice import roll, DiceBaseException
        from re import search
        mod = '0'
        if search(r'[^\.]\+\d+$', expression):
            expression, mod = expression.split('+')
        elif search(r'[^\.]\-\d+$', expression):
            expression, mod = expression.split('-')
            mod = '-'+mod
        valmod = int(mod)
        try:
            a = roll(expression)
        except DiceBaseException as e:
            await interaction.response.send_message('Error in expression:\n```{}\n{}```'.format(expression, e.pretty_print()))
            return
        mod = '' if valmod == 0 else ', {:+d}'.format(valmod)
        if isinstance(a, list):
            if len(str(a)) <= 1000:
                message = '🎲 {}\ntotal 🎲 is {}'.format((', '.join(str(x) for x in a) + mod), sum(a, valmod))
            else:
                message = 'total 🎲 is {}'.format(sum(a, valmod))
        else:
            message = "total 🎲 is {} \nSince you added more dice after the +, I couldn't get you the list of individual dice rolls.".format(a)
        await interaction.response.send_message(message, ephemeral=False)