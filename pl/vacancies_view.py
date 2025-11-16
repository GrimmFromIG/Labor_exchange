import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from bll.models import Vacancy
from pl.utils import get_selection_options

def show_vacancies_page(vacancy_service, company_service):
    st.header("📄 Управління вакансіями")
    
    tabs = st.tabs(["Перегляд та пошук", "Додати нову", "Редагувати", "Видалити"])
    
    with tabs[0]:
        st.subheader("Список вакансій")
        
        try:
            vacancies = vacancy_service.get_all()
            vacancies.sort(key=lambda x: x.title)
            if vacancies:
                st.dataframe(vacancies, use_container_width=True, hide_index=True)
            else:
                st.info("Список вакансій порожній.")
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")
        
        st.subheader("Пошук вакансій")
        keyword_vac = st.text_input("Введіть ключове слово (назва, опис, кваліфікації):")
        if keyword_vac:
            try:
                results_vac = vacancy_service.find_by_keyword(keyword_vac)
                st.dataframe(results_vac, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")
                
    with tabs[1]:
        st.subheader("Додавання вакансії")
        try:
            companies = company_service.get_all()
            options = get_selection_options(companies, 'name', None)
            
            if not options:
                st.warning("Спочатку додайте фірму-замовника, щоб створити вакансію.")
            else:
                with st.form("add_vacancy_form"):
                    title = st.text_input("Назва вакансії")
                    selected_label = st.selectbox("Оберіть компанію:", options.keys(), key="add_vac_comp_select")
                    company_id = options[selected_label]
                    description = st.text_area("Опис вакансії")
                    qualifications = st.text_input("Вимоги до кваліфікації (через кому)", placeholder="Python, SQL, 3+ роки досвіду")
                    submitted = st.form_submit_button("Додати")
                    if submitted:
                        try:
                            new_vacancy = Vacancy(
                                title=title, 
                                description=description, 
                                qualifications=qualifications, 
                                company_id=company_id
                            )
                            vacancy_service.add(new_vacancy)
                            st.success(f"Додано вакансію: {new_vacancy.title}")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку компаній: {e}")

    with tabs[2]:
        st.subheader("Редагування вакансії")
        try:
            vacancies = vacancy_service.get_all()
            options = get_selection_options(vacancies, 'title', None)
            
            if not options:
                st.warning("Немає вакансій для редагування.")
            else:
                selected_label = st.selectbox("Оберіть вакансію:", options.keys(), key="edit_vac_select")
                selected_id = options[selected_label]
                vacancy = vacancy_service.get_by_id(selected_id)
                
                with st.form("edit_vacancy_form"):
                    title = st.text_input("Назва", value=vacancy.title)
                    description = st.text_area("Опис", value=vacancy.description)
                    qualifications = st.text_input("Вимоги до кваліфікації", value=vacancy.qualifications)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            vacancy.title = title
                            vacancy.description = description
                            vacancy.qualifications = qualifications
                            vacancy_service.update(vacancy)
                            st.success(f"Вакансію '{title}' оновлено.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")
            
    with tabs[3]:
        st.subheader("Видалення вакансії")
        try:
            vacancies = vacancy_service.get_all()
            options = get_selection_options(vacancies, 'title', None)
            
            if not options:
                st.warning("Немає вакансій для видалення.")
            else:
                selected_label = st.selectbox("Оберіть вакансію для видалення:", options.keys(), key="del_vac_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        vacancy_id = options[selected_label]
                        vacancy_service.delete(vacancy_id)
                        st.success(f"Вакансію {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")