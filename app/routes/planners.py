import json

from fastapi import APIRouter, Depends, Form, Request, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import RecommendationHistory
from ..services.gemini_service import generate_recommendations


router = APIRouter()


def user_id(request: Request):
    return request.session.get("user_id")


async def save_history(db, uid, planner, data, result):
    if uid:
        db.add(
            RecommendationHistory(
                user_id=uid,
                planner=planner,
                input_data=json.dumps(data),
                result_data=json.dumps(result),
            )
        )
        db.commit()


@router.post("/generate-home")
async def generate_home(
    request: Request,
    budget: float = Form(...),
    rooms: str = Form(...),
    items: str = Form(...),
    style: str = Form("Modern"),
    db: Session = Depends(get_db),
):
    data = {
        "budget": budget,
        "rooms": rooms,
        "items": items,
        "style": style,
    }

    result = await generate_recommendations("home", data)

    await save_history(
        db,
        user_id(request),
        "home",
        data,
        result,
    )

    return result


@router.post("/generate-party")
async def generate_party(
    request: Request,
    budget: float = Form(...),
    guests: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(""),
    db: Session = Depends(get_db),
):
    data = {
        "budget": budget,
        "guests": guests,
        "event_type": event_type,
        "venue": venue,
    }

    result = await generate_recommendations("party", data)

    await save_history(
        db,
        user_id(request),
        "party",
        data,
        result,
    )

    return result


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_description: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_bytes = None
    image_mime_type = None

    if outfit_image:
        image_bytes = await outfit_image.read()
        image_mime_type = outfit_image.content_type

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_description": outfit_description,
    }

    result = await generate_recommendations(
        "jewelry",
        data,
        image_bytes,
        image_mime_type,
    )

    await save_history(
        db,
        user_id(request),
        "jewelry",
        data,
        result,
    )

    return result