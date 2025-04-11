from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models.message import Message
from app.db.models.chat import Chat
import json

router = APIRouter()

active_connections = {}  # {user_id: [WebSocket, WebSocket]}


async def save_message(db: AsyncSession, chat_id: int, sender_id: int, text: str):
    message = Message(chat_id=chat_id, sender_id=sender_id, text=text, status="sent")
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: AsyncSession = Depends(get_db)):
    await websocket.accept()

    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "send_message":
                chat_id = data.get("chat_id")
                sender_id = data.get("sender_id")
                text = data.get("text")

                result = await db.execute(select(Chat).filter_by(id=chat_id))
                chat = result.scalars().first()

                if not chat:
                    await websocket.send_json({"error": "Chat not found"})
                    continue

                recipient_id = chat.user1_id if chat.user2_id == sender_id else chat.user2_id

                message = await save_message(db, chat_id, sender_id, text)

                for conn in active_connections.get(recipient_id, []):
                    await conn.send_json({
                        "action": "new_message",
                        "message_id": message.id,
                        "chat_id": chat_id,
                        "sender_id": sender_id,
                        "text": text,
                        "status": "delivered"
                    })

                message.status = "delivered"
                await db.commit()

            elif action == "update_status":
                message_id = data.get("message_id")
                status = data.get("status")

                result = await db.execute(select(Message).filter_by(id=message_id))
                msg = result.scalars().first()

                if msg:
                    msg.status = status
                    await db.commit()

                    for conn in active_connections.get(msg.sender_id, []):
                        await conn.send_json({
                            "action": "update_status",
                            "message_id": message_id,
                            "status": status
                        })

    except WebSocketDisconnect:
        active_connections[user_id].remove(websocket)
        if not active_connections[user_id]:
            del active_connections[user_id]
