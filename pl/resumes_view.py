import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from pl.utils import get_selection_options

def show_resumes_page(service):
    st.header("📑 Управління резюме")
    
    tabs = st.tabs(["Перегляд", "Додати нове", "Редагувати", "Видалити"])

    with tabs[0]:
        st.subheader("Список резюме")
        sort_key_res = st.selectbox("Сортувати за:", options=[("Назвою", "title")], format_func=lambda x: x[0], key="res_sort")
        try:
            resumes = service.get_all_resumes(sort_by=sort_key_res[1])
            if resumes:
                st.dataframe(resumes, use_container_width=True, hide_index=True)
            else:
                st.info("Список резюме порожній.")
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")

    with tabs[1]:
        st.subheader("Додавання резюме")
        try:
            unemployed_list = service.get_all_unemployed(sort_by="surname")
            options = get_selection_options(unemployed_list, 'name', 'surname')
            
            if not options:
                st.warning("Спочатку додайте безробітного, щоб створити резюме.")
            else:
                with st.form("add_resume_form"):
                    title = st.text_input("Назва резюме (напр., 'Водій')")
                    selected_label = st.selectbox("Оберіть автора резюме:", options.keys(), key="add_res_select")
                    unemployed_id = options[selected_label]
                    skills = st.text_area("Опис навичок (додатково до кваліфікацій)")
                    submitted = st.form_submit_button("Додати")
                    
                    if submitted:
                        try:
                            resume = service.add_resume(title, unemployed_id, skills)
                            st.success(f"Додано резюме: {resume.title}. Кваліфікації скопійовано з профілю.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")

    with tabs[2]:
        st.subheader("Редагування резюме")
        try:
            resumes = service.get_all_resumes(sort_by="title")
            options = get_selection_options(resumes, 'title', None)
            
            if not options:
                st.warning("Немає резюме для редагування.")
            else:
                selected_label = st.selectbox("Оберіть резюме:", options.keys(), key="edit_res_select")
                selected_id = options[selected_label]
                resume = service.get_resume_by_id(selected_id)
                
                with st.form("edit_resume_form"):
                    st.text(f"ID: {resume.id}")
                    st.text(f"Автор (ID): {resume.unemployed_id}")
                    st.text(f"Кваліфікації (з профілю): {resume.qualifications}")
                    new_title = st.text_input("Назва", value=resume.title)
                    new_skills = st.text_area("Опис навичок", value=resume.skills_description)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            service.update_resume(resume.id, new_title, new_skills)
                            st.success(f"Резюме '{new_title}' оновлено.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")
            
    with tabs[3]:
        st.subheader("Видалення резюме")
        try:
            resumes = service.get_all_resumes(sort_by="title")
            options = get_selection_options(resumes, 'title', None)
            
            if not options:
                st.warning("Немає резюме для видалення.")
            else:
                selected_label = st.selectbox("Оберіть резюме для видалення:", options.keys(), key="del_res_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        resume_id = options[selected_label]
                        service.delete_resume(resume_id)
                        st.success(f"Резюме {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")