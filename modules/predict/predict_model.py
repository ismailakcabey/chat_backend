from pydantic import Field
from datetime import datetime
from typing import Optional, Union
from infra.model.objectid import ObjectId
from infra.model.base import BaseTypeModal


class Predict(BaseTypeModal):
    id: Optional[ObjectId] = Field(None, alias="_id", description="predict id")
    question: str = Field(..., description="predict question")
    answer: str = Field(..., description="predict answer")
    converstationId: ObjectId = Field(..., description="predict converstation id")
    inputVoiceData: Optional[str] = Field(..., description="predict input voice data")
    outputVoiceData: Optional[str] = Field(..., description="predict input voice data")
    isInputVoiceData: Optional[bool] = Field(..., description="input voice status")
    isOutputVoiceData: Optional[bool] = Field(..., description="output voice status")

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schemaExtra = {
            "example": {
                "id": "657582fcd96b7a266e3732f0",
                "question": "can you say hello",
                "answer": "hello",
                "converstationId": "657582fcd96b7a266e3732f0",
                "createdAt": datetime.now(),
                "updatedAt": datetime.now(),
            }
        }
