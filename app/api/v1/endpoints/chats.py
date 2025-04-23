from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.db.crud.chat import get_chat, get_user_chats, create_chat
import logging
router = APIRouter()
logger = logging.getLogger(__name__)
@router.get("/chats/{chat_id}")
async def read_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    chat = await get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    return chat

@router.get("/chats/user/")
async def read_user_chats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user is None:
            logger.warning("No current user found in read_user_chats")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Fetching chats for user_id={current_user.id}")
        chats = await get_user_chats(db, current_user.id)
        logger.debug(f"Chats returned: {chats}")
        return chats

    except HTTPException as he:
        logger.error(f"HTTPException in read_user_chats: {he.detail}")
        raise he

    except Exception as e:
        logger.exception("Unexpected error in read_user_chats")
        raise HTTPException(status_code=422, detail=f"Unexpected error: {str(e)}")

@router.post("/chats/")
async def create_new_chat(user1_id: int, user2_id: int, db: AsyncSession = Depends(get_db)):
    return await create_chat(db, user1_id, user2_id)
