from .models import ModelInterface
from .memory import MemoryInterface

class ChatGPT:
    def __init__(self, model: ModelInterface, memory: MemoryInterface):
        self.model = model
        self.memory = memory

    def get_response(self, user_id: str, text: str) -> str:
        self.memory.append(user_id,{'role': 'user', 'content': text})
        
        # Generate AI Response
        response = self.model.chat_completion(self.memory.get(user_id))
        
        # Accessing role and content from the first choice
        role = response.choices[0].message.role
        content = response.choices[0].message.content

        # Appending the role and content to memory
        self.memory.append(user_id, {'role': role, 'content': content})
        return content

    def clean_history(self, user_id: str) -> None:
        self.memory.remove(user_id)