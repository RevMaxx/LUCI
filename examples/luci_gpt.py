from Luci.Utils import gpt

# Using the async GPTAgent
async def use_gpt_agent():
    agent = gpt.GPTAgent()
    query = "Explain the process of photosynthesis."
    
    # Get async response
    response = await agent.create(query)
    print("Async Response:", response)
# Using the sync GPTAgent
def use_sync_gpt_agent():
    agent = gpt.SyncGPTAgent()
    query = "What is the capital of France?"
    
    # Get sync response
    response = agent.syncreate(query)
    print("Sync Response:", response)