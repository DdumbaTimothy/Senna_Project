from src.graph import build_graph
from langchain_core.messages import HumanMessage

def test_senna_flow():
    app = build_graph()
    
    print("\n--- TEST: Waking up the full organism ---")
    
    # Simulation 1: A Greeting
    print("\n👤 User: Hello Senna!")
    inputs = {"messages": [HumanMessage(content="Hello Senna!")], "user_role": "CORP"}
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"   🤖 Node '{key}' executed.")
            if "messages" in value:
                # Correct way to access AI Message content
                print(f"   💬 Reply: {value['messages'][-1].content}")

    # Simulation 2: A Corporate Task
    print("\n👤 User: Find me a cheap venue.")
    inputs = {"messages": [HumanMessage(content="Find me a cheap venue.")], "user_role": "CORP"}
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"   🤖 Node '{key}' executed.")
            if "messages" in value:
                # Correct way to access AI Message content
                print(f"   💬 Reply: {value['messages'][-1].content}")

if __name__ == "__main__":
    test_senna_flow()