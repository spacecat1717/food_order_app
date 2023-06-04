import asyncio

from datetime import timedelta, datetime
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from routers.auth.hashing import verify_password
from db.models.user import User
from exceptions import LoginException
from routers.settings import main as settings


async def check_user_exists(session, name: str) -> bool:
    return bool(await User.get_by_name(session, name))


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await User.get_by_name(session, username)
    if not user:
        raise LoginException
    if not verify_password(password, user.hashed_password):
        raise LoginException
    return user


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# if __name__ == '__main__':
#     asyncio.run(check_user_exists('pidor'))