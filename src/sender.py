from pickle import TRUE
from discord import Interaction


class Sender:
    async def send_message(self, interaction: Interaction, user_id: str, send: str, receive: str):
        """
        Send a message using the Discord API to a Discord channel, either publicly or privately.

        Args:
            messages_history (list): List of previous messages.
            interaction (Interaction): The Discord interaction object.
            send (str): The user message to be sent.
            receive (str): Th
            ephemeral (bool): Indicates whether the message should be sent privately or publicly.
        """
        try:
            print(f"{user_id} sent: {send}, response: {receive}")
            if isinstance(receive, list):  # Check if response is a list of messages
                for msg in receive:
                    await interaction.followup.send(f"{msg}")
            else:
                await interaction.followup.send(f"{receive}")
        except Exception as e:
            print(e)
