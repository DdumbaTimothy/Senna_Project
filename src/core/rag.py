import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from supabase import create_client, ClientOptions
from src.config import Config

# 1. Initialize Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=Config.API_KEY
)

# 2. Initialize Supabase Client with explicit timeout settings
# We increase the fetch timeout to 60 seconds to handle slow networks
supabase_client = create_client(
    Config.SUPABASE_URL, 
    Config.SUPABASE_KEY,
    options=ClientOptions(postgrest_client_timeout=60)
)

def retrieve_knowledge(query: str):
    """
    Directly calls Supabase RPC with RETRY LOGIC for unstable networks.
    """
    print(f"📚 Searching Knowledge Base for: '{query}'")
    
    if Config.USE_MOCK:
        print("   -> Returning MOCK records.")
        return [
            Document(page_content="Ministry of Finance Approved Rates:\nVenue per day: 1,500,000 UGX\nPer Diem (Night): 140,000 UGX", metadata={"source": "Budget_2025.pdf", "sheet": "Rates"})
        ]

    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # A. Convert Query to Vector
            query_vector = embeddings.embed_query(query)
            
            # B. Call Database (RPC)
            response = supabase_client.rpc(
                "match_documents",
                {
                    "query_embedding": query_vector,
                    "match_threshold": 0.5, 
                    "match_count": 4
                }
            ).execute()
            
            # C. Process Results
            results = []
            data = response.data 
            
            if data:
                for record in data:
                    doc = Document(
                        page_content=record.get("content", ""),
                        metadata=record.get("metadata", {})
                    )
                    results.append(doc)
                    
            print(f"   -> Found {len(results)} relevant records.")
            return results

        except Exception as e:
            print(f"⚠️ RAG Attempt {attempt+1}/{max_retries} Failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2) # Wait 2 seconds before retrying
            else:
                print("❌ RAG Failed after retries. Returning empty context.")
                return []