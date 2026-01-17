from fastapi import FastAPI

app = FastAPI(
    title="AI Interview Coach API",
    description="Backend API for AI-powered interview coaching system",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "API is running"}

from app.core.database import engine

@app.get("/db-check")
def db_check():
    try:
        engine.connect()
        return {"db": "connected"}
    except Exception as e:
        return {"error": str(e)}

