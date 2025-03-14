import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDNAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)

def upload_image(file):
    """
    Загружает изображение в Cloudinary и возвращает URL.
    """
    result = cloudinary.uploader.upload(file)
    return result.get("secure_url")  # Берем URL загруженного фото
