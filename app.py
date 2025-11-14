import streamlit as st

from dal.repository import JsonRepository
from bll.unemployed_service import UnemployedService
from bll.company_service import CompanyService
from bll.vacancy_service import VacancyService
from bll.resume_service import ResumeService

from pl.unemployed_view import show_unemployed_page
from pl.companies_view import show_companies_page
from pl.vacancies_view import show_vacancies_page
from pl.resumes_view import show_resumes_page
from pl.matching_view import show_matching_page
from pl.statistics_view import show_statistics_page

def main():
    try:
        repo = JsonRepository(filepath='dal/data.json')
        
        unemployed_service = UnemployedService(repo)
        company_service = CompanyService(repo)
        vacancy_service = VacancyService(repo)
        resume_service = ResumeService(repo, unemployed_service)
        
    except Exception as e:
        st.error(f"Помилка ініціалізації сервісу: {e}")
        st.stop()

    st.set_page_config(layout="wide")
    st.title("👨‍💼 Варіант 5: Біржа праці (OOP Refactored)")
    st.caption("Виконав Петрощук Б. С., ФКНТ, Б-121-24-1-ПІ")

    menu_options = {
        "Безробітні": lambda: show_unemployed_page(unemployed_service, resume_service),
        "Фірми-замовники": lambda: show_companies_page(company_service, vacancy_service),
        "Вакансії": lambda: show_vacancies_page(vacancy_service, company_service),
        "Резюме": lambda: show_resumes_page(resume_service, unemployed_service),
        "Підбір (Matching)": lambda: show_matching_page(resume_service, vacancy_service),
        "Статистика": lambda: show_statistics_page(unemployed_service)
    }

    menu_selection = st.sidebar.radio(
        "Оберіть розділ:",
        options=menu_options.keys()
    )

    page_function = menu_options[menu_selection]
    page_function()

if __name__ == "__main__":
    main()