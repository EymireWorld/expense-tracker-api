from fastapi import APIRouter, Query

from app.api.records import services
from app.api.records.schemas import RecordAddSchema, RecordUpdateSchema
from app.dependencies import current_user_dep, session_dep
from app.schemas import RecordSchema


router = APIRouter(prefix='/records', tags=['Records'])


@router.get('')
async def get_records(
    session: session_dep,
    current_user: current_user_dep,
    offset: int = Query(0, ge=0, le=100),
    limit: int = Query(10, gt=0)
) -> list[RecordSchema]:
    return await services.get_records(session, current_user.id, offset, limit)


@router.get('/{record_id}')
async def get_record(
    session: session_dep,
    current_user: current_user_dep,
    record_id: int
) -> RecordSchema:
    return await services.get_record(session, current_user.id, record_id)


@router.post('')
async def add_record(
    session: session_dep,
    current_user: current_user_dep,
    data: RecordAddSchema
) -> RecordSchema:
    return await services.add_record(session, current_user.id, data)


@router.put('/{record_id}')
async def update_record(
    session: session_dep,
    current_user: current_user_dep,
    record_id: int,
    data: RecordUpdateSchema
):
    return await services.update_record(session, current_user.id, record_id, data)


@router.delete('/{record_id}')
async def remove_record(
    session: session_dep,
    current_user: current_user_dep,
    record_id: int
):
    await services.remove_record(session, current_user.id, record_id)
