from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from auth.database import User
from auth.shemas import UserRead, UserCreate

from operations.router import router as operations_router
from tasks.router import router as tasks_router
from base_config import fastapi_users, auth_backend, current_user


app = FastAPI(title='Chat')

@app.get('/')
async def root():
    return 'There would be a chat'

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    operations_router
)

app.include_router(
    tasks_router
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, unregistered user"
