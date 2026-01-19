from fastapi import FastAPI
from app.routes.users import router as users_router
from app.routes import auth
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "API is running"}

app.include_router(users_router)

app.include_router(auth.router)
from app.routes import interviews
app.include_router(interviews.router)
from app.core.database import engine
from app.models.interview import Interview

Interview.__table__.create(bind=engine, checkfirst=True)
