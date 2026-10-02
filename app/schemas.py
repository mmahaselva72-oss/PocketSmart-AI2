from pydantic import BaseModel, EmailStr
from typing import Optional, List

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float
    rooms: str
    items: str
    style: str = "Modern"

class PartyRequest(BaseModel):
    budget: float
    guests: int
    event_type: str
    venue: str = ""

class JewelryRequest(BaseModel):
    budget: float
    occasion: str
    style: str
    outfit_description: str = ""

class RecommendationItem(BaseModel):
    name: str
    category: str
    price: float
    platform: str
    reason: str
