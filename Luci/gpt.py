import asyncio
from cerina import collections

class GPTAgent:
    def __init__(self):
        self.completion = Completion()
        
    async def create(self, query):
        response = await self.completion.create_async(query)
        return response
    

class SyncGPTAgent:
    def __init__(self):
        self.completion = Completion()
    
    def syncreate(self, query: str) -> str:
        try:
            response = self.completion.create(query)
            return response
        except Exception as e:
            return f"An error occurred: {e}"

    


