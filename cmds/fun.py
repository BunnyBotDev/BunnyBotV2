from random import choice, choices

import discord
from discord import app_commands as apc
from discord.ext import commands
import aiohttp

class Fun(commands.Cog, name="funcommands"):
    """Fun commands for bunnybotv2"""
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        
    @apc.command()
    async def pokemon(self, interaction: discord.Interaction, poke: str):
        await interaction.response.defer(thinking=True) #defer, switches bot status to thinking.
        endpoint = "pokemon-species"
        url = "https://pokeapi.co/api/v2/{}/{}"
        headers = {'Accept': 'application/json'}

        pokecolours = { #list of pokemon type colors, using this for coloring the embed.
            'normal': 'A8A77A',
            'fire': 'EE8130',
            'water': '6390F0',
            'electric': 'F7D02C',
            'grass': '7AC74C',
            'ice': '96D9D6',
            'fighting': 'C22E28',
            'poison': 'A33EA1',
            'ground': 'E2BF65',
            'flying': 'A98FF3',
            'psychic': 'F95587',
            'bug': 'A6B91A',
            'rock': 'B6A136',
            'ghost': '735797',
            'dragon': '6F35FC',
            'dark': '705746',
            'steel': 'B7B7CE',
            'fairy': 'D685AD',
        }
        e = discord.Embed()
        async with aiohttp.ClientSession() as session:
            async with session.get(url.format(endpoint, poke), headers=headers) as resp:
                if resp.status == 404:
                    await interaction.followup.send(f"That pokemon ({poke}) doesn't seem to exist!")
                    return
                data_spec = await resp.json()
            pokeURL = data_spec['varieties'][0]['pokemon']['url']
            async with session.get(pokeURL, headers=headers) as resp:
                data = await resp.json()

        dex_num=[x for x in data_spec['pokedex_numbers'] if x['pokedex']['name'] == 'national'][0]['entry_number']
        e.title = data_spec['name'].capitalize() + f" (#{dex_num:04d})"
        flavor_text = choice([x for x in data_spec['flavor_text_entries'] if x['language']['name'] == 'en'])['flavor_text'] \
            .replace('\f',       '\n') \
            .replace('\u00ad\n', '') \
            .replace('\u00ad',   '') \
            .replace(' -\n',     ' - ') \
            .replace('-\n',      '-') \
            .replace('\n',       ' ')
        e.description = flavor_text

        #typing
        try:
            e.set_author(name=data['types'][0]['type']['name'] + "/" + data['types'][1]['type']['name'])
        except IndexError:
            e.set_author(name=data['types'][0]['type']['name'])
        e.colour =int(pokecolours[data['types'][0]['type']['name']], 16)
        #Image
        sprites = [x for x in data['sprites'] if x.startswith('front_') and not data['sprites'][x] is None]
        weights = []
        for x in sprites:
            weights.append(1 if x.startswith('front_shiny') else 24)
        e.set_image(url=data['sprites'][choices(sprites, weights)[0]])
        #stats
        for x in range(6):
            e.add_field(name=data['stats'][x]['stat']['name'], value=data['stats'][x]['base_stat'])
        e.add_field(name='weight', value=f'{data["weight"]/10.0} Kg')
        e.add_field(name='height', value=f'{data["height"]/10.0} m')
        e.add_field(name='capture rate', value=data_spec['capture_rate'])
        for x in data['abilities']:
            e.add_field(name='Hidden Ability' if x['is_hidden'] else 'Ability', value=x['ability']['name'])
        await interaction.followup.send(embed=e)
