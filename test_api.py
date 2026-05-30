import httpx
import asyncio

URL = "http://127.0.0.1:8000/chat"

async def send_request(role, message):
    print(f"\n📤 Sending {role} Request: '{message}'")
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(URL, json={
            "user_id": "test_user_1",
            "role": role,
            "message": message
        })
        print(f"📥 Senna says:\n{response.json()['response']}")

async def main():
    # 1. Test Corporate Logic
    await send_request("CORP", "Find a venue for 20 pax under 1M UGX next Friday.")
    
    # 2. Test Government Logic
    await send_request("GOV", "I want to buy a laptop for 10,000,000 UGX.")

if __name__ == "__main__":
    asyncio.run(main())