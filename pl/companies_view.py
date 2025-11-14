import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from bll.models import Company
from pl.utils import get_selection_options

def show_companies_page(company_service, vacancy_service):
    st.header("🏢 Управління фірмами-замовниками")
    
    tabs = st.tabs(["Перегляд", "Додати нову", "Редагувати", "Видалити", "Вакансії компанії"])

    with tabs[0]:
        st.subheader("Список фірм")
        try:
            companies = company_service.get_all()
            companies.sort(key=lambda x: x.name)
            if companies:
                st.dataframe(companies, use_container_width=True, hide_index=True)
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
                    new_company = Company(name=name)
                    company_service.add(new_company)
                    st.success(f"Додано: {new_company.name}")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")
    
    with tabs[2]:
        st.subheader("Редагування даних")
        try:
            companies = company_service.get_all()
            options = get_selection_options(companies, 'name', None)
            
            if not options:
                st.warning("Немає фірм для редагування.")
            else:
                selected_label = st.selectbox("Оберіть фірму:", options.keys(), key="edit_comp_select")
                selected_id = options[selected_label]
                company = company_service.get_by_id(selected_id)
                
                with st.form("edit_company_form"):
                    name = st.text_input("Назва", value=company.name)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            company.name = name
                            company_service.update(company)
                            st.success(f"Назву фірми оновлено на {name}.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")
            
    with tabs[3]:
        st.subheader("Видалення фірми")
        try:
            companies = company_service.get_all()
            options = get_selection_options(companies, 'name', None)
            
            if not options:
                st.warning("Немає фірм для видалення.")
            else:
                selected_label = st.selectbox("Оберіть фірму для видалення:", options.keys(), key="del_comp_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        company_id = options[selected_label]
                        company_service.delete(company_id)
                        st.success(f"Фірму {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

    with tabs[4]:
        st.subheader("Перегляд вакансій компанії")
        try:
            companies = company_service.get_all()
            options = get_selection_options(companies, 'name', None)
            
            if not options:
                st.warning("Немає компаній для перегляду.")
            else:
                selected_label = st.selectbox("Оберіть компанію:", options.keys(), key="view_vacancies_select")
                selected_id = options[selected_label]
                
                vacancies = vacancy_service.get_vacancies_for_company(selected_id)
                if vacancies:
                    st.write(f"Вакансії для {selected_label}:")
                    st.dataframe(vacancies, use_container_width=True, hide_index=True)
                else:
                    st.info(f"У {selected_label} ще немає вакансій.")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")