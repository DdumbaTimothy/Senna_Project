"""
The 'Truth Database' for Government Compliance.
In production, this queries Supabase/Postgres.
"""

# Simulated "Guideline Market Prices" (GMP) issued by PPDA
MARKET_PRICES = {
    "HP_LAPTOP": 3500000,    # 3.5M UGX
    "FUEL_LITER": 5600,      # 5600 UGX
    "REAM_OF_PAPER": 25000,  # 25k UGX
    "WORKSHOP_PER_PAX": 75000 # 75k per person (Lunch + Venue)
}

def check_compliance(item: str, proposed_price: float) -> dict:
    """
    Evaluates if a purchase is within the allowable range.
    """
    # Normalize string (simple fuzzy match logic for MVP)
    item_key = None
    if "laptop" in item.lower(): item_key = "HP_LAPTOP"
    elif "fuel" in item.lower(): item_key = "FUEL_LITER"
    elif "paper" in item.lower(): item_key = "REAM_OF_PAPER"
    elif "workshop" in item.lower() or "training" in item.lower(): item_key = "WORKSHOP_PER_PAX"
    
    if not item_key:
        return {"status": "UNKNOWN", "message": "Item not found in Market Price List. Manual approval required."}
    
    market_price = MARKET_PRICES[item_key]
    variance = ((proposed_price - market_price) / market_price) * 100
    
    if proposed_price <= market_price:
        return {"status": "APPROVED", "variance": variance, "limit": market_price}
    else:
        # PPDA often allows small variance, but let's be strict for Senna
        return {
            "status": "FLAGGED", 
            "message": f"Price fits corruption risk profile. Exceeds Market Price by {variance:.1f}%.",
            "limit": market_price
        }