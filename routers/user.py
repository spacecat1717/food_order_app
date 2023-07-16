from typing import Annotated
from datetime import timedelta
from jose import JWTError, jwt

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from routers.auth import utils, hashing
from db.models.user import User
from db.utils.utils import get_async_session
from exceptions import CredentialsException
from schemas import user as schema
from routers.settings import main as settings

user_router = APIRouter(prefix='/users')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@user_router.post('/create', status_code=201, tags=['signup'])
async def create_user(username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[str, Form()],
                      full_name: Annotated[str, Form()], session: AsyncSession = Depends(get_async_session)):
    """
    Create new user in DB if it doesn't exist yet
    :param username: username from form (as form-data)
    :param password: password from form
    :param email: email from form(not required)
    :param full_name: full name from form
    :param session: AsyncSession for DB
    :return: simple json with info
    """
    if await utils.get_user_if_exists(session, username):
        return HTTPException(status_code=409, detail=f'User {username} already exists!')
    await User.create(session=session, username=username, full_name=full_name, email=email,
                                 hashed_password=hashing.hash_password(password))
    return {'status': 'ok', 'message': f'user {username} was successfully created'}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(get_async_session)):
    """
    Dependency func. Gets current user by token
    :param token: token from request (sended as authorization/bearer token)
    :param session: AsyncSession for DB
    :return: user instance if user exists
    :raises CredentialsException if token isn't available
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise CredentialsException
    username = payload.get('sub')
    user = await utils.get_user_if_exists(session, username)
    if not user:
        raise CredentialsException
    return user


@user_router.post('/token', tags=['signin'])
async def get_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                           session: AsyncSession = Depends(get_async_session)):
    """
    Create new token
    :param form: users credentials from login form
    :param session: AsyncSession for DB
    :return: token and its type
    """
    user = await utils.authenticate_user(session, form.username, form.password)
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_token(
        data={'sub': user.username},
        expires_delta=expires
    )
    return {'token': access_token, "token_type": "bearer"}


@user_router.get('/current', response_model=schema.User)
async def current_user(user: Annotated[schema.User, Depends(get_current_user)]):
    """Tmp test func"""
    return user