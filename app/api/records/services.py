from fastapi import HTTPException, status
from sqlalchemy import and_, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.records.schemas import RecordAddSchema, RecordUpdateSchema
from app.models import RecordModel
from app.schemas import RecordSchema


async def get_records(
    session: AsyncSession,
    user_id: int,
    offset: int,
    limit: int
) -> list[RecordSchema]:
    stmt = select(RecordModel).where(RecordModel.user_id == user_id).offset(offset).limit(limit)
    result = await session.execute(stmt)

    return [RecordSchema.model_validate(x) for x in result.scalars()]


async def get_record(
    session: AsyncSession,
    user_id: int,
    record_id: int
) -> RecordSchema:
    stmt = select(RecordModel).where(and_(
        RecordModel.user_id == user_id,
        RecordModel.id == record_id
    ))
    result = await session.execute(stmt)
    result = result.scalar()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Record not found.'
        )

    return RecordSchema.model_validate(result)


async def add_record(
    session: AsyncSession,
    user_id: int,
    data: RecordAddSchema
) -> RecordSchema:
    stmt = insert(RecordModel).values(
        user_id=user_id,
        amount=data.amount
    ).returning(RecordModel)
    result = await session.execute(stmt)

    return RecordSchema.model_validate(result.scalar)


async def update_record(
    session: AsyncSession,
    user_id: int,
    record_id: int,
    data: RecordUpdateSchema
) -> RecordSchema:
    stmt = update(RecordModel).values(
        **data.model_dump(exclude_unset=True)
    ).where(and_(
        RecordModel.user_id == user_id,
        RecordModel.id == record_id
    )).returning(RecordModel)
    result = await session.execute(stmt)
    result = result.scalar()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Record not found.'
        )

    return RecordSchema.model_validate(result)


async def remove_record(
    session: AsyncSession,
    user_id: int,
    record_id: int
):
    stmt = delete(RecordModel).where(and_(
        RecordModel.user_id == user_id,
        RecordModel.id == record_id
    )).returning(RecordModel)
    result = await session.execute(stmt)
    result = result.scalar()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Record not found.'
        )
