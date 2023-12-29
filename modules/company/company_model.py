from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional
from infra.model.objectid import ObjectId
from infra.model.base import BaseTypeModal


class Company(BaseTypeModal):
    id: Optional[ObjectId] = Field(None, alias="_id", description="company id data")
    name: str = Field(..., description="company name")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schemaExtra = {
            "example": {
                "id": "657582fcd96b7a266e3732f0",
                "name": "Name",
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        }
