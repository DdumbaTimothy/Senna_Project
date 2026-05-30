from src.graph import build_graph
from langchain_core.messages import HumanMessage

def test_tool_usage():
    app = build_graph()
    
    # 1. We provide the FULL TRINITY: Budget, Pax, AND Date.
    prompt = "Find venues in Kampala under 2M UGX for 50 pax for next Friday."
    print(f"\n👤 User: {prompt}")
    
    inputs = {"messages": [HumanMessage(content=prompt)]}

    print("🚀 Starting Stream...")
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"👉 Node Reached: {key}")
            
            if "messages" in value:
                last_msg = value["messages"][-1]
                
                # Case A: Tool Call (The AI wants to search)
                if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                    tool_name = last_msg.tool_calls[0]['name']
                    tool_args = last_msg.tool_calls[0]['args']
                    print(f"   🛠️  TOOL CALLED: {tool_name}")
                    print(f"       Query: {tool_args}")
                
                # Case B: Final Text (The AI summarizes results)
                elif last_msg.content:
                    print(f"   💬 Reply: {last_msg.content[:300]}...") 

if __name__ == "__main__":
    test_tool_usage()