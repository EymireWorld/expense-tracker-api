from datetime import datetime

from pydantic import EmailStr

from app.schemas import Schema


class UserShowSchema(Schema):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
