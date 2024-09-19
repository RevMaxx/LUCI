import os
import re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether

class SoapAgent:
    def __init__(self, model_name, api_key, connected=False):
        self.api_key = api_key
        self.model_name = model_name
        self.connected = connected
        self.model = ChatTogether(together_api_key=self.api_key, model=self.model_name)
        self.output_parser = StrOutputParser()
    
    def validate_prompts(self, S, O, A, P):
        # Check if all required sections are present
        if self.connected:
            missing_sections = []
            if not S:
                missing_sections.append("Subjective")
            if not O:
                missing_sections.append("Objective")
            if not A:
                missing_sections.append("Assessment")
            if not P:
                missing_sections.append("Plan")
            
            if missing_sections:
                raise ValueError(f"Missing sections: {', '.join(missing_sections)}")
        return True
    
    def create_soap(self, S, O, A, P, M):
        try:
            # Validate that all necessary sections are filled
            self.validate_prompts(S, O, A, P)

            # Master prompt template
            prompt_template = f"""
            Subjective: {S}
            Objective: {O}
            Assessment: {A}
            Plan: {P}
            
            Instructions: {M}
            """

            # Set up the prompt template for Langchain
            soap_prompt = ChatPromptTemplate.from_template(prompt_template)
            soap_prompt_chain = soap_prompt | self.model | self.output_parser

            # Stream the response in chunks
            for chunk in soap_prompt_chain.stream({"input": "Generate SOAP Note"}):
                print(chunk, end="", flush=True)

        except Exception as e:
            print(f"Error: {e}")