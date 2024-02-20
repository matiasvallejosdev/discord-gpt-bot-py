import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # read local .env file

API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = API_KEY
openai_model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo-1106")


def ask(messages_history, prompt, temperature=0, max_tokens=100):
    """Ask to gpt using a openai api with a model.

    Args:
        messages_history (list): List of messages with openai formatting.
        prompt (str): Prompt message for gpt.
        temperature (int, optional): Temperature var for openai settings. Defaults to 0.
        max_tokens (int, optional): Tokens used for this messages. Defaults to 100.

    Returns:
        str: Return the content answer for the last prompt.
    """
    try:
        messages_history.append({"role": "user", "content": prompt})
        response = openai.chat.completions.create(
            model=openai_model,
            messages=messages_history,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"Error generating response from server: {str(e)}"
