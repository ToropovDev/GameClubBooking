from fastapi import FastAPI
from backend.src.stations.router import router as station_router
from fastapi_users import FastAPIUsers
from backend.src.auth.models import User
from sqlalchemy.dialects.postgresql import UUID
from backend.src.auth.config import auth_backend, get_user_manager
from backend.src.auth.schemas import UserCreate, UserRead, UserUpdate
from backend.src.reservations.router import router as reservation_router
from backend.src.reviews.router import router as review_router

"""
Main FastAPI app
and included routers
"""
app = FastAPI()
app.include_router(station_router)
app.include_router(reservation_router)
app.include_router(review_router)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)