from supabase import create_client, Client
from src.config import Config
import datetime

# Singleton connection
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def log_interaction(user_id: str, role: str, content: str, direction: str, intent: str = "GENERAL"):
    """
    Saves a message to the Cloud Database.
    direction: 'INCOMING' (User) or 'OUTGOING' (Senna)
    """
    try:
        # Check if this message contains a Compliance Alert
        is_flagged = "COMPLIANCE ALERT" in content

        data = {
            "user_id": user_id,
            "user_role": role,
            "message_content": content,
            "direction": direction,
            "intent": intent,
            "compliance_flag": is_flagged,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        
        # Insert into Supabase
        response = supabase.table("senna_logs").insert(data).execute()
        print(f"💾 Logged to DB: {direction} (Flagged: {is_flagged})")
        return response
        
    except Exception as e:
        print(f"⚠️ Database Error: {e}")
        # We don't crash the app if logging fails, just warn
        return None