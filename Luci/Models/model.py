import os
from openai import OpenAI
import asyncio
from openai import AzureOpenAI
import together
from together import AsyncTogether, Together

class ChatModel:
    def __init__(self, model_name, api_key, prompt, SysPrompt=None):
        self.model_name = model_name or os.environ.get('model_name')
        if self.model_name is None:
            raise ValueError("Model Name has not been set! Kindly provide a valid model name.")
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Kindly provide a valid openai key!")
        self.prompt = prompt
        if not prompt:
            raise ValueError("Provide a prompt to proceed..")
        self.client = OpenAI(api_key=self.api_key)
        self.SysPrompt = SysPrompt or "system"

    def call_gpt(self, messages=None, stream=False):
        if messages is None:
            messages = [
                {"role": "Medical AI", "content": "You are an advanced medical AI"},
                {"role": self.SysPrompt, "content": self.prompt}
            ]

        if not stream:
            # Non-streaming case
            result = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return result.choices[0].message.content  # Return the message content directly
        else:
            # Streaming case
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True  # Enable streaming
            )
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
            return full_response  # Return the full accumulated response



    async def call_azure(self, api_version, api_base, deployment_name):
        api_version = os.environ.get('api_version')
        api_base = os.environ.get('api_base')
        deployment_name = os.environ.get('deployment_name')
        if api_version or api_base or deployment_name is None:
            raise ValueError("Missing {name} azure key parameters!")
        
        client = AzureOpenAI(
            api_key=self.api_key,  
            azure_endpoint=api_base,
            api_version=api_version
        )

        try:
            response = await asyncio.to_thread(
                client.chat.completions.create(
                    model=deployment_name,
                    messages=[
                        {"role": "system", "content": "Advanced Medical AI Agent"},
                        {"role": "user", "content": self.prompt}
                    ]
                )
            )

            # print the response
            return response.choices[0].message.content

        except client.AuthenticationError as e:
            # Handle Authentication error here, e.g. invalid API key
            return f"API returned an Authentication Error: {e}"
        
    def call_azure_sync(self, api_version, api_base, deployment_name):
        api_version = os.environ.get('api_version')
        api_base = os.environ.get('api_base')
        deployment_name = os.environ.get('deployment_name')
        if api_version or api_base or deployment_name is None:
            raise ValueError("Missing {name} azure key parameters!")
        
        client = AzureOpenAI(
            api_key=self.api_key,  
            azure_endpoint=api_base,
            api_version=api_version
        )

        try:
            response = client.chat.completions.create(
                            model=deployment_name,
                            messages=[
                                {"role": "system", "content": "Advanced Medical AI Agent"},
                                {"role": self.SysPrompt, "content": self.prompt}
                                ]
                            )
            
            # print the response
            return response.choices[0].message.content

        except client.AuthenticationError as e:
            # Handle Authentication error here, e.g. invalid API key
            return f"API returned an Authentication Error: {e}"

    
    def call_together(self):

        client = Together(api_key=self.api_key)

        messages = [
        {"role": "system", "content": "Advanced Medical AI Agent"},
        {"role": "user", "content": self.prompt}
        ]
        response = client.chat.completions.create(
        model=self.model_name,
        messages=messages,
        )
        return response.choices[0].message 