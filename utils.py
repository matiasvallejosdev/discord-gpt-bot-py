
def is_channel_allowed(channel: str, guild_channel: str) -> bool:
    """
    Checks if a given channel matches a specific channel in the guild.

    Args:
        channel (str): The name of the channel to check.
        guild_channel (str): The name of the guild channel to compare against.

    Returns:
        bool: True if the provided channel matches the guild channel, False otherwise.
    """
    return channel == guild_channel