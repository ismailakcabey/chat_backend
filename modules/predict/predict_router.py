from decorators.cbv import cbv
from fastapi import APIRouter, Body, Depends, Path
from modules.predict.predict_dto import CreatePredictDto, UpdatePredictDto
from infra.model.repository import Filter
from modules.predict.predict_service import PredictService
from modules.auth.auth_service import get_current_user

predict_router = APIRouter(tags=["PredictRouter"])


@cbv(predict_router)
class PredictRouter:
    def __init__(self, jwt=Depends(get_current_user)):
        self.service = PredictService()
        print("predict router started")

    @predict_router.post("/")
    def create_predict(self, predict: CreatePredictDto):
        """
        # Create a predict service
        """
        try:
            data = self.service.create_predict(predict)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}
