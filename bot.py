import discord
from discord.ext import commands
from messages import send_message
from utils import is_channel_allowed

def run_discord_bot(TOKEN, GUILD_ID, GUILD_CHANNEL):
    """Run discord bot using discord api and discord async events.

    Args:
        TOKEN (str): Token for API connection getted from discord application that contains some permissiomns.
        GUILD (str): Your guild name.
    """
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="!", intents=intents)
    messages = []
    available_commands = [
    "/ask - Ask a question to ChatBotGPT.",
    "/clear - Clear the chatbot messages history for the current user."
    ]
    default_message = [
        "**Welcome to ChatBotGPT Discord Bot!**",
        "This bot allows you to interact with ChatBotGPT.",
        "**Available Commands:**",
        *available_commands,
        "To get started, simply type one of the commands listed above followed by any additional parameters as needed.",
        "Feel free to reach out if you have any questions or need assistance!"
    ]

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.id == GUILD_ID:
                synced = await client.tree.sync()
                print(
                    f"{guild.name} (id: {guild.id})\n"
                    f"Discord Version: {discord.__version__}\n"
                    f"Commands: {str(len(synced))}\n"
                )
                break
        else:
            print("Bot is not in the specified guild.")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if is_channel_allowed(str(message.channel.id), GUILD_CHANNEL) is False:
            return await message.channel.send("You're not allowed to use this command in this channel.")

        for msg in default_message:
            await message.channel.send(msg)
    
    @client.tree.command(
        name="clear",
        description="Clear your chat history.",
    )
    async def clear(interaction: discord.Interaction):
        if is_channel_allowed(str(interaction.channel_id), GUILD_CHANNEL) is False:
            return await interaction.response.send_message("You're not allowed to use this command in this channel.")
        
        user_id = interaction.user.id
        messages.clear()
        await interaction.response.send_message(f"Messages history for {user_id} was cleared.")
        
    @client.tree.command(
        name="ask",
        description="Send a message to your gpt agent.",
    )
    async def ask(interaction: discord.Interaction, message: str):
        if is_channel_allowed(str(interaction.channel_id), GUILD_CHANNEL) is False:
            return await interaction.response.send_message("You're not allowed to use this command in this channel.")

        if message[0] == "?":
            message = message[1:]
            await send_message(messages, interaction, message, True)
        else:
            await send_message(messages, interaction, message, False)

    @client.tree.command(
        name="help",
        description="Help options for your agent.",
    )
    async def help(interaction: discord.Interaction):
        if is_channel_allowed(str(interaction.channel_id), GUILD_CHANNEL) is False:
            return await interaction.response.send_message("You're not allowed to use this command in this channel.")

        # Create the combined message with available commands
        message = '\n'.join(available_commands)

        # Send the concatenated message as a single response
        return await interaction.response.send_message(message, ephemeral=True)
                        
    client.run(TOKEN)
    