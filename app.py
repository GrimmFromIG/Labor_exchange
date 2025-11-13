import streamlit as st

from dal.repository import JsonRepository
from bll.services import LaborExchangeService

from pl.unemployed_view import show_unemployed_page
from pl.companies_view import show_companies_page
from pl.vacancies_view import show_vacancies_page
from pl.resumes_view import show_resumes_page

def main():
    try:
        repo = JsonRepository(filepath='dal/data.json')
        service = LaborExchangeService(repository=repo)
    except Exception as e:
        st.error(f"Помилка ініціалізації сервісу: {e}")
        st.stop()

    st.set_page_config(layout="wide")
    st.title("👨‍💼 Варіант 5: Біржа праці")
    st.caption("Виконав Петрощук Б. С., ФКНТ, Б-121-24-1-ПІ")

    menu_options = {
        "Безробітні": show_unemployed_page,
        "Фірми-замовники": show_companies_page,
        "Вакансії": show_vacancies_page,
        "Резюме": show_resumes_page
    }

    menu_selection = st.sidebar.radio(
        "Оберіть розділ:",
        options=menu_options.keys()
    )

    page_function = menu_options[menu_selection]
    page_function(service)

if __name__ == "__main__":
    main()