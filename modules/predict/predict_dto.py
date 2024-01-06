from pydantic import BaseModel, Field
from typing import Optional
from infra.model.objectid import ObjectId


class CreatePredictDto(BaseModel):
    question: str = Field(...)
    converstationId: ObjectId = Field(...)

    class Config:
        schemaExtra = {
            "example": {
                "question": "can you say hello",
                "converstationId": "657582fcd96b7a266e3732f0",
            }
        }
        extra = "forbid"


class UpdatePredictDto(BaseModel):
    question: Optional[str] = Field(None)
    answer: Optional[str] = Field(None)
    converstationId: Optional[ObjectId] = Field(None)

    class Config:
        schemaExtra = {
            "example": {
                "question": "can you say hello",
                "answer": "can you say hello",
                "converstationId": "657582fcd96b7a266e3732f0",
            }
        }
        extra = "forbid"
