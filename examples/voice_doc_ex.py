from Luci.Agents.voice_documentation_agent import VoiceDocumentationAgent

agent = VoiceDocumentationAgent(
    model_name='meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',  # Replace with your model name
    api_key='',   # Replace with your Together API key
    method='call_together'
)
agent.run()
