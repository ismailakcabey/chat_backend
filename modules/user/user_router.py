from decorators.cbv import cbv
from fastapi import APIRouter, Body, Path, Depends
from modules.user.user_dto import CreateUserDto, UpdateUserDto
from infra.model.repository import Filter
from modules.user.user_service import UserService
from modules.auth.auth_service import get_current_user

user_router = APIRouter(tags=["UserRouter"])


@cbv(user_router)
class UserRouter:
    def __init__(self):
        self.service = UserService()
        print("started user router")

    @user_router.post("/")
    async def create_user(self, user: CreateUserDto = Body(...)):
        """
        # Create a user service
        """
        try:
            data = self.service.create_user(user)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @user_router.post("/find")
    async def find_user(
        self, filter: Filter | None = Body(None), jwt=Depends(get_current_user)
    ):
        """
        # Find a user service
        """
        try:
            data = self.service.find_user(filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @user_router.get("/{id}")
    def find_by_id_user(
        self,
        id: str = Path(...),
        filter: Filter = Body(None),
        jwt=Depends(get_current_user),
    ):
        """
        # Find by id user service
        """
        try:
            data = self.service.find_by_id(id, filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @user_router.patch("/{id}")
    def update_user(
        self,
        id: str = Path(...),
        user: UpdateUserDto = Body(...),
        jwt=Depends(get_current_user),
    ):
        try:
            data = self.service.update_user(id, user)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @user_router.delete("/{id}")
    def delete_user(self, id: str = Path(...), jwt=Depends(get_current_user)):
        try:
            data = self.service.delete_user(id)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}
