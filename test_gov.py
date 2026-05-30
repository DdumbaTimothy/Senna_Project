from src.graph import build_graph
from langchain_core.messages import HumanMessage

def test_corruption_block():
    app = build_graph()
    
    # 1. The Corrupt Request
    prompt = "I want to buy an HP Laptop for 5,000,000 UGX."
    print(f"\n👤 User (Ministry): {prompt}")
    
    inputs = {
        "messages": [HumanMessage(content=prompt)],
        "user_role": "GOV",
        "current_intent": "GOV_FLOW" # Force routing for test speed
    }
    
    print("🚀 Starting Audit...")
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"👉 Node Reached: {key}")
            if "messages" in value:
                # Handle tuple or object
                content = value["messages"][-1]
                if isinstance(content, tuple): print(f"   💬 Reply: {content[1]}")
                else: print(f"   💬 Reply: {content}")

if __name__ == "__main__":
    test_corruption_block()