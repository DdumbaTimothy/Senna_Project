import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    # --- AI Settings (Bleeding Edge) ---
    # Gemini 2.0 flash: Best for complex reasoning, SOPs, and "Kingdom Values" checks
    MODEL_REASONING = "gemini-2.5-flash" 

    # Gemini 2.0 flash-lite: Best for low-latency routing and simple classification
    MODEL_FAST = "gemini-2.5-flash" 
    
    API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # --- Database ---
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # --- Tools ---
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # --- Mock Mode ---
    USE_MOCK = os.getenv("USE_MOCK", "False").lower() in ["true", "1", "t"]

    @staticmethod
    def validate():
        if not Config.API_KEY:
            raise ValueError("❌ Missing GOOGLE_API_KEY in .env")
        if not Config.SUPABASE_URL:
            raise ValueError("❌ Missing SUPABASE_URL in .env")
        if not Config.SUPABASE_KEY:
            raise ValueError("❌ Missing SUPABASE_KEY in .env")
        if not Config.COMPOSIO_API_KEY:
            raise ValueError("❌ Missing COMPOSIO_API_KEY in .env")
        if not Config.TAVILY_API_KEY:
            raise ValueError("❌ Missing TAVILY_API_KEY in .env")

        # Add other checks as needed