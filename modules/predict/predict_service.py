from modules.predict.predict_dto import CreatePredictDto, UpdatePredictDto
from datetime import datetime
from infra.db.mongo_connection import MongoConnection
from modules.predict.predict_model import Predict
from infra.model.repository import BaseRepository, Filter
import google.generativeai as genai
import os


class PredictService(BaseRepository):
    def __init__(self):
        self.db = MongoConnection.getInstance().get_db()
        print("predict service started")

    def bard_predict(self, converstationId: str, question: str):
        genai.configure(api_key=os.getenv("BARD_API_KEY"))
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        history = []
        convo = model.start_chat(history=history)
        convo.send_message(question)
        return convo.last.text

    def create_predict(self, predict: CreatePredictDto):
        predict_dict = predict.dict()
        predict_dict["createdAt"] = datetime.now()
        predict_dict["updatedAt"] = datetime.now()
        predict_result = self.bard_predict(
            converstationId=str(predict.converstationId), question=predict.question
        )
        predict_dict["answer"] = predict_result
        print("current prediction", predict_dict)
        return predict_dict
