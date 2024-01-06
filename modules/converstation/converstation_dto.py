from pydantic import BaseModel, Field
from typing import Optional


class CreateConverstationDto(BaseModel):
    name: str = Field(...)

    class Config:
        schemaExtra = {"example": {"name": "name"}}
        extra = "forbid"


class UpdateConverstationDto(BaseModel):
    name: Optional[str] = Field(None)

    class Config:
        schemaExtra = {"example": {"name": "example"}}
        extra = "forbid"
