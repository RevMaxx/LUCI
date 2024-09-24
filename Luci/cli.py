import argparse
from Luci.Agents.soap import SoapAgent
from Luci.Utils.gpt import SyncGPTAgent
import asyncio
from Luci import Search

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
    search_parser.add_argument("--async-mode", action="store_true", help="Perform asynchronous search")  # Renamed from --async
    search_parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results to fetch")

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
        if args.async_mode:  # Changed from args.async to args.async_mode
            asyncio.run(agentic_search(query=args.query, search_type=args.type, async_search=True, max_results=args.max_results))
        else:
            asyncio.run(agentic_search(query=args.query, search_type=args.type, async_search=False, max_results=args.max_results))

if __name__ == "__main__":
    main()
