from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.shemas.payment import Payment, PaymentCreate, PaymentConfirm
from app.db.crud import payment as crud

router = APIRouter()

@router.post("/create", response_model=Payment)
async def create_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_payment = await crud.create_payment(db=db, payment=payment_data, user_id=current_user.id)
    return new_payment

@router.post("/confirm")
async def confirm_payment(
    payment_data: PaymentConfirm,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_payment = await crud.confirm_payment(db=db, payment_data=payment_data, user_id=current_user.id)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment status updated"}
