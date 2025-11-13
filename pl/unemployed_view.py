import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from pl.utils import get_selection_options

def show_unemployed_page(service):
    st.header("👤 Управління безробітними")
    
    tabs = st.tabs(["Перегляд та пошук", "Додати нового", "Редагувати", "Видалити"])

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
                unemployed_list = service.get_all_unemployed(sort_by=sort_key[1])
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
                results = service.find_unemployed_by_keyword(keyword)
                if results:
                    st.dataframe(results, use_container_width=True, hide_index=True)
                else:
                    st.warning("Нікого не знайдено.")
            except Exception as e:
                st.error(f"Помилка пошуку: {e}")
        
        st.subheader("Пошук за кваліфікацією")
        keyword_qual = st.text_input("Введіть ключове слово з кваліфікації:")
        if keyword_qual:
            try:
                results_qual = service.find_unemployed_by_qualification(keyword_qual)
                if results_qual:
                    st.dataframe(results_qual, use_container_width=True, hide_index=True)
                else:
                    st.warning("Нікого не знайдено за цією кваліфікацією.")
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
                    person = service.add_unemployed(name, surname, qualifications)
                    st.success(f"Додано: {person.name} {person.surname} (ID: {person.id})")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")
    
    with tabs[2]:
        st.subheader("Редагування даних")
        try:
            unemployed_list = service.get_all_unemployed(sort_by="surname")
            options = get_selection_options(unemployed_list, 'name', 'surname')
            
            if not options:
                st.warning("Немає безробітних для редагування.")
            else:
                selected_label = st.selectbox("Оберіть безробітного:", options.keys(), key="edit_unemployed_select")
                selected_id = options[selected_label]
                person = service.get_unemployed_by_id(selected_id)
                
                with st.form("edit_unemployed_form"):
                    st.text(f"ID: {person.id}")
                    new_name = st.text_input("Ім'я", value=person.name)
                    new_surname = st.text_input("Прізвище", value=person.surname)
                    new_qualifications = st.text_input("Кваліфікації", value=person.qualifications)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            service.update_unemployed(person.id, new_name, new_surname, new_qualifications)
                            st.success(f"Дані {new_name} {new_surname} оновлено.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

    with tabs[3]:
        st.subheader("Видалення безробітного")
        try:
            unemployed_list = service.get_all_unemployed(sort_by="surname")
            options = get_selection_options(unemployed_list, 'name', 'surname')
            
            if not options:
                st.warning("Немає безробітних для видалення.")
            else:
                selected_label = st.selectbox("Оберіть безробітного для видалення:", options.keys(), key="del_unemployed_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        person_id = options[selected_label]
                        service.delete_unemployed(person_id)
                        st.success(f"Безробітного {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")