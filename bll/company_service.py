from typing import List
from dal.repository import IRepository
from bll.generic_service import GenericService
from bll.models import Company

class CompanyService(GenericService[Company]):
    def __init__(self, repository: IRepository):
        super().__init__(repository, "companies", Company)

    def find_by_name(self, name: str) -> List[Company]:
        if not name:
            return []
        name = name.lower()
        all_companies = self.get_all()
        return [c for c in all_companies if name in c.name.lower()]