from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.payment import Payment
from app.shemas.payment import PaymentCreate, PaymentConfirm


def create_payment(db: Session, payment: PaymentCreate, user_id: int):
    """
    Создание платежа для пользователя.

    Эта функция создаёт новый платеж и привязывает его к пользователю, используя уникальный идентификатор пользователя и данные о платеже.
    Авторизация пользователя осуществляется с помощью токена в заголовке.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - payment: PaymentCreate — данные для создания платежа (модель данных).
    - user_id: int — уникальный идентификатор пользователя, для которого создается платеж.
    - current_user: User — текущий авторизованный пользователь, получаемый через зависимость.

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
    db.commit()
    db.refresh(db_payment)
    return db_payment


def confirm_payment(db: Session, payment_data: PaymentConfirm, user_id: int,
                    ):
    """
    Подтверждение платежа для пользователя.

    Эта функция обновляет статус платежа после его подтверждения.
    Авторизация пользователя осуществляется с помощью токена в заголовке.

    Аргументы:
    - db: Session — объект базы данных для выполнения запроса.
    - payment_data: PaymentConfirm — данные для подтверждения платежа.
    - user_id: int — уникальный идентификатор пользователя, которому принадлежит платеж.
    - current_user: User — текущий авторизованный пользователь, получаемый через зависимость.

    Возвращает:
    - Объект Payment — обновленный платеж.

    Исключения:
    - HTTPException: 401 — если пользователь не авторизован или не совпадает с user_id.
    - HTTPException: 404 — если платеж не найден.
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="Вы не можете подтверждать платежи для другого пользователя")

    db_payment = db.query(Payment).filter(Payment.id == payment_data.payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Платеж не найден")

    db_payment.status = payment_data.status.value
    db.commit()
    db.refresh(db_payment)
    return db_payment
