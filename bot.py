import discord
from discord.ext import commands
from discord import app_commands 
import random
import json
from config import *

# * Starting the discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

text_channels = []
voice_channels = []
filename = ''  # * Set initial value of filename

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except Exception as e:
        print(e)

# TODO: Make it so that only people with the @admin rank can use the commands of the bot
# * First command, to specify the .json file
@bot.tree.command(name="blueprint")
@app_commands.describe(select="bp1 | bp2 | bp3")
async def blueprint(interaction: discord.Interaction, select: str):
    global filename
    data = None
    if select in ["bp1", "bp2", "bp3"]:
        if select == "bp1":
            filename = "blueprint1.json"
        elif select == "bp2":
            filename = "blueprint2.json"
        else:
            filename = "blueprint3.json"
        await interaction.response.send_message(f"{interaction.user.name} choose: `{select}`", ephemeral=True)

        # * Read the .json file
        with open(f'blueprints/{filename}', 'r') as f:
            data = json.load(f)
    else:
        await interaction.response.send_message(f"{interaction.user.name}, that is not a valid option. Please enter a valid option: `bp1`, `bp2`, or `bp3`.", ephemeral=True)
    
    if data is not None:

        global text_channels
        global voice_channels

        for text_room_name, text_room_data in data.get('text', {}).items():
            text_channels.append(text_room_name)

            try:
                permissions = text_room_data.get('permissions', [])
            except IndexError:
                print("No permissions set in a text channel, please atleast use default as the variable! Stopping...")
                exit

            try:
                embed_message = text_room_data.get('messages', {}).get('embed', [])[0]
                normal_message = text_room_data.get('messages', {}).get('msg', [])[0]
                # print(embed_message, normal_message)
            except IndexError:
                print("No embed, or normal message found, skipping...")
                pass

        for voice_room_name, voice_room_data in data.get('voice', {}).items():
            voice_channels.append(voice_room_name)
            
            try:
                permissions = voice_room_data.get('permissions', [])
            except IndexError:
                print("No permissions set in a voice channel, please atleast use default as the variable! Stopping...")
                exit

        # print(text_channels, voice_channels)

# TODO: Need to add the -o for override mode, in case someone wants to creat the server from the ground

@bot.tree.command(name="start")
@app_commands.describe(select="-a for append")
async def start(interaction: discord.Interaction, select: str):
    guild = bot.get_guild(SERVER)
    if select == "-a":
        if filename in ["blueprint1.json", "blueprint2.json", "blueprint3.json"]:
            for tchannels in text_channels:
                await guild.create_text_channel(tchannels)
                print(f"Creating {tchannels}...")
                
            for vchannels in voice_channels:
                await guild.create_text_channel(vchannels)
                print(f"Creating {vchannels}...")
            
            await interaction.response.send_message(f"The blueprint `{filename}` has been applied on the server!")
        else:    
            await interaction.response.send_message(f"{interaction.user.name}, firstly you should set the desired .json file. Please enter one of these options after `/blueprint` : `bp1`, `bp2`, or `bp3`.", ephemeral=True)
    else:
        await interaction.response.send_message(f"{interaction.user.name}, please use the `-a` argument for appending mode.", ephemeral=True)

bot.run(TOKEN)