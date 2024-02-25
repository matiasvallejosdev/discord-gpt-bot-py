from typing import Dict, List
from collections import defaultdict


class MemoryInterface:
    def append(self, user_id: str, message: Dict) -> None:
        pass

    def get(self, user_id: str) -> str:
        return ""

    def remove(self, user_id: str) -> None:
        pass


class Memory(MemoryInterface):
    def __init__(self, system_message: str):
        self.storage = defaultdict(list)
        self.system_message = system_message

    def initialize(self, user_id: str):
        if isinstance(self.system_message, Dict):
            self.storage[user_id] = [self.system_message]
        elif isinstance(self.system_message, List):
            self.storage[user_id] = self.system_message
        else:
            self.storage[user_id] = [{
                "role": "system",
                "content": "You're a general assitant."
            }]
            
            

    def append(self, user_id: str, message: Dict) -> None:
        if self.storage[user_id] == []:
            self.initialize(user_id)
        self.storage[user_id].append(message)

    def get(self, user_id: str) -> str:
        return self.storage[user_id]

    def remove(self, user_id: str) -> None:
        self.storage[user_id] = []