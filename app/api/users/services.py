from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserModel
from app.schemas import UserSchema


async def get_users(session: AsyncSession, offset: int, limit: int) -> list[UserSchema]:
    stmt = select(UserModel).offset(offset).limit(limit)
    result = await session.execute(stmt)

    return [UserSchema.model_validate(x) for x in result.scalars()]


async def get_user(session: AsyncSession, user_id: int) -> UserSchema:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    result = result.scalar()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )

    return UserSchema.model_validate(result)
