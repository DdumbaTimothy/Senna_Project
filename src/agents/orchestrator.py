from langchain_core.messages import SystemMessage, HumanMessage
from src.core.llm import get_senna_router
from src.core.state import SennaState
from src.config import Config

# The Router's specific instruction guide
ROUTER_PROMPT = """
You are the **Senna Router**. Your ONLY job is to classify the user's intent into one of these categories.
Output ONLY the category name. Do not add punctuation or explanation.

CATEGORIES:
1. **GOV_FLOW**: User mentions Ministries, SOPs, PPDA, Compliance, or Audit.
2. **CORP_FLOW**: User mentions Marketing, Booking Venues, Trends, or Sales.
3. **GENERAL_CHAT**: Greetings, small talk, or vague questions.

User Input: {user_input}
Category:
"""

def router_node(state: SennaState) -> dict:
    """
    Analyzes the last message and decides which path to take.
    PRIORITIZES USER ROLE (Identity) over Text.
    """
    print("🚦 Senna is routing...")
    
    last_message = state["messages"][-1].content
    user_role = state.get("user_role", "CORP") # Default to CORP if undefined

    # --- HARD LOGIC OVERRIDES (The Guardrails) ---
    
    # 1. If User is GOV, almost everything operational goes to Guardian
    # We only allow "General Chat" (Greetings) to bypass Guardian.
    if user_role == "GOV":
        # We use a quick check: Is this a "Task" or a "Greeting"?
        # For safety, we route ANY request with numbers/money/items to GOV_FLOW
        keywords = ["buy", "purchase", "ugx", "million", "laptop", "requisition", "allowance"]
        if any(w in last_message.lower() for w in keywords):
            print("👉 Route Selected: GOV_FLOW (Identity Override)")
            return {"current_intent": "GOV_FLOW"}

    # --- AI ROUTING (For ambiguous cases) ---
    
    # Call the Fast Brain
    llm = get_senna_router()
    prompt = ROUTER_PROMPT.format(user_input=last_message)
    response = llm.invoke([HumanMessage(content=prompt)])
    decision = response.content.strip().upper()
    
    # Fallback cleanup
    if "GOV" in decision: clean_decision = "GOV_FLOW"
    elif "CORP" in decision: clean_decision = "CORP_FLOW"
    else: clean_decision = "GENERAL_CHAT"
        
    print(f"👉 Route Selected: {clean_decision}")
    return {"current_intent": clean_decision}