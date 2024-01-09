from decorators.cbv import cbv
from fastapi import APIRouter, Body, Depends, Path, WebSocket
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

    @predict_router.websocket("/ws/manager/listen/{converstationId}")
    async def listen_socket(self, websocket: WebSocket, converstationId: str):
        await self.service.listen(websocket, converstationId)

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

    @predict_router.post("/find")
    def find_predict(self, filter: Filter = Body(...)):
        """
        # Find a predict service
        """
        try:
            data = self.service.find_predict(filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @predict_router.get("/{id}")
    def find_by_id_predict(self, id: str = Path(...), filter: Filter = Body(...)):
        """
        # Find a predict service by id
        """
        try:
            data = self.service.find_by_id_predict(id, filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @predict_router.patch("/{id}")
    def update_by_id_predict(self, id: str, predict: UpdatePredictDto):
        """
        # Update a predict service
        """
        try:
            data = self.service.update_predict(id, predict)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @predict_router.delete("/{id}")
    def delete_by_id_predict(self, id: str):
        """
        # Delete a predict service
        """
        try:
            data = self.service.delete_predict(id)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}
