import responses
from discord import Interaction

async def send_message(messages_history: list, interaction: Interaction, message: str, is_private: bool) -> None:
    """
    Send a message using the Discord API to a Discord channel, either publicly or privately.

    Args:
        messages_history (list): List of previous messages.
        interaction (Interaction): The Discord interaction object.
        message (str): The user message to be sent.
        is_private (bool): Indicates whether the message should be sent privately or publicly.
    """
    try:
        response = responses.handle_response(messages_history, message)

        if isinstance(response, list):  # Check if response is a list of messages
            for msg in response:
                await interaction.response.send_message(f"{msg}", ephemeral=is_private)
        else:
            await interaction.response.send_message(f"{response}", ephemeral=is_private)
    except Exception as e:
        print(e)