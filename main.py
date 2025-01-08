import discord
import subprocess
import json
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_USERNAME = os.getenv("TWITCH_USERNAME")
CHECK_INTERVAL = 60  # Check every 60 seconds

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_stream_status():
    """Checks if the Twitch user is live and notifies the Discord server."""
    is_live = False  # Track if the user is already live to prevent spam

    await client.wait_until_ready()
    channel = discord.utils.get(client.get_all_channels(), name="general")  # Replace with your channel name

    while not client.is_closed():
        try:
            result = subprocess.run(
                ["streamlink", f"https://twitch.tv/{TWITCH_USERNAME}", "--json"],
                capture_output=True,
                text=True,
            )
            output = json.loads(result.stdout)

            if output.get("streams") and not is_live:
                is_live = True
                message = f"@everyone 🎉 **{TWITCH_USERNAME} is LIVE!** Watch here: https://twitch.tv/{TWITCH_USERNAME}"
                await channel.send(message)
            elif not output.get("streams"):
                is_live = False
                print("USER IS CURRENTLY OFFLINE")

        except Exception as e:
            print(f"Error checking stream status: {e}")

        await asyncio.sleep(CHECK_INTERVAL)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(check_stream_status())

client.run(TOKEN)
