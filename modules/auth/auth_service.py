from modules.user.user_service import UserService
from modules.auth.auth_dto import LoginDto
import bcrypt
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from modules.user.user_enum import RoleEnum

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        secret_key = "your_secret_key"
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_role_admin(user: dict = Depends(get_current_user)):
    if user["role"] == RoleEnum.ADMIN:
        return user
    else:
        raise HTTPException(status_code=401, detail="only admin user")


async def get_current_role_user(user: dict = Depends(get_current_user)):
    if user["role"] == RoleEnum.USER:
        return user
    else:
        raise HTTPException(status_code=401, detail="only admin user")


class AuthService:
    def __init__(self):
        self.user_service = UserService()
        print("user service started")

    def login_user(self, login: LoginDto):
        login_status = False
        filter = {"where": {"email": login.email}}
        user = self.user_service.find_user(filter)
        newData = bcrypt.checkpw(
            login.password.encode("utf-8"), user["data"][0]["password"]
        )
        login_status = newData
        if login_status == False:
            return {"message": "incorrect password or email", "status": login_status}
        secret_key = "your_secret_key"
        payload = {"id": user["data"][0]["_id"], "role": user["data"][0]["role"]}
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        token = jwt.encode(
            {"exp": expiration_time, **payload}, secret_key, algorithm="HS256"
        )
        return {
            "message": "login user",
            "data": user["data"][0],
            "loginStatus": login_status,
            "token": token,
        }

    def decode_token(self, token):
        try:
            secret_key = "your_secret_key"
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            if not payload:
                HTTPException(status_code=401, detail="unauth user")
            return payload
        except jwt.ExpiredSignatureError:
            return {"message": f"token is expired"}
        except jwt.InvalidTokenError:
            return {"message": f"token is invalid"}

    def get_me(self, token: str):
        user = self.decode_token(token)
        return {"message": "found user", "data": user}
