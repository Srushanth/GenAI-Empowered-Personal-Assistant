"""_summary_
This script serves as the main entry point for the GenAI Empowered Personal Assistant application.
It initializes the application, sets up the necessary configurations, and starts the user
interaction loop.
"""

from strands import tool
from strands import Agent
from llama_index.readers.google.calendar.base import GoogleCalendarReader

google_calendar_reader = GoogleCalendarReader()
