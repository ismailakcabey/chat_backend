import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.company.company_router import company_router
from modules.user.user_router import user_router
from modules.auth.auth_router import auth_router
from modules.converstation.converstation_router import converstation_router
from modules.predict.predict_router import predict_router

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_router, prefix="/company")
app.include_router(user_router, prefix="/user")
app.include_router(auth_router, prefix="/auth")
app.include_router(converstation_router, prefix="/converstation")
app.include_router(predict_router, prefix="/predict")


@app.get("/")
async def get_root():
    """_summary_

    this function main function

    Returns:
        _type_: _description_
    """
    if (root_url := os.environ.get("ROOT_URL")) is None:
        return {
            "api_docs": {
                "openapi": f"{root_url}/docs",
                "redoc": f"{root_url}/redoc",
            }
        }
    return {"message": "hello world"}
