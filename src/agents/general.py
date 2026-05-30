from langchain_core.messages import SystemMessage, HumanMessage
from src.core.llm import get_senna_brain
from src.core.state import SennaState
from src.prompts import SENNA_SYSTEM_PROMPT

def general_chat_node(state: SennaState) -> dict:
    """
    Handles general conversation using the full Senna persona.
    """
    print("💬 Senna is thinking (General Chat)...")
    
    # 1. Get the Brain
    llm = get_senna_brain()
    
    # 2. Prepare the Messages
    # We always prepend the System Prompt to ensure she stays in character
    messages = [SystemMessage(content=SENNA_SYSTEM_PROMPT)] + state["messages"]
    
    # 3. Generate Response
    response = llm.invoke(messages)
    
    print("✨ Senna Responded.")
    
    # 4. Return the response to append to history
    return {"messages": [response]}