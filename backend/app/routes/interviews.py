from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from uuid import uuid4

from app.core.database import get_db
from app.models.interview import Interview
from app.models.user import User
from app.models.question import Question
from app.models.interview_question import InterviewQuestion
from app.schemas.interview import InterviewCreate, InterviewResponse
from app.routes.dependencies import get_current_user

router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post("/start", response_model=InterviewResponse)
def start_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_interview = Interview(
        user_id=current_user.id,
        role=interview.role,
        level=interview.level,
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    questions = db.query(Question).limit(3).all()

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No questions available"
        )

    for q in questions:
        iq = InterviewQuestion(
            id=uuid4(),
            interview_id=new_interview.id,
            question_id=q.id
        )
        db.add(iq)

    db.commit()

    return new_interview


@router.get("/", response_model=List[InterviewResponse])
def list_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    interviews = (
        db.query(Interview)
        .filter(Interview.user_id == current_user.id)
        .order_by(desc(Interview.started_at))
        .all()
    )

    return interviews


@router.get("/{interview_id}/question")
def get_next_question(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    iq = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.interview_id == interview_id,
            InterviewQuestion.user_answer.is_(None),
        )
        .first()
    )

    if not iq:
        return {"message": "Interview completed"}

    question = db.query(Question).filter(
        Question.id == iq.question_id
    ).first()

    return {
        "question_id": iq.question_id,
        "question": question.question,
    }


@router.post("/{interview_id}/answer")
def submit_answer(
    interview_id: str,
    question_id: str,
    answer: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    iq = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.interview_id == interview_id,
            InterviewQuestion.question_id == question_id,
        )
        .first()
    )

    if not iq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found for this interview",
        )

    iq.user_answer = answer
    db.commit()

    return {"message": "Answer saved successfully"}
