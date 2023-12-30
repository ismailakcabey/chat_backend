from modules.user.user_dto import CreateUserDto, UpdateUserDto
from datetime import datetime
from infra.db.mongo_connection import MongoConnection
from modules.user.user_model import User
from infra.model.repository import BaseRepository, Filter
import bcrypt


class UserService(BaseRepository):
    def __init__(self):
        self.db = MongoConnection.getInstance().get_db()
        print("started user service")

    def create_user(self, user: CreateUserDto):
        user_dict = user.dict()
        user_dict["createdAt"] = datetime.now()
        user_dict["updatedAt"] = datetime.now()
        hashed_password = bcrypt.hashpw(
            user_dict["password"].encode("utf-8"), bcrypt.gensalt()
        )
        user_dict["password"] = hashed_password
        result = self.execute_create_data(self.db.User, user_dict)
        return {"data": result, "message": "successfuly created user"}

    def find_user(self, filter: Filter):
        data = self.execute_find_filter(self.db.User, filter)
        return {
            "data": data["data"],
            "count": data["count"],
            "message": "successfuly found user",
        }

    def update_user(self, id: str, user: UpdateUserDto):
        data = self.execute_update_data(self.db.User, id, user)
        return {"data": data, "message": "successfuly updated user"}

    def delete_user(self, id: str):
        data = self.execute_delete_data(self.db.User, id)
        return {"data": data, "message": "successfuly deleted user"}

    def find_by_id(self, id: str, filter: Filter = None):
        data = self.execute_find_by_id_filter(self.db.User, id, filter)
        return {"data": data, "message": "successfuly found user"}
