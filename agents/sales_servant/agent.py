"""
root agent
"""
from google.adk.agents import Agent

from .prompts import instruction

root_agent = Agent(
    name="chat_agent",
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    instruction=instruction,
)
