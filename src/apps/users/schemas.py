from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRegisterSchema(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    is_active: bool