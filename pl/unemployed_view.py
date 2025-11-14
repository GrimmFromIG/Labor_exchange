import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from bll.models import Unemployed
from pl.utils import get_selection_options

def show_unemployed_page(unemployed_service, resume_service):
    st.header("👤 Управління безробітними")
    
    tabs = st.tabs([
        "Перегляд та пошук", 
        "Додати нового", 
        "Редагувати", 
        "Видалити",
        "Резюме безробітного"
    ])

    with tabs[0]:
        st.subheader("Список безробітних")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            sort_key = st.selectbox(
                "Сортувати за:",
                options=[("Прізвищем", "surname"), ("Ім'ям", "name")],
                format_func=lambda x: x[0],
                key="unemployed_sort"
            )
            try:
                unemployed_list = unemployed_service.get_all()
                if sort_key[1] == "surname":
                    unemployed_list.sort(key=lambda x: x.surname)
                else:
                    unemployed_list.sort(key=lambda x: x.name)
                
                st.info(f"Знайдено: {len(unemployed_list)} осіб(а).")
            except Exception as e:
                st.error(f"Помилка завантаження даних: {e}")
                unemployed_list = []
        with col2:
            if unemployed_list:
                st.dataframe(unemployed_list, use_container_width=True, hide_index=True)
            else:
                st.info("Список безробітних порожній.") 

        st.subheader("Пошук за ім'ям/прізвищем")
        keyword = st.text_input("Введіть ім'я або прізвище для пошуку:")
        if keyword:
            try:
                results = unemployed_service.find_by_keyword(keyword)
                st.dataframe(results, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")
        
        st.subheader("Пошук за кваліфікацією")
        keyword_qual = st.text_input("Введіть ключове слово з кваліфікації:")
        if keyword_qual:
            try:
                results_qual = unemployed_service.find_by_qualification(keyword_qual)
                st.dataframe(results_qual, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")

    with tabs[1]:
        st.subheader("Додавання безробітного")
        with st.form("add_unemployed_form"):
            name = st.text_input("Ім'я")
            surname = st.text_input("Прізвище")
            qualifications = st.text_input("Кваліфікації (через кому)", placeholder="Python, SQL, Аналіз даних")
            submitted = st.form_submit_button("Додати")
            if submitted:
                try:
                    new_person = Unemployed(name=name, surname=surname, qualifications=qualifications)
                    unemployed_service.add(new_person)
                    st.success(f"Додано: {new_person.name} {new_person.surname}")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")
    
    with tabs[2]:
        st.subheader("Редагування даних")
        try:
            unemployed_list = unemployed_service.get_all()
            options = get_selection_options(unemployed_list, 'name', 'surname')
            
            if not options:
                st.warning("Немає безробітних для редагування.")
            else:
                selected_label = st.selectbox("Оберіть безробітного:", options.keys(), key="edit_unemployed_select")
                selected_id = options[selected_label]
                person = unemployed_service.get_by_id(selected_id)
                
                with st.form("edit_unemployed_form"):
                    name = st.text_input("Ім'я", value=person.name)
                    surname = st.text_input("Прізвище", value=person.surname)
                    qualifications = st.text_input("Кваліфікації", value=person.qualifications)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            person.name = name
                            person.surname = surname
                            person.qualifications = qualifications
                            unemployed_service.update(person)
                            st.success(f"Дані {name} {surname} оновлено.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

    with tabs[3]:
        st.subheader("Видалення безробітного")
        try:
            unemployed_list = unemployed_service.get_all()
            options = get_selection_options(unemployed_list, 'name', 'surname')
            
            if not options:
                st.warning("Немає безробітних для видалення.")
            else:
                selected_label = st.selectbox("Оберіть безробітного для видалення:", options.keys(), key="del_unemployed_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        person_id = options[selected_label]
                        unemployed_service.delete(person_id)
                        st.success(f"Безробітного {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

    with tabs[4]:
        st.subheader("Перегляд резюме безробітного")
        try:
            unemployed_list = unemployed_service.get_all()
            options = get_selection_options(unemployed_list, 'name', 'surname')
            
            if not options:
                st.warning("Немає безробітних для перегляду.")
            else:
                selected_label = st.selectbox("Оберіть безробітного:", options.keys(), key="view_resumes_select")
                selected_id = options[selected_label]
                
                resumes = resume_service.get_resumes_for_unemployed(selected_id)
                if resumes:
                    st.write(f"Резюме для {selected_label}:")
                    st.dataframe(resumes, use_container_width=True, hide_index=True)
                else:
                    st.info(f"У {selected_label} ще немає резюме.")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")