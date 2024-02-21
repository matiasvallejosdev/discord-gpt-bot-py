import os
import bot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
GUILD_CHANNEL = os.getenv("DISCORD_GUILD_CHANNEL")

if __name__ == "__main__":
    bot.run_discord_bot(TOKEN, GUILD_ID, GUILD_CHANNEL)
