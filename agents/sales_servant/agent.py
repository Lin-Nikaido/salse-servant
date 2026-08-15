# Copyright (c) 2025 YourIndependence. All rights reserved.
#
# This software is the confidential and proprietary information of
# YourIndependence. Unauthorized copying, distribution,
# modification, or use outside the organization is strictly prohibited.
#
# For internal use only.
# developer team.

"""root agent"""

from google.adk.agents import Agent

from .prompts import instruction


root_agent = Agent(
    name="chat_agent",
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    instruction=instruction,
)
