# Luci/Agents/agent.py

from Luci.Models.model import ChatModel
from Luci.Agents.medica_search_agent import MedicalSearchAgent
import os

class SearchTool:
    def __init__(self, email=None, max_results=10):
        """
        Initialize the SearchTool with necessary parameters.

        Args:
            email (str): Email address required by NCBI to use Entrez API.
            max_results (int): Maximum number of search results to retrieve.
        """
        if not email:
            raise ValueError("Email is required for SearchTool to access PubMed.")
        self.email = email
        self.max_results = max_results

    def search_medical_literature(self, query):
        """
        Search medical literature using MedicalSearchAgent.

        Args:
            query (str): The search query.

        Returns:
            list: List of articles.
        """
        search_agent = MedicalSearchAgent(email=self.email, max_results=self.max_results)
        articles = search_agent.search(query)
        return articles


class Agent:
    def __init__(self, name, objective, task, precautions, tool=None):
        """
        Initialize an Agent.

        Args:
            name (str): The name of the agent.
            objective (str): The objective of the agent.
            task (str): The task the agent is responsible for.
            precautions (str): Precautions the agent should follow.
            tool (object): Optional tool that the agent can use.
        """
        self.name = name
        self.objective = objective
        self.task = task
        self.precautions = precautions
        self.tool = tool
        self.connected_agents = {}  # Dictionary to hold connected agents

    @classmethod
    def built(cls, name, objective, task, precautions, tool=None):
        """
        Build and return an Agent instance.

        Args:
            name (str): The name of the agent.
            objective (str): The objective of the agent.
            task (str): The task the agent is responsible for.
            precautions (str): Precautions the agent should follow.
            tool (object): Optional tool that the agent can use.

        Returns:
            Agent: An instance of Agent.
        """
        return cls(name, objective, task, precautions, tool)

    def connect_agent(self, name, agent):
        """
        Connect another agent.

        Args:
            name (str): The name to assign to the connected agent.
            agent (Agent): The agent to connect.
        """
        self.connected_agents[name] = agent
        print(f"DEBUG: Connected agent '{name}' to '{self.name}'.")


    def get_connected_agent(self, name):
        """
        Retrieve a connected agent by name.

        Args:
            name (str): The name of the connected agent.

        Returns:
            Agent: The connected agent.
        """
        return self.connected_agents.get(name, None)

    def generate_final_answer(self, model, method, query):
        """
        Generate the final answer using the specified model and method.

        Args:
            model (str): The model name to use.
            method (str): The method to call from ChatModel.
            query (str): The final query.

        Returns:
            str: The generated answer.
        """
        print(f"DEBUG: Writer Agent '{self.name}' is generating the final answer.")
        # Construct the prompt incorporating objective, task, and precautions
        prompt = f"""
        Objective: {self.objective}
        Task: {self.task}
        Precautions: {self.precautions}

        Based on the following information, provide a detailed and accurate response.

        Information:
        \"\"\"
        {query}
        \"\"\"
        """

        chat_model = ChatModel(
            model_name=model,
            api_key=os.environ.get('API_KEY'),  # Ensure API_KEY is set
            prompt=prompt,
            SysPrompt=self.precautions
        )

        if hasattr(chat_model, method):
            method_to_call = getattr(chat_model, method)
            response = method_to_call()
            # Assume that the response has 'content' attribute or is a string
            if isinstance(response, dict) and 'content' in response:
                print("DEBUG: Writer Agent received response from ChatModel.")
                return response['content']
            elif hasattr(response, 'content'):
                print("DEBUG: Writer Agent received response content.")
                return response.content
            else:
                print("DEBUG: Writer Agent received response as string.")
                return str(response)
        else:
            print(f"DEBUG: Method '{method}' not found in ChatModel.")
            raise ValueError(f"Method '{method}' not found in ChatModel.")



class WriterAgent(Agent):
    def __init__(self, name, objective, task, precautions, tool=None):
        super().__init__(name, objective, task, precautions, tool)

    def generate_final_answer(self, model, method, query):
        """
        Generate the final answer using the specified model and method.

        Args:
            model (str): The model name to use.
            method (str): The method to call from ChatModel.
            query (str): The final query.

        Returns:
            str: The generated answer.
        """
        # Construct the prompt incorporating objective, task, and precautions
        prompt = f"""
        Objective: {self.objective}
        Task: {self.task}
        Precautions: {self.precautions}

        Based on the following information, provide a detailed and accurate response.

        Information:
        \"\"\"
        {query}
        \"\"\"
        """

        chat_model = ChatModel(
            model_name=model,
            api_key=os.environ.get('API_KEY'),  # Alternatively, pass as parameter
            prompt=prompt,
            SysPrompt=self.precautions
        )

        if hasattr(chat_model, method):
            method_to_call = getattr(chat_model, method)
            response = method_to_call()
            # Assume that the response has 'content' attribute or is a string
            if isinstance(response, dict) and 'content' in response:
                return response['content']
            elif hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        else:
            raise ValueError(f"Method '{method}' not found in ChatModel.")
