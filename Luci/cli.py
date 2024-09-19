import argparse
from Luci.Agents.soap import create_soap
from Luci.gpt import SyncGPTAgent

def generate_soap_note(model, api_key, subjective, objective, assessment, plan, master_prompt, connected):
    create_soap(
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
    gpt_parser = subparsers.add_parser("gpt", help="Get a response from LUCIGPT")
    gpt_parser.add_argument("query", help="Query to ask GPT")

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
    elif args.command == "gpt":
        response = sync_gpt_response(args.query)
        print(f"GPT Response: {response}")

if __name__ == "__main__":
    main()
