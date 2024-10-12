from fastapi import APIRouter

from app.api.auth.router import router as auth_router
from app.api.records.router import router as records_router


router = APIRouter(prefix='/api')
router.include_router(auth_router)
router.include_router(records_router)
