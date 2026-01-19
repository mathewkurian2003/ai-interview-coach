from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class InterviewCreate(BaseModel):
    role: str
    level: str


class InterviewResponse(BaseModel):
    id: UUID
    role: str
    level: str
    status: str
    started_at: datetime

    class Config:
        from_attributes = True
