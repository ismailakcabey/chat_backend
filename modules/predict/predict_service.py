from modules.predict.predict_dto import CreatePredictDto, UpdatePredictDto
from datetime import datetime
from infra.db.mongo_connection import MongoConnection
from modules.predict.predict_model import Predict
from infra.model.repository import BaseRepository, Filter
import google.generativeai as genai
import os
from openai import OpenAI
import base64
import requests
import json
from io import BytesIO
from tempfile import NamedTemporaryFile
from fastapi import WebSocket, WebSocketDisconnect
import logging


class PredictService(BaseRepository):
    def __init__(self):
        self.db = MongoConnection.getInstance().get_db()
        self.client = OpenAI(api_key=os.getenv("CHAT_GPT_API_KEY"))
        self.chat_gpt_text_to_speech_url = "https://api.openai.com/v1/audio/speech"
        self.chat_gpt_speech_to_text_url = (
            "https://api.openai.com/v1/audio/transcriptions"
        )
        self.chat_gpt_speech_to_text_headers = {
            "Authorization": "Bearer " + os.getenv("CHAT_GPT_API_KEY"),
            "Content-Type": "multipart/form-data",
        }
        self.chat_gpt_text_to_speech_headers = {
            "Authorization": "Bearer " + os.getenv("CHAT_GPT_API_KEY"),
            "Content-Type": "application/json",
        }

        print("predict service started")

    async def listen(self, websocket: WebSocket, converstationId: str):
        await websocket.accept()
        try:
            while True:
                # get message from websocket
                data = await websocket.receive_text()
                logging.warning(f"gelen veri {data}")
        except WebSocketDisconnect:
            print("disconnect oldu")

    def base64_to_wav(self, base64_text):
        # Base64'den ses dosyasını çöz
        audio_data = base64.b64decode(base64_text)
        audio_file = BytesIO(audio_data)

        # Base64'den çözülen ses dosyasını WAV formatına dönüştür
        with NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav.write(audio_file.getvalue())
            temp_wav_path = temp_wav.name

        return temp_wav_path

    def text_to_speech(self, text):
        response = requests.post(
            self.chat_gpt_text_to_speech_url,
            headers=self.chat_gpt_text_to_speech_headers,
            data=json.dumps({"model": "tts-1", "input": text, "voice": "alloy"}),
        )
        audio_content = response.content
        base64_encoded = base64.b64encode(audio_content)
        return base64_encoded

    def speech_to_text(self, base64_text):
        # Base64'den ses dosyasını çöz
        audio_data = base64.b64decode(base64_text)
        audio_file = BytesIO(audio_data)

        # OpenAI API'nin beklentisine uygun olarak dosyayı açın
        audio_file.seek(0)
        file_tuple = ("temp.wav", audio_file)

        # Transkripsiyon isteği oluştur
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", file=file_tuple
        )
        transcript_dict = transcript.dict()
        return transcript_dict["text"]

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
        filter = {"where": {"converstationId": converstationId}, "limit": 100}
        old_data = self.find_predict(filter)
        history = []
        for item in old_data["data"]:
            history.append({"role": "user", "parts": [item["question"]]})
            history.append({"role": "model", "parts": [item["answer"]]})
        convo = model.start_chat(history=history)
        convo.send_message(question)
        return convo.last.text

    def create_predict(self, predict: CreatePredictDto):
        predict_dict = predict.dict()
        predict_dict["createdAt"] = datetime.now()
        predict_dict["updatedAt"] = datetime.now()
        if predict.isInputVoice:
            question = self.speech_to_text(predict_dict["inputVoiceData"])
            predict_dict["question"] = question
        predict_result = self.bard_predict(
            converstationId=str(predict_dict["converstationId"]),
            question=predict_dict["question"],
        )
        predict_dict["answer"] = predict_result
        if predict.isOutputVoice:
            voice_output_data = self.text_to_speech(predict_dict["answer"])
            predict_dict["outputVoiceData"] = voice_output_data
        data = self.execute_create_data(self.db.Predict, predict_dict)
        return {"data": data, "message": "succesfuly predict"}

    def find_predict(self, filter: Filter):
        data = self.execute_find_filter(self.db.Predict, filter)
        return {
            "data": data["data"],
            "count": data["count"],
            "message": "succesfuly found predictions",
        }

    def update_predict(self, id: str, predict: UpdatePredictDto):
        data = self.execute_update_data(self.db.Predict, id, predict)
        return {"data": data, "message": "succesfuly update predict"}

    def delete_predict(self, id: str):
        data = self.execute_delete_data(self.db.Predict, id)
        return {"data": data, "message": "succesfuly delete prediction"}

    def find_by_id_predict(self, id: str, filter: Filter):
        data = self.execute_find_by_id_filter(self.db.Predict, id, filter)
        return {"data": data, "message": "succes found"}
