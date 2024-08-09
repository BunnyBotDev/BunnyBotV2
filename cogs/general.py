from re import search

import discord
from discord import app_commands as apc
from discord.ext import commands
from dice import roll, DiceBaseException


class General(commands.Cog, name="general"):
    """Bunnybotv2's General Commands"""
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @apc.command()
    async def avatar(self, interaction: discord.Interaction, user: discord.User):
        """grab someones avatar"""
        #creates a variable for the embed
        e = discord.Embed()
        #sets the embeds image to the users avatar that was passed via discord.User
        e.set_image(url=str(user.avatar))
        await interaction.response.send_message(f"Heres is <@{user.id}>'s avatar!", embed=e, ephemeral=True)

    @apc.command()
    async def userinfo(self, interaction: discord.Interaction, user: discord.User):
        user = interaction.guild.get_member(user.id)
         #creates a variable for the embedm giving it title and descripton
        e = discord.Embed(title=user.display_name+"'s info", description="Heres what I could find!", color=user.accent_color)
         #adding all the fields for the User's details
        e.add_field(name='Title', value=user.name)
        e.add_field(name='User ID', value=user.id)
        e.add_field(name='Status', value=user.status)
        e.add_field(name='Highest Role', value=user.top_role)
        e.add_field(name='Join Date', value=user.joined_at)
        e.add_field(name='Registration Date', value=user.created_at)
        e.add_field(name='Profile Picture', value=user.avatar)
        if user.avatar is not None:
            #setting the embeds image to the users avatar that was passed via discord.User
            e.set_image(url=str(user.avatar))
        await interaction.response.send_message(f"Heres is <@{user.id}>'s info!", embed=e, ephemeral=False)

    @apc.command()
    async def serverinfo(self, interaction: discord.Interaction):
        e = discord.Embed(title=interaction.guild.name+"'s info", description="Heres what I could find!")
        e.add_field(name="Guild Name", value=interaction.guild.name)
        e.add_field(name="Members", value=interaction.guild.member_count)
        e.add_field(name="Owner", value=interaction.guild.owner)
        e.add_field(name="Created At", value=interaction.guild.created_at)
        await interaction.response.send_message(embed=e)

    ####    FIXED; HOURS WASTED: 4  ####
    @apc.command()
    async def status(self, interaction: discord.Interaction, member: discord.Member):
        member = interaction.guild.get_member(member.id)

        # Fetch user status
        status = str(member.status)

        # Fetch user activities
        activities = '\n---\n'.join([str(activity) for activity in member.activities])

        # Create an embed message
        e = discord.Embed(title=f"{member.display_name}'s Status and Activities", description=None, color=member.accent_color)
        e.add_field(name='Status', value=status)
        e.add_field(name='Activities', value=activities or 'No activities')

        # Check if the user is listening to Spotify
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                spotify = activity
                e.add_field(name="",value="")
                e.add_field(name='Listening to', value=spotify.title, inline=True)
                e.add_field(name='Artist', value=', '.join(spotify.artists), inline=True)
                e.add_field(name='Album', value=spotify.album, inline=True)
                e.add_field(name='Track Link', value=spotify.track_url, inline=False)
                e.add_field(name='Started Playing', value=spotify.start.strftime('%H:%M:%S'), inline=True)
                e.add_field(name='Duration', value=str(spotify.duration // 1000000 * 1000000), inline=True) #division and multiplication to strip miliseconds.
                e.set_image(url=spotify.album_cover_url)
                break

        await interaction.response.send_message(embed=e, ephemeral=False)

    @apc.command()
    async def roll(self, interaction: discord.Interaction, expression: str):
        """🎲 rolls dice expressions."""

        if not 'd' in expression:
            expression = "1d" + expression
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
            await interaction.response.send_message(f'Error in expression:\n```{expression}\n{e.pretty_print()}```')
            return
        mod = '' if valmod == 0 else f', {valmod:+d}'
        if isinstance(a, list):
            message = ""
            if len(str(a)) <= 1000: #print all dice if we remain under 1000 chars.
                message += f'🎲 {(', '.join(str(x) for x in a) + mod)}\n'
            if len(a) != 1: #filter out when only 1 dice is rolled
                message += f'total 🎲 is {sum(a, valmod)}'
        else:
            message = f"total 🎲 is {a} \nSince you rolled multiple sets of dice, I couldn't get you the list of individual dice rolls."
        await interaction.response.send_message(message, ephemeral=False)

async def setup(bot: commands.bot):
    await bot.add_cog(General(bot), guild=bot.guild)