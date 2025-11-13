import streamlit as st
from dataclasses import asdict

from dal.repository import JsonRepository
from bll.services import LaborExchangeService
from bll.exceptions import ValidationException, EntityNotFoundException

try:
    repo = JsonRepository(filepath='dal/data.json')
    service = LaborExchangeService(repository=repo)
except Exception as e:
    st.error(f"Помилка ініціалізації сервісу: {e}")
    st.stop()


st.set_page_config(layout="wide")
st.title("👨‍💼 Варіант 5: Біржа праці")
st.caption("Виконав Петрощук Б. С., ФКНТ, Б-121-24-1-ПІ")

menu_option = st.sidebar.radio(
    "Оберіть розділ:",
    ["Безробітні", "Фірми-замовники", "Вакансії"]
)

if menu_option == "Безробітні":
    st.header("👤 Управління безробітними")
    
    tabs = st.tabs(["Перегляд та пошук", "Додати нового", "Видалити"])

    with tabs[0]:
        st.subheader("Список безробітних")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            sort_key = st.selectbox(
                "Сортувати за:",
                options=[("Прізвищем", "surname"), ("Ім'ям", "name")],
                format_func=lambda x: x[0]
            )
            
            try:
                unemployed_list = service.get_all_unemployed(sort_by=sort_key[1])
                st.info(f"Знайдено: {len(unemployed_list)} осіб(а).")
            except Exception as e:
                st.error(f"Помилка завантаження даних: {e}")
                unemployed_list = []

        with col2:
            if unemployed_list:
                st.dataframe(unemployed_list, use_container_width=True)
            else:
                st.info("Список безробітних порожній.") 

        st.subheader("Пошук безробітного")
        keyword = st.text_input("Введіть ім'я або прізвище для пошуку:")
        if keyword:
            try:
                results = service.find_unemployed_by_keyword(keyword)
                if results:
                    st.dataframe(results, use_container_width=True)
                else:
                    st.warning("Нікого не знайдено.")
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")

    with tabs[1]:
        st.subheader("Додавання безробітного")
        with st.form("add_unemployed_form"):
            name = st.text_input("Ім'я")
            surname = st.text_input("Прізвище")
            submitted = st.form_submit_button("Додати")
            
            if submitted:
                try:
                    person = service.add_unemployed(name, surname)
                    st.success(f"Додано: {person.name} {person.surname} (ID: {person.id})")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")

    with tabs[2]:
        st.subheader("Видалення безробітного")
        
        try:
            unemployed_list = service.get_all_unemployed(sort_by="surname")
            options = {f"{p.surname} {p.name} (ID: {p.id})": p.id for p in unemployed_list}
            
            if not options:
                st.warning("Немає безробітних для видалення.")
            else:
                selected_label = st.selectbox("Оберіть безробітного для видалення:", options.keys())
                
                if st.button("Видалити", type="primary"):
                    try:
                        person_id = options[selected_label]
                        service.delete_unemployed(person_id)
                        st.success(f"Безробітного {selected_label} видалено.")
                        st.experimental_rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")


elif menu_option == "Фірми-замовники":
    st.header("🏢 Управління фірмами-замовниками")
    
    tabs = st.tabs(["Перегляд", "Додати нову"])

    with tabs[0]:
        st.subheader("Список фірм")
        try:
            companies = service.get_all_companies(sort_by="name")
            
            if companies:
                st.dataframe(companies, use_container_width=True)
            else:
                st.info("Список фірм порожній.")
                
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")

    with tabs[1]:
        st.subheader("Додавання фірми")
        with st.form("add_company_form"):
            name = st.text_input("Назва фірми")
            submitted = st.form_submit_button("Додати")
            
            if submitted:
                try:
                    company = service.add_company(name)
                    st.success(f"Додано: {company.name} (ID: {company.id})")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")

elif menu_option == "Вакансії":
    st.header("📄 Управління вакансіями")
    
    tabs = st.tabs(["Перегляд та пошук", "Додати нову"])
    
    with tabs[0]:
        st.subheader("Список вакансій")
        try:
            vacancies = service.get_all_vacancies()
            
            if vacancies:
                st.dataframe(vacancies, use_container_width=True)
            else:
                st.info("Список вакансій порожній.")
                
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")
        
        st.subheader("Пошук вакансій")
        keyword = st.text_input("Введіть ключове слово для пошуку (в назві або описі):")
        if keyword:
            try:
                results = service.find_vacancies_by_keyword(keyword)
                if results:
                    st.dataframe(results, use_container_width=True)
                else:
                    st.warning("Нікого не знайдено.")
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")
                
    with tabs[1]:
        st.subheader("Додавання вакансії")
        with st.form("add_vacancy_form"):
            title = st.text_input("Назва вакансії (напр., 'Розробник Python')")
            description = st.text_area("Опис вакансії")
            
            submitted = st.form_submit_button("Додати")
            
            if submitted:
                try:
                    vacancy = service.add_vacancy(title, description)
                    st.success(f"Додано вакансію: {vacancy.title}")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")