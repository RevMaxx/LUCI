from Luci.Agents.soap import *

model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
api_key = "aea3aab7b8275c73f7b171588bf030cf6f0e51f8c638f1bfb8ffbe919332d99d" # or pass directly from user input
    
S = "Patient reports mild headache and fatigue."
O = "Blood pressure is 120/80, heart rate is 75 bpm."
A = "Likely mild dehydration."
P = "Recommend increasing fluid intake, rest, and monitor symptoms."
M = "Generate a detailed SOAP note based on the inputs."

    # Create an instance of the SoapAgent class
soap_agent = SoapAgent(model_name=model_name, api_key=api_key, connected=True)
soap_agent.create_soap(S, O, A, P, M)