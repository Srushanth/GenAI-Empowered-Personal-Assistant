"""_summary_
This script serves as the main entry point for the GenAI Empowered Personal Assistant application.
It initializes the application, sets up the necessary configurations, and starts the user
interaction loop.
"""

from strands import tool
from strands import Agent
from strands.models.ollama import OllamaModel
from ddgs import DDGS

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="qwen3",  # Specify which model to use
)


@tool
def web_search(query: str, num_results: int = 5) -> str:
    """Executes a web search using DuckDuckGo and returns the results.

    Args:
        query (str): The search query to be executed.
        num_results (int, optional): _description_. Defaults to 5.

    Returns:
        str: A summary of the search results.
    """
    ddgs = DDGS()
    results = list(ddgs.text(query, max_results=num_results))
    summary = "\n".join([f"{item['title']} ({item['href']})" for item in results])
    return summary


search_agent = Agent(
    model=ollama_model,
    name="web_search_agent",
    system_prompt="You are a web research specialist retrieving current web results for queries.",
    tools=[web_search],
)

user_query = "What is the capital of india?"

# Explicitly call web_search
search_results = web_search(user_query)
print("Web search results:", search_results)

response = search_agent(user_query)
print("LLM response:", response)
