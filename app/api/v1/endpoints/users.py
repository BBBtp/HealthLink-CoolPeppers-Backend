from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cloudinary import upload_image
from app.core.security import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.shemas.user import UserProfile

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserProfile)
async def update_profile(
        first_name: str = Form(None),
        last_name: str = Form(None),
        age: int = Form(None),
        blood_type: str = Form(None),
        photo: UploadFile = File(None),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Обновляет данные профиля пользователя (без изменения email и пароля).
    Позволяет загрузить фотографию.
    """

    if first_name:
        current_user.first_name = first_name
    if last_name:
        current_user.last_name = last_name
    if age:
        current_user.age = age
    if blood_type:
        current_user.blood_type = blood_type
    if photo:
        photo_url = upload_image(photo.file)
        current_user.photo_url = photo_url

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user
