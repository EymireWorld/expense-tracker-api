from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes= True)


class UserSchema(Schema):
    id: int
    username: str
    email: EmailStr
    hashed_password: bytes
    created_at: datetime


class RecordSchema(Schema):
    id: int
    user_id: int
    amount: float
    created_at: datetime
