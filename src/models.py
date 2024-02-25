
from typing import Dict, List
import openai


class ModelInterface:
    def chat_completion(self, messages: List) -> str:
        pass

    def image_generation(self, prompt: str) -> str:
        pass


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str, model_engine: str, temperature: str, max_tokens: int):
        super().__init__()
        openai.api_key = api_key
        self.model_engine = model_engine or "gpt-3.5-turbo-1106"
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def chat_completion(self, messages):
        """Chat completion to gpt using a openai api with a model.
        Args:
            messages (list): List of messages with openai formatting.
            prompt (str): Prompt message for gpt.
            temperature (int, optional): Temperature var for openai settings. Defaults to 0.
            max_tokens (int, optional): Tokens used for this messages. Defaults to 100.

        Returns:
            str: Return the content answer for the last prompt.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model_engine,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response
        except openai.OpenAIError as e:
            return f"Error generating response from server: {str(e)}"