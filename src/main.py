"""_summary_
This script serves as the main entry point for the GenAI Empowered Personal Assistant application.
It initializes the application, sets up the necessary configurations, and starts the user
interaction loop.
"""

import gradio as gr
from strands import tool, Agent
from strands.models.ollama import OllamaModel
from ddgs import DDGS


# Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen3",
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


def assistant_pipeline(user_query: str):
    # Run web search to get live results
    search_results = web_search(user_query)

    # Call the LLM agent to generate a response
    llm_response = search_agent(user_query)

    # Return both outputs for display
    return llm_response, search_results


# Gradio UI
iface = gr.Interface(
    fn=assistant_pipeline,
    inputs=gr.Textbox(label="Enter your query"),
    outputs=[gr.Textbox(label="LLM Response"), gr.Textbox(label="Web Search Results")],
    title="GenAI Empowered Personal Assistant",
    description="Ask a question and get both AI-generated and live web search answers.",
)

if __name__ == "__main__":
    iface.launch()
