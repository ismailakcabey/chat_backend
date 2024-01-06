from modules.converstation.converstation_dto import (
    CreateConverstationDto,
    UpdateConverstationDto,
)
from datetime import datetime
from infra.db.mongo_connection import MongoConnection
from modules.converstation.converstation_model import Converstation
from infra.model.repository import BaseRepository, Filter


class ConverstationService(BaseRepository):
    def __init__(self):
        self.db = MongoConnection.getInstance().get_db()
        print("starter converstation service")

    def create_converstation(self, converstation: CreateConverstationDto):
        converstation_dict = converstation.dict()
        converstation_dict["createdAt"] = datetime.now()
        converstation_dict["updatedAt"] = datetime.now()
        result = self.execute_create_data(self.db.Converstation, converstation_dict)
        return {"data": result, "message": "succesfuly created converstation"}

    def find_converstation(self, filter: Filter):
        data = self.execute_find_filter(self.db.Converstation, filter)
        return {
            "data": data["data"],
            "count": data["count"],
            "message": "succesfuly found converstation",
        }

    def update_converstation(self, id: str, converstation: UpdateConverstationDto):
        data = self.execute_update_data(self.db.Converstation, id, converstation)
        return {
            "data": data,
            "message": "successfuly updated converstation",
        }

    def delete_converstation(self, id: str):
        data = self.execute_delete_data(self.db.Converstation, id)
        return {"data": data, "message": "succesfly deleted converstation"}

    def find_by_id_converstation(self, id: str, filter: Filter):
        data = self.execute_find_by_id_filter(self.db.Converstation, id, filter)
        return {"data": data, "message": "successfly founded converstation"}
