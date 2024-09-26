from Luci import Agent, SearchTool
import os  # Import os to set environment variables

# User-defined parameters
query = "diabetes treatment guidelines"  # Final Query
model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"  # Choose a model name
method = "call_together"  # Choose a ChatModel method (corrected)
email = "wbavishek@gmail.com"

# Set the API_KEY environment variable
os.environ['API_KEY'] = ""

# Make a Research Agent
research_agent = Agent.built(
    name="ResearchAgent",
    objective="Gather the latest research on diabetes treatment guidelines.",
    task=query,  # The research task/query
    precautions="Do not hallucinate information; only use reputable medical journals and sources.",
    tool=SearchTool(email=email)
)

# Make a Writer Agent
writer = Agent.built(
    name="WriterAgent",
    objective="Compose a comprehensive summary based on the research findings.",
    task="Summarize the diabetes treatment guidelines based on the provided research.",
    precautions="Maintain medical accuracy and clarity.",
    tool=None  # No specific tool needed for writing
)

# Connect the Writer Agent to the Research Agent
research_agent.connect_agent('writer_agent', writer)

# Generate the final answer using the connected Writer Agent 
# This uses the Research Agent's task as the query for the Writer Agent
final_answer = research_agent.generate_final_answer(model, method, query)

print("Final Answer:")
print(final_answer)
