
from typing import List, Dict, Any
from dataclasses import asdict

from bll.models import Unemployed, Company, Vacancy, Resume, Category
from dal.repository import JsonRepository
from bll.exceptions import ValidationException, EntityNotFoundException

class LaborExchangeService:
    def __init__(self, repository: JsonRepository):
        self.repository = repository

    def add_unemployed(self, name: str, surname: str) -> Unemployed:
        if not name or not surname:
            raise ValidationException("Ім'я та прізвище не можуть бути порожніми.")
        
        person = Unemployed(name=name, surname=surname)
        
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

    def find_unemployed_by_keyword(self, keyword: str) -> List[Unemployed]:
        if not keyword:
            return []
            
        keyword = keyword.lower()
        all_persons = self.get_all_unemployed()
        
        return [
            p for p in all_persons 
            if keyword in p.name.lower() or keyword in p.surname.lower()
        ]

    def delete_unemployed(self, person_id: str):
        data = self.repository.load_all_data()
        
        person_found = False
        for i, person_data in enumerate(data["unemployed"]):
            if person_data['id'] == person_id:
                data["unemployed"].pop(i)
                person_found = True
                break
        
        if not person_found:
            raise EntityNotFoundException(f"Безробітного з ID {person_id} не знайдено.")
            
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
    
    def add_vacancy(self, title: str, description: str) -> Vacancy:
        if not title:
            raise ValidationException("Назва вакансії не може бути порожньою.")
            
        vacancy = Vacancy(title=title, description=description)
        
        data = self.repository.load_all_data()
        data["vacancies"].append(asdict(vacancy))
        self.repository.save_all_data(data)
        
        return vacancy

    def get_all_vacancies(self) -> List[Vacancy]:
        data = self.repository.load_all_data()
        return [Vacancy(**v) for v in data["vacancies"]]

    def find_vacancies_by_keyword(self, keyword: str) -> List[Vacancy]:
        if not keyword:
            return []
            
        keyword = keyword.lower()
        all_vacancies = self.get_all_vacancies()
        
        return [
            v for v in all_vacancies 
            if keyword in v.title.lower() or keyword in v.description.lower()
        ]