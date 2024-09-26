## LUCI 

Luci is the first AI-based medical agent designed to automate a wide range of healthcare processes. Luci also facilitates advanced tasks like generating master prompts that interconnect and enabling custom search queries for text or images, all with simple Python calls. It helps professionals handle everything from generating SOAP notes to performing agentic searches, assisting with GPT queries, and even creating personalized AI models.

## Installation

```bash
pip install LuciAI
```

## Usage

After installing luci - go to your terminal and type luci_cli

### Ask Any Query

```bash
luci-cli cerina "Your Query?"
```
![alt text](image.png)

### Agentic Search

```bash
luci-cli search "COVID-19 symptoms" --type text --async-mode --max-results 5
```
![alt text](image-1.png)

You can switch between text and image searches, and toggle asynchronous mode by adding --async-mode.

- Change --type to `text` or `image`
- If you choose asynchronous mode then add it `--async-mode`
- If you want to use synchronous then remove it

### Models

Choose your model and find their respective methods!

|FUNCTION NAME | METHOD | TYPE |
| -------------| ------------- | -------------|
| TOGETHER     | call_together | ASYNC |
| OPENAI       | call_gpt | SYNC |
| OPENAI       | call_async_gpt | ASYNC |
| AZURE OPENAI | call_azure | ASYNC |
| AZURE OPENAI | call_azure_sync | SYNC |

```python
from Luci.Models.model import ChatModel

# Initialize the ChatModel class
chat_model = ChatModel(
    model_name="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # Specify your model name
    api_key="",  # Your OpenAI API key
    prompt="What is the weather today?"
    #SysPrompt = "You can mention your system prompt here"
)

# Call the method that generates a response
result = chat_model.call_together()

# Print the result
print(result)
```

### Searching any Query

```python
from Luci.Agents import Search

query = "Revmaxx LLC"
search_instance = Search(query)

results = search_instance.search_text(max_results=5)
search_instance.print_text_result(results)
```

### Get the JSON Response of the Search Query

```python
from Luci import search_text

query="Recent trends of AI?"

print(search_text(query, max_results=3))
```

### Search any Image

```python
from Luci import Search

query = "Your Query ?"
search_instance = Search(query)

results = search_instance.search_images(max_results=5)
search_instance.print_text_result(results)
```

### Generate SOAP Notes through CLI

```bash
luci-cli soap --model "your_model" --api-key "your_api_key" --subjective "..." --objective "..." --assessment "..." --plan "..." --master-prompt "..." --connected
```

### Generate SOAP Notes

```python
from Luci.Agents.soap import *

model_name = "" # Mention the model name
api_key = # or pass directly from user input

t = "Fetch transcript from a audio of doctor & patient conversations"   
S = f"""Generate a subjective from the transcript {t} by mentioning the heading ## Subjective under sub headings **Chief Complaints**, **HPI** """
O = f"Find the objectives from the transcript {t} by mentioning the heading ## Objective under sub headings **Vitals** and **History**"
A = f"Find the assessment from the transcript {t} by mentioning the heading ## Assessment under a list of valid assessments"
P = f"Generate plan from the transcript {t} by mentioning the heading ## Plan under a list of valid plans"
M = "Generate a detailed SOAP note based on the inputs. Follow headings and sub-headings carefully"

    # Create an instance of the SoapAgent class
soap_agent = SoapAgent(model_name=model_name, api_key=api_key, connected=True)
soap_agent.create_soap(S, O, A, P, M)
```

### Voice Documentation

Voice dictation for clinical notes, transcribing speech to text, and structuring it into standardized formats like SOAP notes.

```python
from Luci.Agents.voice_documentation_agent import VoiceDocumentationAgent

agent = VoiceDocumentationAgent(
    model_name='',  # Replace with your model name
    api_key='',   # Replace with your Together API key
    method='call_together' #mention here method
)
agent.run()
```
### CLI Example

```bash
luci-cli voice_doc --model-name <MODEL_NAME> --api-key <API_KEY> [--method <METHOD>] [--stop-word <STOP_WORD>]
```

### Medical Search Agent

Search the new papers on pubmed through luci!

```python
from Luci.Agents.medica_search_agent import MedicalSearchAgent

email = "wbavishek@gmail.com"
max_results = 5
query = "diabetes treatment guidelines"

agent = MedicalSearchAgent(email=email, max_results=max_results)
articles = agent.search(query)
agent.print_results(articles)
```
### CLI Example

```python
luci-cli medsearch "diabetes treatment guidelines" --email "wbavishekbhattacharjee@gmail.com"
 --max-results 2
```

### Chain of Thoughts

```python
import asyncio
from Luci import create_master_prompt

async def main():
    # Define API key and model
    api_key = ""
    model_name = "cerina"  # Could be "together" or "cerina"

    # Define your list of prompts
    prompts = [
        "Generate a summary of the latest AI research.",
        "Explain the benefits of using AI in healthcare."
    ]

    # Generate master prompt using the standalone function
    master_prompt = await create_master_prompt(
        api_key=api_key,
        model_name=model_name,
        prompts=prompts,
        connected=True,  # Set to True to enable passing info between prompts
        search=True  # Set to True to enable search functionality
    )

    print("Generated Master Prompt:", master_prompt)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing

We welcome contributions to LuciAI! If you're interested in improving the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Create a pull request.

## License

[![License: RevMaxx LLC Software License](https://img.shields.io/badge/license-RevMaxx%20LLC-blue.svg)](LICENSE)


