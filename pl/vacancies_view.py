import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from pl.utils import get_selection_options

def show_vacancies_page(service):
    st.header("📄 Управління вакансіями")
    
    tabs = st.tabs(["Перегляд та пошук", "Додати нову", "Редагувати", "Видалити"])
    
    with tabs[0]:
        st.subheader("Список вакансій")
        
        sort_key_vac = st.selectbox("Сортувати за:", options=[("Назвою", "title")], format_func=lambda x: x[0], key="vac_sort")
        
        try:
            vacancies = service.get_all_vacancies(sort_by=sort_key_vac[1])
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
                results_vac = service.find_vacancies_by_keyword(keyword_vac)
                if results_vac:
                    st.dataframe(results_vac, use_container_width=True, hide_index=True)
                else:
                    st.warning("Нічого не знайдено.")
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")
                
    with tabs[1]:
        st.subheader("Додавання вакансії")
        with st.form("add_vacancy_form"):
            title = st.text_input("Назва вакансії (напр., 'Розробник Python')")
            description = st.text_area("Опис вакансії")
            qualifications = st.text_input("Вимоги до кваліфікації (через кому)", placeholder="Python, SQL, 3+ роки досвіду")
            submitted = st.form_submit_button("Додати")
            if submitted:
                try:
                    vacancy = service.add_vacancy(title, description, qualifications)
                    st.success(f"Додано вакансію: {vacancy.title}")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")

    with tabs[2]:
        st.subheader("Редагування вакансії")
        try:
            vacancies = service.get_all_vacancies(sort_by="title")
            options = get_selection_options(vacancies, 'title', None)
            
            if not options:
                st.warning("Немає вакансій для редагування.")
            else:
                selected_label = st.selectbox("Оберіть вакансію:", options.keys(), key="edit_vac_select")
                selected_id = options[selected_label]
                vacancy = service.get_vacancy_by_id(selected_id)
                
                with st.form("edit_vacancy_form"):
                    st.text(f"ID: {vacancy.id}")
                    new_title = st.text_input("Назва", value=vacancy.title)
                    new_desc = st.text_area("Опис", value=vacancy.description)
                    new_qualifications = st.text_input("Вимоги до кваліфікації", value=vacancy.qualifications)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            service.update_vacancy(vacancy.id, new_title, new_desc, new_qualifications)
                            st.success(f"Вакансію '{new_title}' оновлено.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")
            
    with tabs[3]:
        st.subheader("Видалення вакансії")
        try:
            vacancies = service.get_all_vacancies(sort_by="title")
            options = get_selection_options(vacancies, 'title', None)
            
            if not options:
                st.warning("Немає вакансій для видалення.")
            else:
                selected_label = st.selectbox("Оберіть вакансію для видалення:", options.keys(), key="del_vac_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        vacancy_id = options[selected_label]
                        service.delete_vacancy(vacancy_id)
                        st.success(f"Вакансію {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")