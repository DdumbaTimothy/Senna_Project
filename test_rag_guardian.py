from src.graph import build_graph
from langchain_core.messages import HumanMessage

def test_namayingo_audit():
    app = build_graph()
    
    # 1. The Corrupt Request (Overpaying Per Diem)
    # The Budget says 140,000. We ask for 500,000.
    query = "I want to process a per diem for Makumbi Moses for the Namayingo activity at 500,000 UGX per night."
    
    print(f"\n👤 User (GOV): {query}")
    
    inputs = {
        "messages": [HumanMessage(content=query)],
        "user_role": "GOV",
        "current_intent": "GOV_FLOW"
    }
    
    print("🚀 Starting RAG Audit (Consulting 'QUARTER TWO DRAFT BUDGETS 2025')...")
    for output in app.stream(inputs):
        for key, value in output.items():
            if "messages" in value:
                content = value["messages"][-1].content
                print(f"\n🤖 Senna ({key}):\n{content}")

if __name__ == "__main__":
    test_namayingo_audit()