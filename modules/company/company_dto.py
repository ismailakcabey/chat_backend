from pydantic import BaseModel, Field
from typing import Optional


class CreateCompanyDto(BaseModel):
    name: str = Field(...)

    class Config:
        schemaExtra = {
            "example": {
                "name": "Name",
            }
        }
        extra = "forbid"  # extra alana izin verilmiyor


class UpdateCompanyDto(BaseModel):
    name: Optional[str] = Field(...)

    class Config:
        schemaExtra = {
            "example": {
                "name": "Name",
            }
        }
        extra = "forbid"  # extra alana izin verilmiyor
