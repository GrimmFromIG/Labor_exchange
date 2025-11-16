from typing import List, Dict, Any
from collections import Counter
from dal.repository import IRepository
from bll.generic_service import GenericService
from bll.models import Unemployed

class UnemployedService(GenericService[Unemployed]):
    def __init__(self, repository: IRepository):
        super().__init__(repository, "unemployed", Unemployed)

    def find_by_qualification(self, keyword: str) -> List[Unemployed]:
        if not keyword:
            return []
        keyword = keyword.lower()
        all_persons = self.get_all()
        return [p for p in all_persons if keyword in p.qualifications.lower()]

    def find_by_keyword(self, keyword: str) -> List[Unemployed]:
        if not keyword:
            return []
        keyword = keyword.lower()
        all_persons = self.get_all()
        return [
            p for p in all_persons 
            if keyword in p.name.lower() or keyword in p.surname.lower()
        ]

    def get_statistics(self) -> Dict[str, Any]:
        all_unemployed = self.get_all()
        total = len(all_unemployed)
        
        all_skills = []
        for person in all_unemployed:
            all_skills.extend([
                s.strip().lower() for s in person.qualifications.split(',') if s.strip()
            ])
            
        if not all_skills:
            top_skill = "N/A"
        else:
            top_skill = Counter(all_skills).most_common(1)[0][0]
            
        return {"total_unemployed": total, "top_qualification": top_skill}