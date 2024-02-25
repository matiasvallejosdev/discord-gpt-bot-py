import os
import discord

from dotenv import load_dotenv, find_dotenv

from src.utils import read_json
from src.models import OpenAIModel
from src.chatgpt import ChatGPT
from src.discordbot import DiscordClient
from src.sender import Sender
from src.memory import Memory
from src.server import keep_alive

load_dotenv(find_dotenv())
models = OpenAIModel(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_engine=os.getenv("OPENAI_MODEL"),
    temperature=int(os.getenv("OPENAI_TEMPERATURE")),
    max_tokens=int(os.getenv("OPENAI_TOKENS")),
)
system = read_json("system.json")
memory = Memory(system_message=system)
chatgpt = ChatGPT(models, memory)


def run():
    """Run discord bot using discord client and sender."""
    intents = discord.Intents.all()
    available_commands = [
        "/ask - Ask a question to ChatBotGPT.",
        "/help - Gives a list of options to interact with your agent.",
    ]
    client = DiscordClient(
        intents=intents,
        guild_id=int(os.getenv("DISCORD_GUILD_ID")),
        guild_channel=os.getenv("DISCORD_GUILD_CHANNEL"),
        available_commands=available_commands,
    )
    sender = Sender()

    @client.tree.command(
        name="help",
        description="Help options for your agent.",
    )
    async def help(interaction: discord.Interaction):
        if client.is_channel_allowed(str(interaction.channel_id)) is False:
            receive = "You're not allowed to use this command in this channel."
            await interaction.response.send_message(receive, ephemeral=True)

        # Create the combined message with available commands
        receive = "\n".join(available_commands)

        # Send the concatenated message as a single response
        await interaction.response.send_message(receive, ephemeral=True)

    @client.tree.command(
        name="ask",
        description="Send a message to your gpt agent.",
    )
    async def ask(interaction: discord.Interaction, message: str):
        user_id = interaction.user.id

        if client.is_channel_allowed(str(interaction.channel_id)) is False:
            receive = "You're not allowed to use this command in this channel."
            await sender.send_message(interaction, user_id, message, receive)

        if interaction.user == client.user:
            return

        await interaction.response.defer()
        receive = chatgpt.get_response(user_id, message)
        await sender.send_message(interaction, user_id, message, receive)

    @client.tree.command(
        name="clear",
        description="Clear your chat history.",
    )
    async def clear(interaction: discord.Interaction):
        if client.is_channel_allowed(str(interaction.channel_id)) is False:
            receive = "You're not allowed to use this command in this channel."
            await interaction.response.send_message(receive, ephemeral=True)

        user_id = interaction.user.id
        memory.remove(user_id)
        await interaction.response.send_message(
            f"Messages history for {user_id} was cleared.", ephemeral=True
        )

    # Run your discord client
    client.run(token=os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    keep_alive()
    run()
