"""There are the utils for authentication system"""

from datetime import timedelta, datetime
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from routers.auth.hashing import verify_password
from db.models.user import User
from exceptions import LoginException
from routers.settings import main as settings


async def get_user_if_exists(session, name: str):
    """
    :param session: AsyncSession for DB
    :param name: username from request data
    :return: User instance if user exists else None
    """
    return await User.get_by_name(session, name)


async def authenticate_user(session: AsyncSession, username: str, password: str):
    """
    Check user's credentials
    :param session: AsyncSession for DB
    :param username: username from login form
    :param password: raw password from login form
    :return: User instance if data is correct
    :raise LoginException if data is incorrect
    """
    user = await get_user_if_exists(session, username)
    if not user:
        raise LoginException
    if not verify_password(password, user.hashed_password):
        raise LoginException
    return user


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
