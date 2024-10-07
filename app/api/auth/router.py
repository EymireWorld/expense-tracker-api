from fastapi import APIRouter

from app.api.auth import services
from app.api.auth.schemas import (
    TokenSchema,
    UserSingInSchema,
    UserSingUpSchema
)
from app.api.users.schemas import UserShowSchema
from app.dependencies import current_user_dep, session_dep


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/sign_in')
async def sign_in(session: session_dep, data: UserSingInSchema) -> TokenSchema:
    return await services.sing_in(session, data)


@router.post('/sign_up')
async def sign_up(session: session_dep, data: UserSingUpSchema) -> TokenSchema:
    return await services.sing_up(session, data)


@router.get('/me')
async def profile(current_user: current_user_dep) -> UserShowSchema:
    return current_user  # type: ignore
