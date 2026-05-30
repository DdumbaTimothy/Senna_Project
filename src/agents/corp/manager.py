from langchain_core.messages import SystemMessage
from src.core.llm import get_senna_brain
from src.core.state import SennaState
from src.tools.market import get_market_search_tool
from langgraph.prebuilt import ToolNode

# 1. Initialize Tools
tools = [get_market_search_tool()]
# This creates a "Node" that can actually run the tool
tool_node = ToolNode(tools)

# The "Hustler" Persona (Same as before)
MANAGER_PROMPT = """
You are the **Corporate Operations Manager** node of Senna.
Your goal is **Operational Velocity** and **Fair Value**.

**Your Playbook:**
1. **Analyze:** Check if you have the "Trinity" (Budget, Date, Pax).
2. **Action:** - If missing info -> Ask the user.
   - If you have info -> USE THE 'market_research' TOOL to find options.
   - If you have results -> Summarize them with prices.

**Output Style:**
- Be crisp.
- If you use the tool, just output the tool call. Do not narrate "I am searching now."
"""

def manager_node(state: SennaState) -> dict:
    """
    The Real Corporate Agent logic with TOOLS.
    """
    print("💼 Senna Manager is thinking (with Tools)...")
    
    # 1. Get the Brain and BIND the tools
    llm = get_senna_brain()
    llm_with_tools = llm.bind_tools(tools)
    
    # 2. Contextualize
    messages = [SystemMessage(content=MANAGER_PROMPT)] + state["messages"]
    
    # 3. Think
    response = llm_with_tools.invoke(messages)
    
    # 4. Return the response
    return {"messages": [response]}