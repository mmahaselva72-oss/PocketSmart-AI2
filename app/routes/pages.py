from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, RecommendationHistory

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
       return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
        return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    uid = request.session.get("user_id")
    history = db.query(RecommendationHistory).filter_by(user_id=uid).order_by(
        RecommendationHistory.created_at.desc()).limit(10).all() if uid else []
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"history": history}
    )
@router.get("/home-planner", response_class=HTMLResponse)
def home_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={}
    )
@router.get("/party-planner", response_class=HTMLResponse)
def party_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={}
    )

@router.get("/jewelry-planner", response_class=HTMLResponse)
def jewelry_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={}
    )

@router.get("/history", response_class=HTMLResponse)
def history(request: Request, db: Session = Depends(get_db)):
    uid = request.session.get("user_id")
    records = db.query(RecommendationHistory).filter_by(user_id=uid).order_by(
        RecommendationHistory.created_at.desc()).all() if uid else []
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"history": records}
    )
