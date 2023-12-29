from modules.company.company_dto import CreateCompanyDto, UpdateCompanyDto
from datetime import datetime
from infra.db.mongo_connection import MongoConnection
from modules.company.company_model import Company
from infra.model.repository import BaseRepository, Filter
from modules.company.company_model import Company


class CompanyService(BaseRepository):
    def __init__(self):
        self.db = MongoConnection.getInstance().get_db()
        print("started company service")

    def create_company(self, company: CreateCompanyDto):
        company_dict = company.dict()
        company_dict["createdAt"] = datetime.now()
        company_dict["updatedAt"] = datetime.now()
        result = self.execute_create_data(self.db.Company, company_dict)
        return {"data": result, "message": "successfully created company"}

    def find_company(self, filter: Filter):
        data = self.execute_find_filter(self.db.Company, filter)
        return {
            "data": data["data"],
            "count": data["count"],
            "message": "successfully found company",
        }

    def update_company(self, id: str, company: UpdateCompanyDto):
        data = self.execute_update_data(self.db.Company, id, company)
        return {"data": data, "message": "successfully updated company"}

    def delete_company(self, id: str):
        data = self.execute_delete_data(self.db.Company, id)
        return {"data": data, "message": "successfully deleted company"}

    def find_by_id(self, id: str, filter: Filter = None):
        data = self.execute_find_by_id_filter(self.db.Company, id, filter)
        return {"data": data, "message": "successfully found company"}
