from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.payment import Payment
from app.shemas.payment import PaymentCreate, PaymentConfirm

async def create_payment(db: AsyncSession, payment: PaymentCreate, user_id: int):
    """
    Создание платежа для пользователя.

    Эта функция создаёт новый платеж и привязывает его к пользователю, используя уникальный идентификатор пользователя и данные о платеже.
    Авторизация пользователя осуществляется с помощью токена в заголовке.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - payment: PaymentCreate — данные для создания платежа (модель данных).
    - user_id: int — уникальный идентификатор пользователя, для которого создается платеж.

    Возвращает:
    - Объект Payment — созданный платеж.

    Исключения:
    - HTTPException: 401 — если пользователь не авторизован или не совпадает с user_id.
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не можете создать платеж для другого пользователя")

    payment_url = f"https://sberbank.ru/pay?appointment_id={payment.appointment_id}"  # Заглушка
    db_payment = Payment(**payment.dict(), payment_url=payment_url)

    db.add(db_payment)
    await db.commit()  # Асинхронная операция commit
    await db.refresh(db_payment)  # Асинхронная операция refresh

    return db_payment

async def confirm_payment(db: AsyncSession, payment_data: PaymentConfirm, user_id: int):
    """
    Подтверждение платежа для пользователя.

    Эта функция обновляет статус платежа после его подтверждения.
    Авторизация пользователя осуществляется с помощью токена в заголовке.

    Аргументы:
    - db: AsyncSession — объект асинхронной сессии базы данных.
    - payment_data: PaymentConfirm — данные для подтверждения платежа.
    - user_id: int — уникальный идентификатор пользователя, которому принадлежит платеж.

    Возвращает:
    - Объект Payment — обновленный платеж.

    Исключения:
    - HTTPException: 401 — если пользователь не авторизован или не совпадает с user_id.
    - HTTPException: 404 — если платеж не найден.
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не можете подтверждать платежи для другого пользователя")

    # Асинхронный запрос для получения платежа по ID
    query = select(Payment).filter(Payment.id == payment_data.payment_id)
    result = await db.execute(query)
    db_payment = result.scalars().first()

    if not db_payment:
        raise HTTPException(status_code=404, detail="Платеж не найден")

    db_payment.status = payment_data.status.value
    await db.commit()  # Асинхронная операция commit
    await db.refresh(db_payment)  # Асинхронная операция refresh

    return db_payment
