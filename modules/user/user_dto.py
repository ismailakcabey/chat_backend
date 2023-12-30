from pydantic import BaseModel, Field
from typing import Optional
from modules.user.user_enum import RoleEnum


class CreateUserDto(BaseModel):
    fullname: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    phone_number: Optional[str] = Field(None)
    role: Optional[RoleEnum] = Field("USER")

    class Config:
        schemaExtra = {
            "example": {
                "fullname": "Name",
                "email": "ismial@example.com",
                "password": "ismial@example.com",
                "phone_number": "5555455654",
                "role": "USER",
            }
        }
        extra = "forbid"  # extra alana izin verilmiyor


class UpdateUserDto(BaseModel):
    fullname: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone_number: Optional[str] = Field(None)
    role: Optional[str] = Field(None)

    class Config:
        schemaExtra = {
            "example": {
                "fullname": "Name",
                "email": "ismial@example.com",
                "phone_number": "5555455654",
                "role": "USER",
            }
        }
        extra = "forbid"  # extra alana izin verilmiyor
