from src.core.llm import get_senna_brain
from src.prompts import SENNA_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage

def test_senna_awakening():
    print(f"🧠 Waking up Senna...")
    
    # 1. Initialize the Brain
    brain = get_senna_brain()
    
    # 2. Inject the Soul (System Prompt)
    messages = [
        SystemMessage(content=SENNA_SYSTEM_PROMPT),
        HumanMessage(content="Who are you and what are your core values?")
    ]
    
    # 3. Generate
    try:
        response = brain.invoke(messages)
        print("\n--- SENNA RESPONSE ---")
        print(response.content)
        print("----------------------\n")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_senna_awakening()