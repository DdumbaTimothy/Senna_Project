from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition
from src.agents.corp.manager import manager_node, tool_node
from src.core.state import SennaState
from src.agents.orchestrator import router_node
from src.agents.general import general_chat_node
from src.agents.gov.guardian import guardian_node

def build_graph():
    workflow = StateGraph(SennaState)

    # 1. Add Nodes
    workflow.add_node("router", router_node)
    workflow.add_node("general_chat", general_chat_node)
    workflow.add_node("corp_agent", manager_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("gov_agent", guardian_node)

    # 2. Entry Point
    workflow.set_entry_point("router")

    # 3. Router Logic (FIXED HERE)
    workflow.add_conditional_edges(
        "router",
        lambda state: state["current_intent"],
        {
            "GOV_FLOW": "gov_agent",        # <--- NOW POINTS TO REAL AGENT
            "CORP_FLOW": "corp_agent",
            "GENERAL_CHAT": "general_chat"
        }
    )

    # 4. The "Manager" Logic
    workflow.add_conditional_edges(
        "corp_agent",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )

    # 5. The "Tool" Logic
    workflow.add_edge("tools", "corp_agent")

    # 6. Exit Points
    workflow.add_edge("general_chat", END)
    workflow.add_edge("gov_agent", END) # Gov agent stops after audit (for now)

    return workflow.compile()