from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas import Schema


class UserSingUpSchema(Schema):
    name: str = Field(min_length=4, max_length=16)
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserSingInSchema(Schema):
    username: str = Field(min_length=4, max_length=16)
    password: str = Field(min_length=8, max_length=64)


class UserShowSchema(Schema):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class TokenSchema(Schema):
    access_token: str
    token_type: str
