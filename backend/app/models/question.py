from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
