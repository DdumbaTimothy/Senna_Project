from typing import TypedDict, List, Annotated
import operator
from langchain_core.messages import BaseMessage

class SennaState(TypedDict):
    """
    The Global State of the conversation.
    This dict is passed to every agent in the swarm.
    """
    # Messages: The chat history. 'operator.add' means we append new messages, not overwrite.
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Context: Who is the user?
    user_role: str  # 'GOV' or 'CORP'
    user_id: str    # The User's ID (for database lookup)
    
    # Task Tracking: What are we doing?
    current_intent: str # 'BOOKING', 'COMPLIANCE', 'MARKETING', 'GENERAL'
    task_status: str    # 'PENDING', 'IN_PROGRESS', 'WAITING_APPROVAL'
    
    # The Negotiation Loop Variables
    vendor_price: float
    target_price: float
    negotiation_round: int