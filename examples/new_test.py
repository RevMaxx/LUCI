# new_test.py
from Luci.Models.model import ChatModel

# Initialize the ChatModel class
chat_model = ChatModel(
    model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # Specify your model name
    api_key="aea3aab7b8275c73f7b171588bf030cf6f0e51f8c638f1bfb8ffbe919332d99d",  # Your OpenAI API key
    prompt="What is the weather today?"
)

# Call the method that generates a response
result = chat_model.call_together()

# Print the result
print(result)
