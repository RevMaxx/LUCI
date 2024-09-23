import os
import re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from cerina import Completion, search_text
from Luci.Agents.search import *

class ChainAgent:
    def __init__(self, model_name, api_key=None, connected=False, search=False):
        self.model_name = model_name
        self.connected = connected
        self.search = search
        self.model = None
        self.output_parser = StrOutputParser()

        # Handle API key only if the model is not Cerina
        if model_name != "cerina":
            self.api_key = api_key or os.environ.get("api_key")
            if not self.api_key:
                raise NameError("api_key is missing!")
            self.model = ChatTogether(together_api_key=self.api_key, model=self.model_name)
        else:
            self.model = Completion()

        if not model_name:
            raise ValueError("Model name has not been mentioned!")

    async def generate_prompt(self, prompt_text):
        # If search=True, perform search on the first prompt
        if self.search:
            search_res = self.perform_search(prompt_text)
            return search_res

        # Handle prompt generation for the model
        if isinstance(self.model, Completion):
            response = self.model.create(prompt_text)
            print(f"[DEBUG] Response from Completion model: {response}")
            return response
        else:
            prompt_template = ChatPromptTemplate.from_template(prompt_text)
            prompt_chain = prompt_template | self.model | self.output_parser

            # Streaming logic when connected=True
            if self.connected:
                result = ""
                print(f"[DEBUG] Starting streaming for prompt: {prompt_text}")
                async for chunk in prompt_chain.stream({"input": prompt_text}):
                    print(f"[DEBUG] Received chunk: {chunk}")
                    print(chunk, end="", flush=True)
                    result += chunk  # Accumulate chunks into result
                return result  # Return accumulated result
            else:
                # Handle non-streaming response
                response = await prompt_chain({"input": prompt_text})
                return response if response is not None else ""

    def perform_search(self, query):
        # Integrate an external search functionality
        results = search_text(query, max_results=5)  # Fetch search results
        return results  # Return the raw results instead of processing them

    async def execute(self, prompts):
        master_prompt = ""
        for prompt in prompts:
            response = await self.generate_prompt(prompt)
            
            # Initialize a variable for the synthesized content
            synthesized_content = []

            if self.search:  # Check if search is enabled
                search_results = self.perform_search(prompt)  # Get search results
                # Synthesize the search results into a more cohesive narrative
                synthesized_content.append(f"Based on the latest findings, here are some insights regarding '{prompt}':\n")
                for result in search_results:
                    title = result.get('title', 'No Title')
                    body = result.get('body', 'No Body')
                    synthesized_content.append(f"- {body} (Source: {title})")

            if response:  # Check if response is not None or empty
                synthesized_content.append(f"\nAdditionally, considering the prompt '{prompt}', we can say: {response}")

            # Join synthesized content into a structured format
            master_prompt += "\n".join(synthesized_content) + "\n\n"

        return master_prompt.strip()  # Return the final structured prompt


# Make api_key optional with a default value of None
async def create_master_prompt(model_name, prompts, api_key=None, connected=False, search=False):
    # Pass None as api_key if model_name is "cerina"
    if model_name == "cerina":
        api_key = None
    agent = ChainAgent(model_name=model_name, api_key=api_key, connected=connected, search=search)
    return await agent.execute(prompts)
