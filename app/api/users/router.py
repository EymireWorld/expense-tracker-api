from fastapi import APIRouter, Query

from app.api.users import services
from app.api.users.schemas import UserShowSchema
from app.dependencies import current_user_dep, session_dep


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('')
async def get_users(
    session: session_dep,
    offset: int = Query(0, ge=0, le=100),
    limit: int = Query(10, gt=0)
) -> list[UserShowSchema]:
    return await services.get_users(session, offset, limit)  # type: ignore


@router.get('/{user_id}')
async def get_user(session: session_dep, user_id: int)-> UserShowSchema:
    return await services.get_user(session, user_id)  # type: ignore
