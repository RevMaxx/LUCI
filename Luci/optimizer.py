import aiohttp
from typing import Optional
from .gpt import Completion

class PromptOptimizer:
    def __init__(self, model: Optional[str] = None, token: Optional[str] = None):
        self.completion = Completion(model=model, token=token)

    async def optimize_prompt(self, prompt: str) -> str:
        """
        Optimize the given prompt using the GPT API.

        Args:
            prompt (str): The prompt to optimize.

        Returns:
            str: The optimized prompt.
        """
        optimized_prompt = await self.create_async(prompt)
        return optimized_prompt

    async def create_async(self, prompt: str) -> str:
        """
        Create a response using the GPT API.

        Args:
            prompt (str): The prompt to send to the GPT API.

        Returns:
            str: The response from the GPT API.
        """
        return await self.completion.create_async(prompt)