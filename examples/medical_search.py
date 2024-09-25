# medical_search_example.py

from Luci.Agents.medica_search_agent import MedicalSearchAgent

email = "wbavishek@gmail.com"
max_results = 5
query = "diabetes treatment guidelines"

agent = MedicalSearchAgent(email=email, max_results=max_results)
articles = agent.search(query)
agent.print_results(articles)

