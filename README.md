# PocketSmart AI

A TN Skills project: an AI-powered budget and recommendation assistant for Home Interior, Party Planning, and Jewelry.

## Stack
- FastAPI
- Jinja2
- HTML/CSS/JavaScript
- SQLite
- Gemini API
- JWT authentication

## Local setup

1. Create a virtual environment:
   Windows:
   `python -m venv .venv`
   `.venv\Scripts\activate`

2. Install:
   `pip install -r requirements.txt`

3. Copy `.env.example` to `.env` and add your Gemini API key.

4. Run:
   `uvicorn app.main:app --reload`

5. Open:
   `http://127.0.0.1:8000`

## GitHub / deployment

Do not commit `.env`. Commit `.env.example` only.

The included `render.yaml` provides a starting point for deployment on Render. Add `GEMINI_API_KEY` as a secret environment variable in the deployment dashboard.

## Project structure

- `app/main.py` - FastAPI application
- `app/database.py` - SQLite setup
- `app/models.py` - database models
- `app/routes/` - application routes
- `app/services/` - AI and recommendation logic
- `app/templates/` - Jinja2 pages
- `app/static/` - CSS and JavaScript
- `tests/` - basic API tests
