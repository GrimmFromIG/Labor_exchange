from typing import List, Dict, Any
from dataclasses import asdict

from bll.models import Unemployed, Company, Vacancy, Resume, Category
from dal.repository import JsonRepository
from bll.exceptions import ValidationException, EntityNotFoundException

class LaborExchangeService:
    def __init__(self, repository: JsonRepository):
        self.repository = repository

    def _find_item_index(self, data_list: List[Dict], item_id: str) -> int:
        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                return i
        raise EntityNotFoundException(f"Об'єкт з ID {item_id} не знайдено.")

    def add_unemployed(self, name: str, surname: str, qualifications: str) -> Unemployed:
        if not name or not surname:
            raise ValidationException("Ім'я та прізвище не можуть бути порожніми.")
        
        person = Unemployed(name=name, surname=surname, qualifications=qualifications)
        
        data = self.repository.load_all_data()
        data["unemployed"].append(asdict(person))
        self.repository.save_all_data(data)
        
        return person

    def get_all_unemployed(self, sort_by: str = None) -> List[Unemployed]:
        data = self.repository.load_all_data()
        unemployed_list = [Unemployed(**p) for p in data["unemployed"]]
        
        if sort_by == "name":
            unemployed_list.sort(key=lambda x: x.name)
        elif sort_by == "surname":
            unemployed_list.sort(key=lambda x: x.surname)
            
        return unemployed_list

    def get_unemployed_by_id(self, person_id: str) -> Unemployed:
        data = self.repository.load_all_data()
        for item in data["unemployed"]:
            if item['id'] == person_id:
                return Unemployed(**item)
        raise EntityNotFoundException(f"Безробітного з ID {person_id} не знайдено.")

    def update_unemployed(self, person_id: str, new_name: str, new_surname: str, new_qualifications: str) -> Unemployed:
        if not new_name or not new_surname:
            raise ValidationException("Ім'я та прізвище не можуть бути порожніми.")
        
        data = self.repository.load_all_data()
        index = self._find_item_index(data["unemployed"], person_id)
        
        data["unemployed"][index]["name"] = new_name
        data["unemployed"][index]["surname"] = new_surname
        data["unemployed"][index]["qualifications"] = new_qualifications
        
        self.repository.save_all_data(data)
        return Unemployed(**data["unemployed"][index])

    def find_unemployed_by_keyword(self, keyword: str) -> List[Unemployed]:
        if not keyword:
            return []
        keyword = keyword.lower()
        all_persons = self.get_all_unemployed()
        return [
            p for p in all_persons 
            if keyword in p.name.lower() or keyword in p.surname.lower()
        ]

    def find_unemployed_by_qualification(self, keyword: str) -> List[Unemployed]:
        if not keyword:
            return []
        keyword = keyword.lower()
        all_persons = self.get_all_unemployed()
        return [
            p for p in all_persons 
            if keyword in p.qualifications.lower()
        ]

    def delete_unemployed(self, person_id: str):
        data = self.repository.load_all_data()
        index = self._find_item_index(data["unemployed"], person_id)
        data["unemployed"].pop(index)
        self.repository.save_all_data(data)

    def add_company(self, name: str) -> Company:
        if not name:
            raise ValidationException("Назва компанії не може бути порожньою.")
        company = Company(name=name)
        data = self.repository.load_all_data()
        data["companies"].append(asdict(company))
        self.repository.save_all_data(data)
        return company

    def get_all_companies(self, sort_by: str = None) -> List[Company]:
        data = self.repository.load_all_data()
        company_list = [Company(**c) for c in data["companies"]]
        if sort_by == "name":
            company_list.sort(key=lambda x: x.name)
        return company_list
    
    def get_company_by_id(self, company_id: str) -> Company:
        data = self.repository.load_all_data()
        for item in data["companies"]:
            if item['id'] == company_id:
                return Company(**item)
        raise EntityNotFoundException(f"Компанію з ID {company_id} не знайдено.")

    def update_company(self, company_id: str, new_name: str) -> Company:
        if not new_name:
            raise ValidationException("Назва компанії не може бути порожньою.")
        data = self.repository.load_all_data()
        index = self._find_item_index(data["companies"], company_id)
        data["companies"][index]["name"] = new_name
        self.repository.save_all_data(data)
        return Company(**data["companies"][index])

    def delete_company(self, company_id: str):
        data = self.repository.load_all_data()
        index = self._find_item_index(data["companies"], company_id)
        data["companies"].pop(index)
        self.repository.save_all_data(data)
    
    def add_vacancy(self, title: str, description: str, qualifications: str) -> Vacancy:
        if not title:
            raise ValidationException("Назва вакансії не може бути порожньою.")
        vacancy = Vacancy(title=title, description=description, qualifications=qualifications)
        data = self.repository.load_all_data()
        data["vacancies"].append(asdict(vacancy))
        self.repository.save_all_data(data)
        return vacancy

    def get_all_vacancies(self, sort_by: str = None) -> List[Vacancy]:
        data = self.repository.load_all_data()
        vacancy_list = [Vacancy(**v) for v in data["vacancies"]]
        if sort_by == "title":
            vacancy_list.sort(key=lambda x: x.title)
        return vacancy_list

    def get_vacancy_by_id(self, vacancy_id: str) -> Vacancy:
         data = self.repository.load_all_data()
         for item in data["vacancies"]:
             if item['id'] == vacancy_id:
                 return Vacancy(**item)
         raise EntityNotFoundException(f"Вакансію з ID {vacancy_id} не знайдено.")

    def update_vacancy(self, vacancy_id: str, new_title: str, new_desc: str, new_qualifications: str) -> Vacancy:
        if not new_title:
            raise ValidationException("Назва вакансії не може бути порожньою.")
        data = self.repository.load_all_data()
        index = self._find_item_index(data["vacancies"], vacancy_id)
        data["vacancies"][index]["title"] = new_title
        data["vacancies"][index]["description"] = new_desc
        data["vacancies"][index]["qualifications"] = new_qualifications
        self.repository.save_all_data(data)
        return Vacancy(**data["vacancies"][index])

    def delete_vacancy(self, vacancy_id: str):
        data = self.repository.load_all_data()
        index = self._find_item_index(data["vacancies"], vacancy_id)
        data["vacancies"].pop(index)
        self.repository.save_all_data(data)

    def find_vacancies_by_keyword(self, keyword: str) -> List[Vacancy]:
        if not keyword:
            return []
        keyword = keyword.lower()
        all_vacancies = self.get_all_vacancies()
        return [
            v for v in all_vacancies 
            if keyword in v.title.lower() or keyword in v.description.lower()
        ]
    
    def add_resume(self, title: str, unemployed_id: str, skills: str) -> Resume:
        if not title or not unemployed_id:
            raise ValidationException("Назва та ID безробітного є обов'язковими.")
        
        person = self.get_unemployed_by_id(unemployed_id) 
        
        resume = Resume(
            title=title, 
            unemployed_id=unemployed_id, 
            skills_description=skills,
            qualifications=person.qualifications
        )
        data = self.repository.load_all_data()
        data["resumes"].append(asdict(resume))
        self.repository.save_all_data(data)
        return resume

    def get_all_resumes(self, sort_by: str = None) -> List[Resume]:
        data = self.repository.load_all_data()
        resume_list = [Resume(**r) for r in data["resumes"]]
        if sort_by == "title":
            resume_list.sort(key=lambda x: x.title)
        return resume_list
        
    def get_resume_by_id(self, resume_id: str) -> Resume:
         data = self.repository.load_all_data()
         for item in data["resumes"]:
             if item['id'] == resume_id:
                 return Resume(**item)
         raise EntityNotFoundException(f"Резюме з ID {resume_id} не знайдено.")

    def update_resume(self, resume_id: str, new_title: str, new_skills: str) -> Resume:
        if not new_title:
            raise ValidationException("Назва резюме не може бути порожньою.")
        data = self.repository.load_all_data()
        index = self._find_item_index(data["resumes"], resume_id)
        data["resumes"][index]["title"] = new_title
        data["resumes"][index]["skills_description"] = new_skills
        self.repository.save_all_data(data)
        return Resume(**data["resumes"][index])

    def delete_resume(self, resume_id: str):
        data = self.repository.load_all_data()
        index = self._find_item_index(data["resumes"], resume_id)
        data["resumes"].pop(index)
        self.repository.save_all_data(data)