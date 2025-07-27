"""_summary_
This script serves as the main entry point for the GenAI Empowered Personal Assistant application.
It initializes the application, sets up the necessary configurations, and starts the user
interaction loop.
"""

from strands import tool
from strands import Agent
from duckduckgo_search import DDGS


def web_search(query: str, num_results: int = 5):
    """_summary_

    Args:
        query (str): _description_
        num_results (int, optional): _description_. Defaults to 5.

    Returns:
        _type_: _description_
    """
    ddgs = DDGS()
    return ddgs.text(query, max_results=num_results)


search_agent = Agent()
