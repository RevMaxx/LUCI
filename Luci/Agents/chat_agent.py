from Luci.Models.model import ChatModel

class ChatAgent:
    def __init__(self, model_name, api_key, prompt, SysPrompt=None):
        self.chat_model = ChatModel(model_name, api_key, prompt, SysPrompt)

    async def get_response(self, messages=None, stream=False):
        return await self.chat_model.call_openai(messages, stream)

    def get_gpt_response(self, messages=None, stream=False):
        return self.chat_model.call_gpt(messages, stream)

    async def get_azure_response(self, api_version, api_base, deployment_name):
        return await self.chat_model.azure_openai(api_version, api_base, deployment_name)

    def get_together_response(self):
        return self.chat_model.together_ai()