from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.core.llm import get_senna_brain
from src.core.state import SennaState
from src.core.rag import retrieve_knowledge

GUARDIAN_SYSTEM_PROMPT = """
You are the **Government Compliance Auditor**.
Your job is to compare User Requests against Official Budget Documents.

**CRITICAL RULES FOR COMPARISON:**
1. **Check the Unit:** If the user asks for a price "per night", "per person", or "unit cost", you MUST compare it against the **RATE** or **UNIT COST** column in the evidence.
2. **Do NOT compare a Rate against a Total.** - Example: If Budget Rate is 140,000 and Total is 560,000.
   - User asks for 500,000/night.
   - 500,000 > 140,000 -> **REJECT**. (Do not approve just because 500k < 560k).
3. **Strict Limits:** The Budgeted Rate is the **Maximum Ceiling**.

**Output Format:**
- If Rejected: Start with "🚨 **COMPLIANCE ALERT**". Explain the specific variance (Requested Rate vs Approved Rate).
- If Approved: Start with "✅ **COMPLIANCE CLEARED**".
"""

def guardian_node(state: SennaState) -> dict:
    """
    The RAG-Enabled Compliance Auditor.
    """
    print("🔒 Guardian is auditing (Checking Knowledge Base)...")
    
    if not state["messages"]:
        return {"messages": [AIMessage(content="Error: No message to audit.")]}

    last_msg = state["messages"][-1].content
    llm = get_senna_brain()

    # 1. RETRIEVAL
    print(f"   🔎 Searching docs for context on: '{last_msg}'")
    docs = retrieve_knowledge(last_msg)
    
    context_text = "\n\n".join([f"--- EVIDENCE (Source: {d.metadata.get('source', 'Unknown')} | Sheet: {d.metadata.get('sheet', 'Unknown')}) ---\n{d.page_content}" for d in docs])

    if not context_text:
        context_text = "No specific budget records found for this item."

    # 2. AUDIT PROMPT
    audit_prompt = f"""
    **USER REQUEST:** "{last_msg}"

    **EVIDENCE FROM BUDGET FILES:**
    {context_text}

    **TASK:** Audit the request. Pay close attention to **RATE** vs **TOTAL**. 
    If the user request exceeds the specific **RATE** in the budget, REJECT IT.
    """

    # 3. VERDICT
    response = llm.invoke([
        SystemMessage(content=GUARDIAN_SYSTEM_PROMPT), 
        HumanMessage(content=audit_prompt)
    ])
    
    print("   ⚖️ Verdict Reached.")
    return {"messages": [response]}