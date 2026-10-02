import json
from .mock_products import HOME_PRODUCTS, PARTY_PRODUCTS, JEWELRY_PRODUCTS

def _fallback(planner, data):
    budget = float(data.get("budget", 0))
    if planner == "home":
        products = HOME_PRODUCTS
    elif planner == "party":
        products = PARTY_PRODUCTS
    else:
        products = JEWELRY_PRODUCTS

    # Keep only items that can reasonably fit the supplied budget.
    affordable = [p for p in products if p["price"] <= budget]
    if not affordable:
        affordable = products[:2]

    return {
        "planner": planner,
        "budget": budget,
        "summary": f"Recommendations prepared for a budget of ₹{budget:,.0f}.",
        "items": [
            {**p, "reason": "Selected as a budget-friendly option for your preferences."}
            for p in affordable[:5]
        ]
    }

async def generate_recommendations(planner, data, image_bytes=None):
    # This starter uses deterministic fallback data so the project works
    # even before a Gemini API key is configured.
    #
    # Gemini integration can be enabled in this service without changing
    # the planner routes or frontend contract.
    return _fallback(planner, data)
