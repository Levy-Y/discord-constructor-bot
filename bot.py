import discord
from discord.ext import commands
from discord import app_commands
import random
import json
from config import TOKEN

# * Starting the discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

filename = ''  # * Set initial value of filename

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except Exception as e:
        print(e)

@bot.tree.command(name="blueprint")
@app_commands.describe(selected_bp="bp1 | bp2 | bp3")
async def blueprint(interaction: discord.Interaction, selected_bp: str):
    global filename
    if selected_bp == "bp1":
        filename = "blueprint1.json"
    elif selected_bp == "bp2":
        filename = "blueprint2.json"
    elif selected_bp == "bp3":
        filename = "blueprint3.json"

    await interaction.response.send_message(f"{interaction.user.name} choose: `{selected_bp}`", ephemeral=True)

    # * Read the .json file
    with open(f'blueprints/{filename}', 'r') as f:
        data = json.load(f)

    text_channels = []
    voice_channels = []

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
            print(embed_message, normal_message)
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

    print(text_channels, voice_channels)

bot.run(TOKEN)
