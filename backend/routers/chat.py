from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from services import answer_question

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
)

@router.post("/message", response_model=schemas.ChatResponse)
async def handle_chat_message(
    request: schemas.ChatRequest,
    db: Session = Depends(get_db),
    # TODO: replace None with actual JWT-decoded user_metadata once auth is implemented
    # user_metadata: dict = Depends(get_current_user)
):
    reply = await answer_question(
        question=request.message,
        user_metadata=None,  # Swap for real user once JWT is ready
        db=db,
    )
    return schemas.ChatResponse(reply=reply)
