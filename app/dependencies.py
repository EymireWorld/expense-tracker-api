from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_user
from app.database import get_session
from app.schemas import UserSchema


session_dep = Annotated[AsyncSession, Depends(get_session)]
current_user_dep = Annotated[UserSchema, Depends(get_current_user)]
