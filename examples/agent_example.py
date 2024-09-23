import asyncio
from Luci import *

# Define your tool logic as an async function
async def example_tool_logic(query):
    return f"Processed query: {query}"

async def main():
    custom_tool = CustomTool(name="Example Tool", tool_logic=example_tool_logic)
    web_scraper = WebScraper(name="Example Scraper", base_url="https://revmaxx.co")
    agent = Agents(name = "Medical Assistant", task = "Answer health queries", goal="Provide accurate health information")
    agent.tools = [custom_tool, web_scraper]  # Add tools to the agent

    query = "What are some health tips?"
    response = await agent.generate_response(query)

    print("Agent Response:", response)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
