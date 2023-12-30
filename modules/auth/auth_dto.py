from pydantic import BaseModel, Field
from typing import Optional


class LoginDto(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schemaExtra = {
            "example": {
                "email": "ismial@example.com",
                "password": "ismial@example.com",
            }
        }
        extra = "forbid"  # extra alana izin verilmiyor
