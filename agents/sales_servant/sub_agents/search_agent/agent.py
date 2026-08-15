"""
search agent
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

search_agent = Agent(
    name="search_agent",
    model="gemini-flash-latest",
    description=(
        "Web検索を使って、最新情報や外部情報を調査するエージェント。"
    ),
    instruction=(
        "ユーザーの依頼に必要な情報を検索し、"
        "根拠を明確にして結果を返してください。"
    ),
    tools=[google_search],
)