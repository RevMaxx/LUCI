from Luci.Agents.chat_agent import ChatAgent
import os

async def main():
    model_name = "gpt-4o-mini"
    api_key = "sk-proj-qxKCxYrDK44NZxFM1mcsT3BlbkFJg7rO9hjKLJYahr8KyLnJ"
    prompt = "Translate the following English text to French: 'Hello, how are you?'"
    agent = ChatAgent(model_name=model_name, api_key=api_key, prompt=prompt)
    
    # Get a response from OpenAI
    response = await agent.get_response()
    print("OpenAI Response:", response)
