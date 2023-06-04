from typing import Annotated
from datetime import timedelta
from jose import JWTError, jwt

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from routers.auth import utils, hashing
from db.models.user import User
from db.utils.utils import get_async_session
from exceptions import CredentialsException, LoginException
from schemas import user as schema
from routers.settings import main as settings

user_router = APIRouter(prefix='/users')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token4561625')


@user_router.post('/create', response_model=schema.User, status_code=201, tags=['signup'])
async def create_user(username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[str, Form()],
                      full_name: Annotated[str, Form()], session: AsyncSession = Depends(get_async_session)):
    if await utils.check_user_exists(session, username):
        return HTTPException(status_code=409, detail=f'User {username} already exists!')
    new_user = await User.create(session=session, username=username, full_name=full_name, email=email,
                                 hashed_password=hashing.hash_password(password))
    return new_user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise CredentialsException
    except JWTError:
        raise CredentialsException
    user = await User.get_by_name(session, username)
    if not user:
        raise CredentialsException
    return user


@user_router.post('/token', tags=['signin'])
async def get_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                           session: AsyncSession = Depends(get_async_session)):
    user = await utils.authenticate_user(session, form.username, form.password)
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_token(
        data={'sub': user.username},
        expires_delta=expires
    )
    return {'token': access_token, "token_type": "bearer"}

@user_router.get('/current', response_model=schema.User)
async def current_user(user: Annotated[schema.User, Depends(get_current_user)]):
    return user