from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey("interviews.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    user_answer = Column(Text, nullable=True)
