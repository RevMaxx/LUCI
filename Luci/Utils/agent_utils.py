import yaml
from Luci.Agents.agent import Agent, SearchTool
import os

def load_agent_from_yaml(yaml_path):
    """
    Load an agent configuration from a YAML file and instantiate the agent.

    Args:
        yaml_path (str): Path to the YAML configuration file.

    Returns:
        Agent: An instance of the Agent class configured with the YAML parameters.
    """
    # Check if the YAML file exists
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"The YAML file '{yaml_path}' does not exist. Please provide a valid path.")

    # Load the YAML file
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    # Determine if the 'agent' key exists
    if 'agent' in config:
        agent_config = config['agent']
    else:
        agent_config = config

    # Extract the agent's attributes from the YAML configuration
    name = agent_config.get('name')
    objective = agent_config.get('objective')
    task = agent_config.get('task')
    precautions = agent_config.get('precautions')
    tool_name = agent_config.get('tool', None)

    # Validate the essential attributes
    if not name or not objective or not task:
        raise ValueError(f"The YAML configuration is missing required fields. Ensure 'name', 'objective', and 'task' are provided in the YAML file '{yaml_path}'.")

    # Normalize 'precautions' to be a list
    if precautions is None:
        precautions = []
    elif isinstance(precautions, str):
        precautions = [precautions]
    elif isinstance(precautions, list):
        # Ensure all items in the list are strings
        if not all(isinstance(item, str) for item in precautions):
            raise ValueError("All items in the 'precautions' list must be strings.")
    else:
        raise ValueError("The 'precautions' field should be either a string or a list of strings.")

    # Instantiate the tool if specified
    if tool_name == "SearchTool":
        email = agent_config.get('email', None)  # Assuming email might be part of the config for SearchTool
        if email:
            tool = SearchTool(email=email)
        else:
            raise ValueError("SearchTool requires an 'email' parameter in the YAML configuration.")
    else:
        tool = None  # No tool specified or tool set to 'None'

    # Create and return the Agent instance
    agent = Agent.built(
        name=name,
        objective=objective,
        task=task,
        precautions=precautions,
        tool=tool
    )

    return agent
