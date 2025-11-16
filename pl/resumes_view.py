import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from bll.models import Resume
from pl.utils import get_selection_options

def show_resumes_page(resume_service, unemployed_service):
    st.header("📑 Управління резюме")
    
    tabs = st.tabs(["Перегляд", "Додати нове", "Редагувати", "Видалити"])

    with tabs[0]:
        st.subheader("Список резюме")
        try:
            resumes = resume_service.get_all()
            resumes.sort(key=lambda x: x.title)
            if resumes:
                st.dataframe(resumes, use_container_width=True, hide_index=True)
            else:
                st.info("Список резюме порожній.")
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")

    with tabs[1]:
        st.subheader("Додавання резюме")
        try:
            unemployed_list = unemployed_service.get_all()
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
                            new_resume = Resume(
                                title=title, 
                                unemployed_id=unemployed_id, 
                                skills_description=skills
                            )
                            resume_service.add(new_resume)
                            st.success(f"Додано резюме: {new_resume.title}. Кваліфікації скопійовано з профілю.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження даних: {e}")

    with tabs[2]:
        st.subheader("Редагування резюме")
        try:
            resumes = resume_service.get_all()
            options = get_selection_options(resumes, 'title', None)
            
            if not options:
                st.warning("Немає резюме для редагування.")
            else:
                selected_label = st.selectbox("Оберіть резюме:", options.keys(), key="edit_res_select")
                selected_id = options[selected_label]
                resume = resume_service.get_by_id(selected_id)
                
                with st.form("edit_resume_form"):
                    st.text(f"Кваліфікації (з профілю): {resume.qualifications}")
                    title = st.text_input("Назва", value=resume.title)
                    skills = st.text_area("Опис навичок", value=resume.skills_description)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            resume.title = title
                            resume.skills_description = skills
                            resume_service.update(resume)
                            st.success(f"Резюме '{title}' оновлено.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")
            
    with tabs[3]:
        st.subheader("Видалення резюме")
        try:
            resumes = resume_service.get_all()
            options = get_selection_options(resumes, 'title', None)
            
            if not options:
                st.warning("Немає резюме для видалення.")
            else:
                selected_label = st.selectbox("Оберіть резюме для видалення:", options.keys(), key="del_res_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        resume_id = options[selected_label]
                        resume_service.delete(resume_id)
                        st.success(f"Резюме {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")