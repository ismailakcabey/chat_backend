from pydantic import Field
from datetime import datetime
from typing import Optional
from infra.model.objectid import ObjectId
from infra.model.base import BaseTypeModal


class Converstation(BaseTypeModal):
    id: Optional[ObjectId] = Field(None, alias="_id", description="converstation id")
    name: str = Field(..., description="converstation name")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schemaExtra = {
            "example": {
                "id": "657582fcd96b7a266e3732f0",
                "name": "example",
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        }
