from fastapi import HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import (
    encode_jwt,
    hash_password,
    validate_password
)
from app.api.auth.schemas import (
    TokenSchema,
    UserSingInSchema,
    UserSingUpSchema
)
from app.models import UserModel


async def sing_in(session: AsyncSession, data: UserSingInSchema):
    stmt = select(UserModel).where(UserModel.username == data.username)
    result = await session.execute(stmt)
    result = result.scalar()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password.'
        )

    if not validate_password(data.password, result.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password.'
        )

    return TokenSchema(access_token=encode_jwt(result.id), token_type='Bearer')


async def sing_up(session: AsyncSession, data: UserSingUpSchema):
    stmt = insert(UserModel).values(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password)
    ).returning(UserModel.id)

    try:
        result = await session.execute(stmt)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username or email is already registered.'
        )
    else:
        await session.commit()

    user_id = result.scalar()

    return TokenSchema(access_token=encode_jwt(user_id), token_type='Bearer')  # type: ignore
