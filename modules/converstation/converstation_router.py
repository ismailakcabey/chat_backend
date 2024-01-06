from decorators.cbv import cbv
from fastapi import APIRouter, Body, Depends, Path
from modules.converstation.converstation_dto import (
    CreateConverstationDto,
    UpdateConverstationDto,
)
from infra.model.repository import Filter
from modules.converstation.converstation_service import ConverstationService
from modules.auth.auth_service import get_current_user

converstation_router = APIRouter(tags=["ConverstationRouter"])


@cbv(converstation_router)
class ConverstationRouter:
    def __init__(self, jwt=Depends(get_current_user)):
        self.service = ConverstationService()
        print("started converstation router")

    @converstation_router.post("/")
    def create_converstation(self, converstation: CreateConverstationDto):
        """
        # Create a converstation service
        """
        try:
            data = self.service.create_converstation(converstation)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @converstation_router.post("/find")
    def find_converstation(self, filter: Filter = Body(None)):
        """
        # Find a converstation service
        """
        try:
            data = self.service.find_converstation(filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @converstation_router.get("/{id}")
    def find_by_id(self, id: str = Path(...), filter=Body(None)):
        """
        # Find by id a converstation service
        """
        try:
            data = self.service.find_by_id_converstation(id, filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @converstation_router.patch("/{id}")
    def update_converstation(
        self, id: str = Path(...), converstation: UpdateConverstationDto = Body(...)
    ):
        try:
            data = self.service.update_converstation(id, converstation)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @converstation_router.delete("/{id}")
    def delete_converstation(self, id: str = Path(...)):
        try:
            data = self.service.delete_converstation(id)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}
