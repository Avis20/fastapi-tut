from pydantic import BaseModel, EmailStr, UUID4, Field, validator
from datetime import datetime


class UserCreate(BaseModel):
    """Проверка создания пользователя"""

    email: EmailStr
    name: str
    password: str


class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    ts_expires: datetime

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def token2hex(cls, value):
        """Конвертируем uuid в hex формат"""
        return value.hex


class User(UserCreate):
    token: TokenBase = {}
