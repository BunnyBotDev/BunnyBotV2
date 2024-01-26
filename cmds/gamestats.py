import discord
from discord import app_commands as apc
from dotenv import load_dotenv
import os
import time
import requests
from requests.auth import HTTPBasicAuth
import base64


#Create variables
TRN = "ff310728-e8db-4c2e-9304-fd44da5ac7c7"

class gstats(apc.Group, name="gamestats"):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        
    @apc.command()
    async def csgo(self, interaction: discord.Interaction, input: str):
        """Grabs a users csgo stats"""
        UserID = str(input)
        method = "get"
        URL = f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/76561198008049283"
        headers={"TRN-Api-Key": TRN, "Content-Type": "application/json"}

       
        rsp = requests.request(method, URL, headers=headers, auth=None)
        await interaction.response.send_message(rsp)
        print(f"{rsp.status_code}: {rsp.text}")