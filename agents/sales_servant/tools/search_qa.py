# Copyright (c) 2025 YourIndependence. All rights reserved.
#
# This software is the confidential and proprietary information of
# YourIndependence. Unauthorized copying, distribution,
# modification, or use outside the organization is strictly prohibited.
#
# For internal use only.
# developer team.

"""
QA search tool
"""


from typing import List

from pydantic import BaseModel
from pydantic import Field


class QaAnswer(BaseModel):
    question: str = Field(..., description="Question")
    answer: str = Field(..., description="Answer")

class QaAnswers(BaseModel):
    qas: List[QaAnswer]


def search_q_and_a(query: str) -> QaAnswers:
    """Search QA and Answers.
    You should use this tool when, the Customer

    Args:
        query: The search query.

    Returns:

    """
