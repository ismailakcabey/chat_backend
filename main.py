import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.company.company_router import company_router

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_router, prefix="/company")


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
