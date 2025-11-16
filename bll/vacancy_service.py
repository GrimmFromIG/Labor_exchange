from typing import List, Dict
from dal.repository import IRepository
from bll.generic_service import GenericService
from bll.models import Vacancy, Resume

class VacancyService(GenericService[Vacancy]):
    def __init__(self, repository: IRepository):
        super().__init__(repository, "vacancies", Vacancy)

    def find_by_keyword(self, keyword: str) -> List[Vacancy]:
        if not keyword:
            return []
        keyword = keyword.lower()
        all_vacancies = self.get_all()
        return [
            v for v in all_vacancies 
            if keyword in v.title.lower() 
            or keyword in v.description.lower()
            or keyword in v.qualifications.lower()
        ]
        
    def get_vacancies_for_company(self, company_id: str) -> List[Vacancy]:
        all_vacancies = self.get_all()
        return [v for v in all_vacancies if v.company_id == company_id]

    def _calculate_match_score(self, s1_vacancy: str, s2_resume: str) -> float:
        set1_vacancy = set(s.strip().lower() for s in s1_vacancy.split(',') if s.strip())
        set2_resume = set(s.strip().lower() for s in s2_resume.split(',') if s.strip())
        
        if not set2_resume:
            return 0.0
            
        intersection = set1_vacancy.intersection(set2_resume)
        return len(intersection) / len(set2_resume)

    def _calculate_reverse_match_score(self, s1_vacancy: str, s2_resume: str) -> float:
        set1_vacancy = set(s.strip().lower() for s in s1_vacancy.split(',') if s.strip())
        set2_resume = set(s.strip().lower() for s in s2_resume.split(',') if s.strip())
        
        if not set1_vacancy:
            return 0.0
            
        intersection = set1_vacancy.intersection(set2_resume)
        return len(intersection) / len(set1_vacancy)

    def find_matches_for_resume(self, resume: Resume, min_match: float = 0.25) -> List[Dict]:
        all_vacancies = self.get_all()
        matches = []
        for vacancy in all_vacancies:
            score = self._calculate_match_score(vacancy.qualifications, resume.qualifications)
            if score >= min_match:
                matches.append({"vacancy": vacancy, "score": score})
        return sorted(matches, key=lambda x: x["score"], reverse=True)

    def find_matches_for_vacancy(self, vacancy: Vacancy, all_resumes: List[Resume], min_match: float = 0.25) -> List[Dict]:
        matches = []
        for resume in all_resumes:
            score = self._calculate_reverse_match_score(vacancy.qualifications, resume.qualifications)
            if score >= min_match:
                matches.append({"resume": resume, "score": score})
        return sorted(matches, key=lambda x: x["score"], reverse=True)
