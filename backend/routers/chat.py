from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from services import answer_question
from dependencies import get_current_user
router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
)

@router.post("/message", response_model=schemas.ChatResponse)
async def handle_chat_message(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db),
    user_metadata: dict = Depends(get_current_user)
):
    reply = await answer_question(
        question=request.message,
        user_metadata=user_metadata,
        db=db,
    )
    return schemas.ChatResponse(reply=reply)
