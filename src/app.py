import sys
import os

# --- PATH FIX ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ----------------

import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage
from src.graph import build_graph

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Senna | Universal Coordination Engine",
    page_icon="🧬",
    layout="wide"
)

# Initialize Brain
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CSS FOR SPEED ---
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 5px; }
    .reportview-container { background: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=60)
    st.title("Senna Core")
    
    role = st.selectbox(
        "Operating Mode",
        ("Government (Automation)", "Corporate (Operations)")
    )
    
    st.divider()
    
    if role == "Government (Automation)":
        user_role = "GOV"
        st.info("**⚡ MINISTRY AUTOPILOT**")
        st.markdown("**Focus:** Speed & Auto-Correction.")
    else:
        user_role = "CORP"
        st.success("**🚀 HUSTLER MODE**")
        st.markdown("**Focus:** Market Intelligence.")

    st.divider()
    # --- MEMORY INSPECTOR (NEW) ---
    with st.expander("🧠 Debug: Brain Memory"):
        if "messages" in st.session_state:
            st.caption(f"Holding {len(st.session_state.messages)} messages in Short-Term Memory.")
            for i, msg in enumerate(st.session_state.messages):
                st.text(f"[{i}] {msg['role'].upper()}: {msg['content'][:50]}...")
    # -----------------------------
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()

# --- HELPER: CONSTRUCT HISTORY ---
def get_conversation_history():
    """
    Converts Streamlit history into LangChain Message Objects.
    This ensures Senna remembers previous context (like Rejections).
    """
    history_objects = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            history_objects.append(HumanMessage(content=msg["content"]))
        else:
            history_objects.append(AIMessage(content=msg["content"]))
    return history_objects

# --- MAIN CHAT ---
st.title(f"Senna: {role.split(' ')[0]} Mode")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Type your request..."):
    
    # 1. Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Run Senna
    with st.chat_message("assistant"):
        status_box = st.empty()
        
        # UX: Fake Processing Steps
        with status_box.status("⚙️ Processing Context...", expanded=True) as status:
            if user_role == "GOV":
                st.write("🛡️ Analyzing Conversation History...")
                time.sleep(0.5)
                st.write("🔍 Consulting Budgets & Workplans...")
            else:
                st.write("🌍 Checking Market Rates...")
            status.update(label="✅ Ready", state="complete", expanded=False)
        
        # 3. PREPARE INPUTS WITH FULL HISTORY (The Fix)
        # We grab the full history + the new prompt is already in it
        full_history = get_conversation_history()
        
        inputs = {
            "messages": full_history, # <--- SENDING MEMORY HERE
            "user_role": user_role,
            "current_intent": "GOV_FLOW" if user_role == "GOV" else "CORP_FLOW"
        }
        
        try:
            full_response = st.session_state.graph.invoke(inputs)
            
            # Extract the LATEST response
            last_msg = full_response["messages"][-1]
            response_text = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)

            # 4. RENDER OUTPUT
            if user_role == "GOV":
                # 1. REJECTION LOGIC
                if "REJECTED" in response_text or "COMPLIANCE ALERT" in response_text:
                    st.warning("⚠️ **Wait - Budget Mismatch Detected**")
                    st.markdown(response_text)
                    st.info("💡 **Required Action:** Please explicitly authorize the approved rate (140k) or provide a waiver.")
                
                # 2. APPROVAL / GENERATION LOGIC
                # We check for keywords indicating the user accepted the 140k
                elif "proceed with preparing" in response_text.lower() or "finalized" in response_text.lower() or "transaction details" in response_text.lower():
                    st.success("✅ **Compliance Cleared. Document Generated.**")
                    st.markdown(response_text)
                    
                    # --- NEW: GENERATE DOCX ---
                    from src.core.docs import generate_requisition_doc
                    
                    # We pass the AI's text to the document generator
                    doc_file = generate_requisition_doc(response_text)
                    
                    st.download_button(
                        label="📥 Download Official Memo (.docx)",
                        data=doc_file,
                        file_name="Requisition_Namayingo.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    # --------------------------
                
                else:
                    st.markdown(response_text)
            else:
                st.markdown(response_text)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"Error: {e}")