import discord
import responses


async def send_message(message, user_message, is_private):
    """Send message using discord API to a discord channel public or private.

    Args:
        message (interface): Interface to send message to discord.
        user_message (str): User message entry.
        is_private (bool): Chat type private or public.
    """
    try:
        response = responses.handle_response(user_message)
        print(f"bot: '{response}'")

        if isinstance(response, list):  # Check if response is a list of messages
            for msg in response:
                await message.author.send(msg) if is_private else await message.channel.send(msg)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def is_discord_bot_channel(channels, channel):
    """Returns True or False boolean depending if the channel is inside my channel array.

    Args:
        channels (str): String with comma-separated channel names.
        channel (str): Channel message.
        author (str): Author of the message.

    Returns:
        bool: True if the author is found in the channel string, False otherwise.
    """
    if 'Direct' in channel:
        return True
    else:
        channel_list = channels.split(",")
        return channel in channel_list


def run_discord_bot(TOKEN, GUILD, CHANNELS):
    """Run discord bot using discord api and discord async events.

    Args:
        TOKEN (str): Token for API connection getted from discord application that contains some permissiomns.
        GUILD (str): Your guild name.
    """
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        print(
            f"{client.user} is connected to the following guild:\n"
            f"{guild.name}(id: {guild.id})\n"
        )

    @client.event
    async def on_message(message):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        if (
            message.author == client.user
            or is_discord_bot_channel(CHANNELS, channel) is False
        ):
            return

        if len(user_message) == 0:
            return

        print(f"{channel}")
        print(f"{username}: '{user_message}'")
        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, True)
        else:
            await send_message(message, user_message, False)

    client.run(TOKEN)
