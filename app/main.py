from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .database import Base, engine
from .config import SECRET_KEY
from .routes import pages, auth, planners

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PocketSmart AI")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router, prefix="/api")
app.include_router(planners.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "service": "PocketSmart AI"}
