"""
root agent
"""
from google.adk.agents import Agent

root_agent = Agent(
    name="chat_agent",
    model="gemini-flash-latest",
    instruction="ユーザーの質問に日本語で回答してください。",
)