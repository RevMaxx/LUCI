import asyncio
import aiohttp
from .gpt import Completion

class Agents:
    def __init__(self, name, task, goal):
        self.name = name
        self.task = task
        self.goal = goal

    async def template(self, query):
        """
        Create a prompt template using the agent's backstory and query.

        Args:
            query (str): The user's query.

        Returns:
            str: The formatted prompt template.
        """
        context = f"Agent Name: {self.name}\nTask: {self.task}\nGoal: {self.goal}\nQuery: {query}\n"
        
        if self.tools:
            tool_contexts = await asyncio.gather(*[tool.use_tool(query) for tool in self.tools])
            tool_context = "\n\n".join(tool_contexts)
            context += f"\n\nTools:\n{tool_context}"
        
        return context

    async def generate_response(self, query):
        """
        Generate a response using the agent's prompt template and query.

        Args:
            query (str): The user's query.

        Returns:
            str: The generated response from the GPT API.
        """
        prompt = await self.create_prompt_template(query)
        completion = Completion()
        response = await completion.create_async(prompt)
        return response


class CustomTool:
    def __init__(self, name, tool_logic):
        self.name = name
        self.tool_logic = tool_logic

    async def use_tool(self, query):
        """
        Use the custom tool with the given query.

        Args:
            query (str): The query to use with the custom tool.

        Returns:
            str: The result from the custom tool.
        """
        return await self.tool_logic(query)


class WebScraper:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url

    async def scrape(self, path):
        """
        Scrape content from the specified path on the base URL.

        Args:
            path (str): The path to scrape content from.

        Returns:
            str: The scraped content.
        """
        url = f"{self.base_url}{path}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f"Failed to scrape {url}. Status code: {response.status}")

    async def use_tool(self, query):
        """
        Use the web scraper as a tool to fetch and return content based on the query.

        Args:
            query (str): The query to determine the path for scraping.

        Returns:
            str: The result from the web scraper.
        """
        # For simplicity, let's assume the query is directly the path to scrape
        return await self.scrape(query)
