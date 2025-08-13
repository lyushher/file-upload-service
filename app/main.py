from fastapi import FastAPI
from app.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title="File Upload Service (Core)")
    app.include_router(api_router, prefix="/api")
    return app

app = create_app()
