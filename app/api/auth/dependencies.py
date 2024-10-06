from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import UserModel
from app.settings import JWT_TOKEN_LIFETIME


def encode_jwt(user_id: int) -> str:
    data = {
        'user_id': user_id,
        'end_at': int((datetime.now(timezone.utc) + timedelta(seconds= JWT_TOKEN_LIFETIME)).timestamp())
    }

    with open('certificates\\jwt-private.pem', encoding= 'utf-8') as key_file:
        private_key = key_file.read()

    return jwt.encode(data, private_key, 'RS256')


def decode_jwt(token: str | bytes) -> dict:
    with open('certificates\\jwt-public.pem', encoding= 'utf-8') as key_file:
        public_key = key_file.read()

    return jwt.decode(token, public_key, ['RS256'])


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: AsyncSession = Depends(get_session)
):
    if credentials.scheme != 'Bearer':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid authentication scheme.'
        )

    data = decode_jwt(credentials.credentials)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token.'
        )
    if data['end_at'] < int(datetime.now(timezone.utc).timestamp()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Expired token.'
        )

    stmt = select(UserModel).where(UserModel.id == data['user_id'])
    result = await session.execute(stmt)

    return result.scalar()
