# test_setup.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env")
else:
    genai.configure(api_key=api_key)
    try:
        # Simple handshake with Gemini
        model = genai.GenerativeModel('gemini-2.5-flash') # Using 2.5 flash as proxy for availability
        response = model.generate_content("Hello Senna, are you online?")
        print(f"✅ Success! Brain is active: {response.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")