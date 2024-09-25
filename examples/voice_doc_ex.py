from Luci.Agents.voice_documentation_agent import VoiceDocumentationAgent

agent = VoiceDocumentationAgent(
    model_name='meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',  # Replace with your model name
    api_key='aea3aab7b8275c73f7b171588bf030cf6f0e51f8c638f1bfb8ffbe919332d99d',   # Replace with your Together API key
    method='call_together'
)
agent.run()
