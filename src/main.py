from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import build_graph
from langchain_core.messages import HumanMessage, AIMessage
from src.core.database import log_interaction # <--- NEW IMPORT

app = FastAPI(title="Senna Core API")
graph = build_graph()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    role: str = "CORP"

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"📩 Incoming: {request.message} [{request.role}]")
    
    # 1. LOG INCOMING
    log_interaction(
        user_id=request.user_id,
        role=request.role,
        content=request.message,
        direction="INCOMING",
        intent="PENDING"
    )
    
    # 2. Run Senna
    inputs = {
        "messages": [HumanMessage(content=request.message)],
        "user_role": request.role,
        "user_id": request.user_id
    }
    
    try:
        output = graph.invoke(inputs)
        
        # Extract response securely
        last_msg = output["messages"][-1]
        response_text = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        
        # Determine intent from the final state (if available)
        # Note: LangGraph output usually contains the keys from the state
        final_intent = output.get("current_intent", "GENERAL")

        # 3. LOG OUTGOING
        log_interaction(
            user_id=request.user_id,
            role=request.role,
            content=response_text,
            direction="OUTGOING",
            intent=final_intent
        )
        
        return {"response": response_text}
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))