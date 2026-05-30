from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import Config
from src.core.mock_llm import MockLLM

def get_senna_brain():
    """
    Returns the 'Reasoning Engine' (Gemini 3.0 Pro) configured with 
    Senna's parameters.
    """
    if Config.USE_MOCK:
        return MockLLM(agent_type="brain")
        
    llm = ChatGoogleGenerativeAI(
        model=Config.MODEL_REASONING,
        google_api_key=Config.API_KEY,
        temperature=0.3, # Low temp for precision/compliance
        convert_system_message_to_human=True 
    )
    return llm

def get_senna_router():
    """
    Returns the 'Fast Engine' (Gemini 2.5 Flash) for quick routing.
    """
    if Config.USE_MOCK:
        return MockLLM(agent_type="router")
        
    llm = ChatGoogleGenerativeAI(
        model=Config.MODEL_FAST,
        google_api_key=Config.API_KEY,
        temperature=0.0
    )
    return llm