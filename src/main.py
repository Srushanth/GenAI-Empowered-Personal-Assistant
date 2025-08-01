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


def assistant_chatbot(message, history):
    """
    Chatbot function for Gradio ChatInterface.
    Accepts the latest user message and the chat history.
    Returns the assistant's response (LLM) and appends web search results as a reference.
    """
    # Run web search to get live results
    search_results = web_search(message)

    # Call the LLM agent to generate a response
    llm_response = search_agent(message)

    # Optionally, append web search results as a reference in the chat
    response = f"{llm_response}\n\n---\n**Web Search Results:**\n{search_results}"
    return response


# Gradio ChatInterface
iface = gr.ChatInterface(
    fn=assistant_chatbot,
    title="GenAI Empowered Personal Assistant",
    description=(
        "Chat with your AI assistant. Each answer includes both an AI-generated response "
        "and live web search results."
    ),
    textbox=gr.Textbox(placeholder="Ask anything...", label="Your message"),
)

if __name__ == "__main__":
    iface.launch()
