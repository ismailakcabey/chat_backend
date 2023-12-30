from decorators.cbv import cbv
from fastapi import APIRouter, Body, Depends
from modules.auth.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
from modules.auth.auth_dto import LoginDto

auth_router = APIRouter(
    tags=["AuthRouter"],
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@cbv(auth_router)
class AuthRouter:
    def __init__(self):
        self.service = AuthService()
        print("auth service started")

    @auth_router.post("/login")
    async def login_user(self, login: LoginDto = Body(...)):
        """
        # Login user service
        """
        try:
            data = self.service.login_user(login)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @auth_router.get("/me")
    async def login_me(self, token: str = Depends(oauth2_schema)):
        """
        # Get Me service
        """
        try:
            data = self.service.get_me(token)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}
