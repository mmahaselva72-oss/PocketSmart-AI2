import json
import re

from google import genai
from google.genai import types

from ..config import settings
from .mock_products import HOME_PRODUCTS, PARTY_PRODUCTS, JEWELRY_PRODUCTS

MODEL_NAME = "gemini-3.5-flash-lite"


def _fallback(planner, data):
    budget = float(data.get("budget", 0))

    if planner == "home":
        products = HOME_PRODUCTS
    elif planner == "party":
        products = PARTY_PRODUCTS
    else:
        products = JEWELRY_PRODUCTS

    affordable = [p for p in products if p["price"] <= budget]

    if not affordable:
        affordable = products[:2]

    return {
        "planner": planner,
        "budget": budget,
        "summary": (
            f"Recommendations prepared for a budget of "
            f"₹{budget:,.0f}."
        ),
        "items": [
            {
                **p,
                "reason": (
                    "Selected as a budget-friendly option "
                    "for your preferences."
                ),
            }
            for p in affordable[:5]
        ],
    }


def _extract_json(text):
    if not text:
        return None

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _build_prompt(planner, data):
    budget = float(data.get("budget", 0))

    if planner == "home":
        return f"""
You are PocketSmart AI, a smart budget and home-interior
recommendation assistant.

Create personalized home interior recommendations.

User requirements:
- Budget: ₹{budget:,.0f}
- Rooms: {data.get("rooms", "")}
- Required items: {data.get("items", "")}
- Style: {data.get("style", "Modern")}

Important:
1. Stay within the user's total budget.
2. Consider the requested room, items and style.
3. Recommend practical products.
4. Use realistic Indian prices in INR.
5. Prefer well-known platforms such as Amazon, IKEA and Flipkart.
6. Return exactly 5 recommendations when possible.
7. Do not invent product URLs.
8. The response MUST be valid JSON only.

Return this structure:

{{
  "planner": "home",
  "budget": {budget},
  "summary": "short personalized summary",
  "items": [
    {{
      "name": "product name",
      "category": "category",
      "price": 1499,
      "platform": "Amazon",
      "reason": "why this suits the user"
    }}
  ]
}}
"""

    if planner == "party":
        return f"""
You are PocketSmart AI, a smart event and party budget
recommendation assistant.

Create a practical party/event plan.

User requirements:
- Total budget: ₹{budget:,.0f}
- Guests: {data.get("guests", "")}
- Event type: {data.get("event_type", "")}
- Venue: {data.get("venue", "")}

Important:
1. Stay within the total budget.
2. Consider the number of guests.
3. Consider the event type and venue.
4. Include useful categories such as food, decoration,
   entertainment and accommodation when appropriate.
5. Prefer platforms such as Swiggy, Zomato, OYO and Amazon.
6. Use realistic Indian prices in INR.
7. Return exactly 5 recommendations when possible.
8. Do not invent product URLs.
9. The response MUST be valid JSON only.

Return this structure:

{{
  "planner": "party",
  "budget": {budget},
  "summary": "short personalized summary",
  "items": [
    {{
      "name": "recommendation name",
      "category": "category",
      "price": 4500,
      "platform": "Swiggy",
      "reason": "why this suits the event"
    }}
  ]
}}
"""

    return f"""
You are PocketSmart AI, a personalized jewelry recommendation assistant.

Create jewelry recommendations based on the user's requirements.

User requirements:
- Budget: ₹{budget:,.0f}
- Occasion: {data.get("occasion", "")}
- Style: {data.get("style", "")}
- Outfit description: {data.get("outfit_description", "")}

Important:
1. Stay within the user's budget.
2. Consider the occasion and preferred style.
3. If an outfit image is supplied, analyze its visible colors,
   style and overall aesthetic.
4. Recommend jewelry that coordinates with the outfit.
5. Prefer platforms such as Amazon and Flipkart.
6. Use realistic Indian prices in INR.
7. Return exactly 5 recommendations when possible.
8. Do not invent product URLs.
9. The response MUST be valid JSON only.

Return this structure:

{{
  "planner": "jewelry",
  "budget": {budget},
  "summary": "short personalized summary",
  "items": [
    {{
      "name": "jewelry name",
      "category": "category",
      "price": 2499,
      "platform": "Amazon",
      "reason": "why this jewelry suits the user"
    }}
  ]
}}
"""


async def generate_recommendations(
    planner,
    data,
    image_bytes=None,
    image_mime_type=None,
):
    """
    Generate recommendations using Gemini.

    If GEMINI_API_KEY is not configured or Gemini fails,
    the application automatically uses the fallback data.
    """

    if not settings.GEMINI_API_KEY:
        return _fallback(planner, data)

    try:
        client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        prompt = _build_prompt(planner, data)

        contents = [prompt]

        if image_bytes:
            mime_type = image_mime_type or "image/jpeg"

            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            )

            contents = [
                image_part,
                prompt,
            ]

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=3000,
            ),
        )

        result = _extract_json(response.text)

        if not result or not isinstance(result, dict):
            return _fallback(planner, data)

        result.setdefault("planner", planner)

        result.setdefault(
            "budget",
            float(data.get("budget", 0)),
        )

        result.setdefault(
            "summary",
            (
                "AI recommendations prepared for a budget of "
                f"₹{float(data.get('budget', 0)):,.0f}."
            ),
        )

        result.setdefault("items", [])

        return result

    except Exception as exc:
        print(f"Gemini API error: {exc}")
        return _fallback(planner, data)