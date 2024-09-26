import argparse
import asyncio
from Luci.Agents.soap import SoapAgent
from Luci.Utils.gpt import SyncGPTAgent
from Luci.Agents.voice_documentation_agent import VoiceDocumentationAgent
from Luci.Agents.medica_search_agent import MedicalSearchAgent  # Corrected import
from Luci.Agents.agent import Agent, WriterAgent, SearchTool 
from Luci import Search
from cerina import Completion
import os
from Luci.Utils.agent_utils import load_agent_from_yaml

async def generate_yaml_files(agent_name, objective, precautions, task):
    """
    Generate two YAML configuration files for the new agent using Cerina.

    Args:
        agent_name (str): Name of the agent.
        objective (str): Objective of the agent.
        precautions (str): Precautions the agent should follow.
        task (str): Task the agent is responsible for.
    """
    completion = Completion()

    # Prompt to generate research_agent.yaml
    research_prompt = f"""
    Create a YAML configuration file for a research agent named "{agent_name}_research". 
    The agent's objective is: "{objective}". 
    The agent's task is: "{task}". 
    Precautions to follow: "{precautions}".
    Include necessary fields such as name, objective, task, precautions, and tool (default to SearchTool).
    """
    research_response = completion.create(research_prompt)
    research_yaml = research_response

    # Prompt to generate writer_agent.yaml
    writer_prompt = f"""
    Create a YAML configuration file for a writer agent named "{agent_name}_writer". 
    The agent's objective is: "Compose a comprehensive summary based on the research findings." 
    The agent's task is: "Summarize the research articles into a coherent and concise summary." 
    Precautions to follow: "Maintain medical accuracy and clarity." 
    Include necessary fields such as name, objective, task, precautions, and tool (none by default).
    """
    writer_response = completion.create(writer_prompt)
    writer_yaml = writer_response

    # Define file paths
    agents_dir = os.path.join(os.getcwd(), "agents_configs")
    os.makedirs(agents_dir, exist_ok=True)
    research_yaml_path = os.path.join(agents_dir, f"{agent_name}_research.yaml")
    writer_yaml_path = os.path.join(agents_dir, f"{agent_name}_writer.yaml")

    # Save YAML files
    with open(research_yaml_path, 'w') as f:
        f.write(research_yaml)
    with open(writer_yaml_path, 'w') as f:
        f.write(writer_yaml)

    print(f"\n[YAML Files Generated]")
    print(f"1. Research Agent Configuration: {research_yaml_path}")
    print(f"2. Writer Agent Configuration: {writer_yaml_path}\n")
    print("You can now modify these YAML files as needed and use them to instantiate your agents.\n")

async def refine_and_generate_yaml(agent_name, objective, precautions, task):
    """
    Refine user inputs and generate two YAML configuration files using Cerina.

    Args:
        agent_name (str): Name of the agent.
        objective (str): Initial objective provided by the user.
        precautions (str): Initial precautions provided by the user.
        task (str): Initial task provided by the user.
    """
    completion = Completion()

    # Refine the objective, task, and precautions
    refinement_prompt = f"""
    Refine the following user inputs to make them more accurate, comprehensive, and aligned with the agent's purpose:

    1. Agent Name: {agent_name}
    2. Objective: {objective}
    3. Task: {task}
    4. Precautions: {precautions}
    5. Email: youremail@gmail.com

    Ensure that the objective is clear, the task is specific, the precautions are concise and effective with a list of precautions (if applicable), and recommend the most appropriate tool (e.g., SearchTool) based on the task.
    """
    refined_response = completion.create(refinement_prompt)
    refined_data = refined_response.strip()  # Extract the refined data

    # Use Cerina's API to convert the refined data into YAML format
    yaml_prompt = f"""
    Convert the following refined data into a YAML configuration file for an agent:

    Refined Data:
    {refined_data}

    Ensure the YAML includes the following fields: name, objective, task, precautions, and tool. Don't need to add yaml tag and backtick because it is saved as yaml file on the system.
    """
    yaml_response = completion.create(yaml_prompt)
    yaml_content = yaml_response.strip()

    # Define file paths
    agents_dir = os.path.join(os.getcwd(), "agents_configs")
    os.makedirs(agents_dir, exist_ok=True)
    research_yaml_path = os.path.join(agents_dir, f"{agent_name}_research.yaml")
    writer_yaml_path = os.path.join(agents_dir, f"{agent_name}_writer.yaml")

    # Save the generated YAML content
    with open(research_yaml_path, 'w') as f:
        f.write(yaml_content)

    # Similarly generate the writer YAML configuration
    writer_prompt = f"""
    Create a YAML configuration file for a writer agent named "{agent_name}_writer". 
    The agent's objective is: "Compose a comprehensive summary based on the research findings." 
    The agent's task is: "Summarize the research articles into a coherent and concise summary." 
    Precautions to follow: "Maintain medical accuracy and clarity." 
    Include necessary fields such as name, objective, task, precautions, and tool (none by default).
    Don't need to add yaml tag and backtick because it is saved as yaml file on the system.
    """
    writer_response = completion.create(writer_prompt)
    writer_yaml_content = writer_response.strip()

    with open(writer_yaml_path, 'w') as f:
        f.write(writer_yaml_content)

    print(f"\n[Refined YAML Files Generated]")
    print(f"1. Research Agent Configuration: {research_yaml_path}")
    print(f"2. Writer Agent Configuration: {writer_yaml_path}\n")
    print("You can now modify these YAML files as needed and use them to instantiate your agents.\n")

def create_refined_agent_yaml(args):
    """
    Handle the create_agent CLI command with prompt refinement.

    Args:
        args: Parsed CLI arguments.
    """
    asyncio.run(refine_and_generate_yaml(
        agent_name=args.name,
        objective=args.objective,
        precautions=args.precautions,
        task=args.task
    ))

def create_agent_yaml(args):
    """
    Handle the create_agent CLI command.

    Args:
        args: Parsed CLI arguments.
    """
    asyncio.run(generate_yaml_files(
        agent_name=args.name,
        objective=args.objective,
        precautions=args.precautions,
        task=args.task
    ))

def generate_soap_note(model, api_key, subjective, objective, assessment, plan, master_prompt, connected):
    soap_agent = SoapAgent(model_name=model, api_key=api_key, connected=connected)
    soap_agent.create_soap(
        model=model,
        api_key=api_key,
        S=subjective,
        O=objective,
        A=assessment,
        P=plan,
        M=master_prompt,
        connected=connected
    )

def sync_gpt_response(query):
    agent = SyncGPTAgent()
    response = agent.syncreate(query)
    return response

async def agentic_search(query: str, search_type: str = "text", async_search: bool = True, max_results: int = 10):
    """
    Perform agentic search based on the query, type of search (text/image), and mode (async/sync).

    Args:
        query (str): The query to search for.
        search_type (str): Specify "text" for text search or "image" for image search. Defaults to "text".
        async_search (bool): Whether to perform asynchronous search. Defaults to True.
        max_results (int): The maximum number of search results to return. Defaults to 10.

    Returns:
        list: A list of search results.
    """
    search = Search(query)
    
    if search_type == "text":
        if async_search:
            results = await search.search_text_async(max_results)
        else:
            results = search.search_text(max_results)
        search.print_text_result(results)
        
    elif search_type == "image":
        if async_search:
            results = await search.search_images_async(max_results)
        else:
            results = search.search_images(max_results)
        search.print_img_result(results)
    
    return results

def voice_documentation(model_name, api_key, method, stop_word):
    """
    Run the Voice Documentation Agent.

    Args:
        model_name (str): The name of the model to use.
        api_key (str): The API key for authentication.
        method (str): The method to call from ChatModel.
        stop_word (str): The word to say to stop recording.
    """
    agent = VoiceDocumentationAgent(
        model_name=model_name,
        api_key=api_key,
        method=method,
        stop_word=stop_word
    )
    agent.run()

def medical_search(query, email, max_results=10):
    """
    Run the Medical Search Agent to search PubMed.

    Args:
        query (str): The search query.
        email (str): Email address required by NCBI.
        max_results (int): Maximum number of results to fetch.
    """
    agent = MedicalSearchAgent(email=email, max_results=max_results)
    articles = agent.search(query)
    agent.print_results(articles)

def research_writer_agent(name, model, method, query, email):
    """
    Create and run a Research and Writer Agent.

    Args:
        name (str): Name of the Research Agent.
        model (str): The model name to use.
        method (str): The method to call from ChatModel.
        query (str): The research query.
        email (str): Email address required by NCBI.
    """
    # Make a Research Agent
    research_agent = Agent.built(
        name=f"{name}_research",
        objective="Gather the latest research on the specified medical topic.",
        task=query,  # The research task/query
        precautions="Do not hallucinate information; only use reputable medical journals and sources.",
        tool=SearchTool(email=email)
    )

    # Make a Writer Agent
    writer = Agent.built(
        name=f"{name}_writer",
        objective="Compose a comprehensive summary based on the research findings.",
        task="Summarize the research articles into a coherent and concise summary.",
        precautions="Maintain medical accuracy and clarity.",
        tool=None  # No specific tool needed for writing
    )

    # Connect the Writer Agent to the Research Agent
    research_agent.connect_agent('writer_agent', writer)

    # Generate the final answer using the connected Writer Agent
    final_answer = research_agent.generate_final_answer(model, method)

    print("Final Answer:")
    print(final_answer)

async def run_agent_from_yaml(yaml_path, model, method):
    """
    Run an agent based on the provided YAML configuration file with the specified model and method.

    Args:
        yaml_path (str): Path to the YAML configuration file.
        model (str): Model name to use.
        method (str): Method name to call.
    """
    agent = load_agent_from_yaml(yaml_path)

    # Check if this is a research agent that needs to connect to a writer agent
    if 'research' in agent.name.lower():
        writer_yaml_path = yaml_path.replace('_research.yaml', '_writer.yaml')
        if os.path.exists(writer_yaml_path):
            writer_agent = load_agent_from_yaml(writer_yaml_path)
            agent.connect_agent('writer_agent', writer_agent)
            print(f"Connected writer agent '{writer_agent.name}' to research agent '{agent.name}'.")

    print(f"Running agent '{agent.name}' with model '{model}' and method '{method}'...")

    # Run the agent and get the final answer
    final_answer = agent.generate_final_answer(model, method, query=None)
    print("\nFinal Output:")
    print(final_answer)

def main():
    parser = argparse.ArgumentParser(description="Healthcare Professional CLI Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Choose a command")

    # SOAP Note generator
    soap_parser = subparsers.add_parser("soap", help="Generate SOAP note")
    soap_parser.add_argument("--model", required=True, help="Model to use for generating the SOAP note")
    soap_parser.add_argument("--api-key", required=True, help="API Key for authentication")
    soap_parser.add_argument("--subjective", required=True, help="Subjective input for SOAP note")
    soap_parser.add_argument("--objective", required=True, help="Objective input for SOAP note")
    soap_parser.add_argument("--assessment", required=True, help="Assessment input for SOAP note")
    soap_parser.add_argument("--plan", required=True, help="Plan input for SOAP note")
    soap_parser.add_argument("--master-prompt", required=True, help="Master prompt for SOAP note")
    soap_parser.add_argument("--connected", action="store_true", help="Check if all sections are added")

    # GPT agent for other tasks
    gpt_parser = subparsers.add_parser("cerina", help="Get a response from cerina")
    gpt_parser.add_argument("query", help="Query to ask cerina")

    # Agentic search feature
    search_parser = subparsers.add_parser("search", help="Perform an agentic search")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--type", choices=["text", "image"], default="text", help="Specify search type (text or image)")
    search_parser.add_argument("--async-mode", action="store_true", help="Perform asynchronous search")
    search_parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results to fetch")

    # Voice Documentation feature
    voice_doc_parser = subparsers.add_parser("voice_doc", help="Run the Voice Documentation Agent")
    voice_doc_parser.add_argument("--model-name", required=True, help="Name of the model to use")
    voice_doc_parser.add_argument("--api-key", required=True, help="API Key for authentication")
    voice_doc_parser.add_argument("--method", default="call_gpt", help="Method to call from ChatModel")
    voice_doc_parser.add_argument("--stop-word", default="stop", help="Word to say to stop recording")

    # Research and Writer Agent feature
    research_writer_parser = subparsers.add_parser("research_writer", help="Run a Research and Writer Agent")
    research_writer_parser.add_argument("--name", required=True, help="Name of the Research Agent")
    research_writer_parser.add_argument("--model", required=True, help="Model to use for generating the final answer")
    research_writer_parser.add_argument("--method", default="call_gpt", help="Method to call from ChatModel")
    research_writer_parser.add_argument("--query", required=True, help="Research query")
    research_writer_parser.add_argument("--email", required=True, help="Your email address (required by NCBI)")

    # Create Agent feature
    create_agent_parser = subparsers.add_parser("create_agent", help="Create a new agent by specifying name, objective, precautions, and task")
    create_agent_parser.add_argument("--name", required=True, help="Name of the new agent")
    create_agent_parser.add_argument("--objective", required=True, help="Objective of the agent")
    create_agent_parser.add_argument("--precautions", required=True, help="Precautions the agent should follow")
    create_agent_parser.add_argument("--task", required=True, help="Task the agent is responsible for")

    # Medical Search feature
    med_search_parser = subparsers.add_parser("medsearch", help="Perform a medical literature search")
    med_search_parser.add_argument("query", help="Search query")
    med_search_parser.add_argument("--email", required=True, help="Your email address (required by NCBI)")
    med_search_parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results to fetch")

    # Add the refined create_agent subparser
    create_refined_agent_parser = subparsers.add_parser("refined_agent", help="Create a new agent with refined prompts, using AI-driven enhancement.")
    create_refined_agent_parser.add_argument("--name", required=True, help="Name of the new agent")
    create_refined_agent_parser.add_argument("--objective", required=True, help="Objective of the agent")
    create_refined_agent_parser.add_argument("--precautions", required=True, help="Precautions the agent should follow")
    create_refined_agent_parser.add_argument("--task", required=True, help="Task the agent is responsible for")

    # Add the run_agent subparser with model and method options
    run_agent_parser = subparsers.add_parser("run_agent", help="Run an agent from a YAML configuration file")
    run_agent_parser.add_argument("--yaml-path", required=True, help="Path to the YAML configuration file")
    run_agent_parser.add_argument("--model", required=True, help="Model name to use (e.g., gpt-3.5-turbo)")
    run_agent_parser.add_argument("--method", required=True, help="Method to call (e.g., call_gpt)")

    args = parser.parse_args()

    if args.command == "soap":
        generate_soap_note(
            model=args.model,
            api_key=args.api_key,
            subjective=args.subjective,
            objective=args.objective,
            assessment=args.assessment,
            plan=args.plan,
            master_prompt=args.master_prompt,
            connected=args.connected
        )
    elif args.command == "cerina":
        response = sync_gpt_response(args.query)
        print(f"Medical Assistant: {response}")
    elif args.command == "search":
        # Run agentic search asynchronously if --async-mode is passed
        if args.async_mode:
            asyncio.run(agentic_search(query=args.query, search_type=args.type, async_search=True, max_results=args.max_results))
        else:
            asyncio.run(agentic_search(query=args.query, search_type=args.type, async_search=False, max_results=args.max_results))
    elif args.command == "voice_doc":
        voice_documentation(
            model_name=args.model_name,
            api_key=args.api_key,
            method=args.method,
            stop_word=args.stop_word
        )
    elif args.command == "research_writer":
        research_writer_agent(
            name=args.name,
            model=args.model,
            method=args.method,
            query=args.query,
            email=args.email
        )

    elif args.command == "medsearch":
        medical_search(
            query=args.query,
            email=args.email,
            max_results=args.max_results
        )
    elif args.command == "refined_agent":
        create_refined_agent_yaml(args)

    elif args.command == "create_agent":
        create_agent_yaml(args)

    elif args.command == "run_agent":
        asyncio.run(run_agent_from_yaml(args.yaml_path, args.model, args.method))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
