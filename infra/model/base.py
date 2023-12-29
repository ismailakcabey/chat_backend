from datetime import datetime
from pydantic import BaseModel


class BaseTypeModal(BaseModel):
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schemaExtra = {
            "example": {
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        }
