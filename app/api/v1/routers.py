from fastapi import APIRouter
from app.websockets import chat
from app.api.v1.endpoints import clinics, doctors, services, appointments, payment, auth, users, appointment_slots, \
    chats

router = APIRouter()

router.include_router(clinics.router, prefix="/clinics", tags=["clinics"])
router.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
router.include_router(services.router, prefix="/services", tags=["services"])
router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
router.include_router(payment.router, prefix="/payment", tags=["payment"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(appointment_slots.router, prefix="/appointment_slots", tags=["appointment_slots"])
router.include_router(chats.router, prefix="/chat", tags=["chat"])

router.include_router(chat.router, prefix="/ws", tags=["websocket"])