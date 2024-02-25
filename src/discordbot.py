import discord
from discord import Intents
from discord.ext import commands


class DiscordClient(commands.Bot):
    def __init__(
        self,
        intents: Intents,
        guild_id: int,
        guild_channel: str,
        available_commands: str,
        command_prefix="!",
    ) -> None:
        super().__init__(intents=intents, command_prefix=command_prefix)
        self.guild_id = guild_id
        self.guild_channel = guild_channel
        self.available_commands = available_commands
        self.default_message = [
            "**Welcome to ChatBotGPT Discord Bot!**",
            "This bot allows you to interact with ChatBotGPT.",
            "**Available Commands:**",
            *available_commands,
            "To get started, simply type one of the commands listed above followed by any additional parameters as needed.",
            "Feel free to reach out if you have any questions or need assistance!",
        ]
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="/ask | /clear"
        )

    async def on_ready(self):
        for guild in self.guilds:
            if guild.id == self.guild_id:
                synced = await self.tree.sync()
                print(
                    f"{guild.name} (id: {guild.id})\n"
                    f"Discord Version: {discord.__version__}\n"
                    f"Commands: {str(len(synced))}\n"
                )
                break
            else:
                print("Bot is not in the specified guild.")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if self.is_channel_allowed(str(message.channel.id)) is False:
            return await message.channel.send(
                "You're not allowed to use this command in this channel."
            )

        for msg in self.default_message:
            await message.channel.send(msg)

    def is_channel_allowed(self, channel: str) -> bool:
        """
        Checks if a given channel matches a specific channel in the guild.

        Args:
            channel (str): The name of the channel to check.
            guild_channel (str): The name of the guild channel to compare against.

        Returns:
            bool: True if the provided channel matches the guild channel, False otherwise.
        """
        return channel == self.guild_channel
