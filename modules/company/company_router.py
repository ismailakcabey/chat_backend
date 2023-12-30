from decorators.cbv import cbv
from fastapi import APIRouter, Body, Depends, Path
from modules.company.company_dto import CreateCompanyDto, UpdateCompanyDto
from infra.model.repository import Filter
from modules.company.company_service import CompanyService
from modules.auth.auth_service import get_current_user

company_router = APIRouter(tags=["CompanyRouter"])


@cbv(company_router)
class CompanyRouter:
    def __init__(self, jwt=Depends(get_current_user)):
        self.service = CompanyService()
        print("started company router")

    @company_router.post("/")
    async def create_company(self, company: CreateCompanyDto = Body(...)):
        """
        # Create a company service
        """
        try:
            data = self.service.create_company(company)
            return data
        except Exception as e:
            print("error creating company service", e)
            return {"message": f"failed {e}"}

    @company_router.post("/find")
    def find_company(self, filter: Filter = Body(None)):
        """
        # Find a company service
        """
        try:
            data = self.service.find_company(filter)
            return data
        except Exception as e:
            return {"message": f"failed {e}"}

    @company_router.get("/{id}")
    def find_by_id(self, id: str = Path(...), filter: Filter = Body(None)):
        """
        # Find By Id A Company Service
        """
        try:
            data = self.service.find_by_id(id, filter)
            return {"data": data, "message": f"company found successfully"}
        except Exception as e:
            return {"message": f"failed to find {e}"}

    @company_router.patch("/{id}")
    def update_company(
        self, id: str = Path(...), company: UpdateCompanyDto = Body(...)
    ):
        """
        # Update a company service
        """
        try:
            data = self.service.update_company(id, company)
            return {"data": data, "message": "successful update"}
        except Exception as e:
            return {"message": f"failed {e}"}

    @company_router.delete("/{id}")
    def delete_company(self, id: str = Path(...)):
        """
        # Delete a company service
        """
        try:
            data = self.service.delete_company(id)
            return {"data": data, "message": "deleted successfully"}
        except Exception as e:
            return {"message": f"failed {e}"}
