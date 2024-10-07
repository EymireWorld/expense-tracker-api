from pydantic import EmailStr, Field

from app.schemas import Schema


class UserSingUpSchema(Schema):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserSingInSchema(Schema):
    username: str = Field(min_length=4, max_length=16)
    password: str = Field(min_length=8, max_length=64)


class TokenSchema(Schema):
    access_token: str
    token_type: str
