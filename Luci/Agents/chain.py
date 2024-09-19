import os
import re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from cerina import Completion, print_search_results, search_text
from Luci.Agents.search import *

class ChainAgent:
    def __init__(self, model_name, api_key, connected=False, search=False):
        self.api_key = api_key
        self.model_name = model_name
        self.connected = connected
        self.search = search
        self.model = None
        self.output_parser = StrOutputParser()
        
        if model_name == "cerina":
            self.completion = Completion()
        else:
            self.model = ChatTogether(together_api_key=self.api_key, model=self.model_name)

    def generate_prompt(self, prompt_text):
        if self.search:
            return self.perform_search(prompt_text)
        
        if isinstance(self.model, Completion):
            response = self.model.create(prompt_text)
        else:
            prompt_template = ChatPromptTemplate.from_template(prompt_text)
            prompt_chain = prompt_template | self.model | self.output_parser
            
            # Check if connected is true to pass info between prompts
            if self.connected:
                for chunk in prompt_chain.stream({"input": prompt_text}):
                    print(chunk, end="", flush=True)
            else:
                response = prompt_chain({"input": prompt_text})
                return response

    def perform_search(self, query):
        # This is where you could integrate an external search functionality
        search_instance = Search(query)
        results = search_instance.search_text(max_results=5)
        return search_instance.print_text_result(results)
        
    def execute(self, prompts):
        master_prompt = ""
        for prompt in prompts:
            response = self.generate_prompt(prompt)
            if self.connected:
                # Modify the response to connect with the next prompt
                master_prompt += response
            else:
                print(f"Response for prompt '{prompt}': {response}")
        return master_prompt

# Developer can pass multiple prompts
def create_master_prompt(api_key, model_name, prompts, connected=False, search=False):
    agent = ChainAgent(model_name=model_name, api_key=api_key, connected=connected, search=search)
    return agent.execute(prompts)

