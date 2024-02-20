import os
import bot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CHANNELS = os.getenv("DISCORD_CHANNELS")

if __name__ == "__main__":
    bot.run_discord_bot(TOKEN, GUILD, CHANNELS)
