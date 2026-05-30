from src.agents.orchestrator import router_node
from langchain_core.messages import HumanMessage

def test_router_logic():
    # Test Case 1: Government Request
    print("\n--- TEST 1: Government Context ---")
    state_gov = {"messages": [HumanMessage(content="I need to initiate a requisition for the DEI workshop under PPDA rules.")]}
    result_gov = router_node(state_gov)
    assert result_gov["current_intent"] == "GOV_FLOW"
    
    # Test Case 2: Corporate Request
    print("\n--- TEST 2: Corporate Context ---")
    state_corp = {"messages": [HumanMessage(content="Find me a cheap venue for the Suit Republic launch party.")]}
    result_corp = router_node(state_corp)
    assert result_corp["current_intent"] == "CORP_FLOW"
    
    # Test Case 3: Hello
    print("\n--- TEST 3: General Chat ---")
    state_chat = {"messages": [HumanMessage(content="Hi Senna, good morning.")]}
    result_chat = router_node(state_chat)
    assert result_chat["current_intent"] == "GENERAL_CHAT"

    print("\n✅ All Routing Tests Passed!")

if __name__ == "__main__":
    test_router_logic()