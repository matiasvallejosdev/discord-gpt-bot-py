import gpt

messages = []


def handle_response(message):
    """Handle bot responses using chatgpt with openai api or automatic answers.

    Args:
        message (string): Prompt message to be answered.
    """
    prompt = str(message).lower()
    response = ""

    if prompt == "clear history" or prompt == "clear":
        messages.clear()
        response = "Clear successfully!"
        return response
    elif prompt == "hi":
        messages.clear()
        response = [
            "Hi! Welcome to the chatbot.",
            "You can start a private conversation by typing '?' followed by your message.",
            "To clear the message history, type 'clear' or 'clear history'.",
            "How can I assist you today?"
        ]
        return response
    elif prompt == "how are you?":
        response = "I'm just a bot, so I don't have feelings, but thanks for asking!"
        return response
    elif "thank you" in prompt:
        response = "You're welcome!"
        return response
    elif "bye" in prompt:
        response = "Goodbye! Have a great day!"
        return response
    else:
        response = gpt.ask(messages, prompt)
        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response})
    return response
