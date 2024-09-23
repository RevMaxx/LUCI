from Luci.Utils import gpt

# Using the sync GPTAgent
def use_sync_gpt_agent():
    agent = gpt.SyncGPTAgent()
    query = "What is the capital of France?"
    
    # Get sync response
    response = agent.syncreate(query)
    print("Sync Response:", response)