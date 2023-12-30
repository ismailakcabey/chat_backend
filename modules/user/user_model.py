from pydantic import Field
from datetime import datetime
from typing import Optional
from infra.model.objectid import ObjectId
from infra.model.base import BaseTypeModal
from modules.user.user_enum import RoleEnum


class User(BaseTypeModal):
    id: Optional[ObjectId] = Field(None, alias="_id", description="user id")
    fullname: str = Field(..., description="user name")
    email: str = Field(..., description="user email")
    phone_number: str = Field(..., description="user phone number")
    password: str = Field(..., description="user password")
    role: RoleEnum = Field(..., description="user role")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schemaExtra = {
            "example": {
                "id": "657582fcd96b7a266e3732f0",
                "fullname": "Name",
                "email": "email@example.com",
                "password": "password",
                "phone_number": "5555465654",
                "role": "USER",
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        }
