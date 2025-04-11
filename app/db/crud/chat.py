from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.db.models.chat import Chat
from fastapi import HTTPException


# Получение чата по ID
async def get_chat(db: AsyncSession, chat_id: int):
    result = await db.execute(select(Chat).filter(Chat.id == chat_id))
    return result.scalars().first()


# Получение всех чатов пользователя
async def get_user_chats(db: AsyncSession, user_id: int):
    result = await db.execute(select(Chat).filter(
        (Chat.user1_id == user_id) | (Chat.user2_id == user_id)
    ))
    return result.scalars().all()


# Создание нового чата
async def create_chat(db: AsyncSession, user1_id: int, user2_id: int):
    # Получаем пользователей
    user1_result = await db.execute(select(User).filter(User.id == user1_id))
    user2_result = await db.execute(select(User).filter(User.id == user2_id))

    user1 = user1_result.scalars().first()
    user2 = user2_result.scalars().first()

    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="Один из пользователей не найден")

    # Проверяем, что хотя бы один из пользователей - доктор
    if user1.role != "doctor" and user2.role != "doctor":
        raise HTTPException(status_code=403, detail="Один из пользователей должен быть доктором")

    # Проверяем, существует ли уже чат
    chat_check_result = await db.execute(select(Chat).filter(
        ((Chat.user1_id == user1_id) & (Chat.user2_id == user2_id)) |
        ((Chat.user1_id == user2_id) & (Chat.user2_id == user1_id))
    ))

    chat = chat_check_result.scalars().first()

    if not chat:
        # Если чат не существует, создаем новый
        chat = Chat(user1_id=user1_id, user2_id=user2_id)
        db.add(chat)
        await db.commit()
        await db.refresh(chat)

    return chat
