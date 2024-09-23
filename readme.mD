## LUCI 

The first AI-based medical agent designed to automate all medical processes.

## Installation

```bash
pip install LuciAI
```

## Usage

## Chain Agents

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
```

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```

## Searching any Query

```python
from Luci.Agents import Search

query = "Revmaxx LLC"
search_instance = Search(query)

results = search_instance.search_text(max_results=5)
search_instance.print_text_result(results)
```

## Get the JSON Response of the Search Query

```python
from Luci import search_text

query="Recent trends of AI?"

print(search_text(query, max_results=3))
```

## Search any Image

```python
from Luci import Search

query = "Your Query ?"
search_instance = Search(query)

results = search_instance.search_images(max_results=5)
search_instance.print_text_result(results)
```

## Generate SOAP Notes

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

## Contributing

We welcome contributions to LuciAI! If you're interested in improving the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Create a pull request.

## License

[![License: RevMaxx LLC Software License](https://img.shields.io/badge/license-RevMaxx%20LLC-blue.svg)](LICENSE)


