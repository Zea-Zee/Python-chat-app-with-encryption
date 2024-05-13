import fastapi_users
from fastapi_users import FastAPIUsers

from auth.database import User
from auth.manager import get_user_manager
from auth.auth import auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
