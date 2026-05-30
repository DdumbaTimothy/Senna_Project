from langchain_core.messages import AIMessage

class MockLLM:
    def __init__(self, agent_type="general"):
        self.agent_type = agent_type

    def bind_tools(self, tools):
        # Return self, we don't actually bind for the mock unless we want to simulate tool calling
        return self

    def invoke(self, messages):
        last_msg = messages[-1].content.lower() if hasattr(messages[-1], 'content') else str(messages[-1]).lower()
        
        # Extract user input if it's the router prompt
        if "user input:" in last_msg:
            user_input = last_msg.split("user input:")[-1].strip()
        else:
            user_input = last_msg
            
        print(f"[MOCK DEBUG] agent_type={self.agent_type}, user_input='{user_input}'")
        
        # 1. Mock Router
        if self.agent_type == "router":
            if "requisition" in user_input or "ppda" in user_input or "audit" in user_input or "ministry" in user_input:
                return AIMessage(content="GOV_FLOW")
            elif "venue" in user_input or "party" in user_input or "market" in user_input or "sales" in user_input:
                return AIMessage(content="CORP_FLOW")
            else:
                return AIMessage(content="GENERAL_CHAT")
                
        # 2. Mock Brain (Manager/Guardian/General)
        if "requisition" in user_input or "rate" in user_input:
            # Simulate Guardian Compliance
            if "140" in user_input or "100" in user_input:
                return AIMessage(content="✅ **COMPLIANCE CLEARED**. The requested rate matches the approved budget of 140,000 UGX. Proceeding with preparing the transaction details.")
            else:
                return AIMessage(content="🚨 **COMPLIANCE ALERT**. The requested rate exceeds the approved budget ceiling (140,000 UGX). Request REJECTED.")
                
        elif "venue" in user_input or "cheap" in user_input:
            # Simulate Manager tool result
            return AIMessage(content="I have researched the market. Here are 3 options:\n1. Kampala Serena (High-end)\n2. Mestil Hotel (Mid-tier)\n3. Suit Republic Hub (Cost-effective)\n\nWhich one should we book?")
            
        else:
            return AIMessage(content="Hello! I am Senna. How can I help you today?")
