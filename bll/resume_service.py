from typing import List
from dal.repository import IRepository
from bll.generic_service import GenericService
from bll.models import Resume
from bll.unemployed_service import UnemployedService
from bll.exceptions import ValidationException

class ResumeService(GenericService[Resume]):
    def __init__(self, repository: IRepository, unemployed_service: UnemployedService):
        super().__init__(repository, "resumes", Resume)
        self._unemployed_service = unemployed_service

    def add(self, entity: Resume) -> Resume:
        if not entity.title or not entity.unemployed_id:
            raise ValidationException("Назва та ID безробітного є обов'язковими.")
        
        person = self._unemployed_service.get_by_id(entity.unemployed_id)
        entity.qualifications = person.qualifications
        
        return super().add(entity)

    def get_resumes_for_unemployed(self, unemployed_id: str) -> List[Resume]:
        all_resumes = self.get_all()
        return [r for r in all_resumes if r.unemployed_id == unemployed_id]