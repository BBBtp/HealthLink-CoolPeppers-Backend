from sqlalchemy import insert, delete, select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, Doctor, Clinic
from app.db.models.favorites import FavoriteType, user_favorites


async def add_to_favorites(db: AsyncSession, user_id: int, item_id: int, item_type: FavoriteType):
    """
    Добавляет врача или клинику в избранное пользователя
    """
    # Проверяем существование пользователя
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Проверяем существование элемента
    if item_type == FavoriteType.DOCTOR:
        item = await db.get(Doctor, item_id)
    else:
        item = await db.get(Clinic, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_type.value.capitalize()} not found"
        )

    # Проверяем, не добавлен ли уже элемент
    stmt = select(user_favorites).where(
        user_favorites.c.user_id == user_id,
        user_favorites.c.item_id == item_id,
        user_favorites.c.item_type == item_type
    )
    result = await db.execute(stmt)
    if result.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{item_type.value.capitalize()} already in favorites"
        )

    # Добавляем связь
    await db.execute(
        insert(user_favorites).values(
            user_id=user_id,
            item_id=item_id,
            item_type=item_type
        )
    )
    await db.commit()
    return {"message": f"{item_type.value.capitalize()} added to favorites"}


async def remove_from_favorites(db: AsyncSession, user_id: int, item_id: int, item_type: FavoriteType):
    """
    Удаляет врача или клинику из избранного пользователя
    """
    # Проверяем существование пользователя
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Проверяем существование элемента
    if item_type == FavoriteType.DOCTOR:
        item = await db.get(Doctor, item_id)
    else:
        item = await db.get(Clinic, item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item_type.value.capitalize()} not found"
        )

    # Проверяем, есть ли элемент в избранном
    stmt = select(user_favorites).where(
        user_favorites.c.user_id == user_id,
        user_favorites.c.item_id == item_id,
        user_favorites.c.item_type == item_type
    )
    result = await db.execute(stmt)
    if not result.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{item_type.value.capitalize()} not in favorites"
        )

    # Удаляем связь
    await db.execute(
        delete(user_favorites).where(
            user_favorites.c.user_id == user_id,
            user_favorites.c.item_id == item_id,
            user_favorites.c.item_type == item_type
        )
    )
    await db.commit()
    return {"message": f"{item_type.value.capitalize()} removed from favorites"}