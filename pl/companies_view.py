import streamlit as st
from bll.exceptions import ValidationException, EntityNotFoundException
from pl.utils import get_selection_options

def show_companies_page(service):
    st.header("🏢 Управління фірмами-замовниками")
    
    tabs = st.tabs(["Перегляд", "Додати нову", "Редагувати", "Видалити"])

    with tabs[0]:
        st.subheader("Список фірм")
        try:
            companies = service.get_all_companies(sort_by="name")
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
                    company = service.add_company(name)
                    st.success(f"Додано: {company.name} (ID: {company.id})")
                except ValidationException as e:
                    st.error(f"Помилка валідації: {e}")
                except Exception as e:
                    st.error(f"Сталася помилка: {e}")
    
    with tabs[2]:
        st.subheader("Редагування даних")
        try:
            companies = service.get_all_companies(sort_by="name")
            options = get_selection_options(companies, 'name', None)
            
            if not options:
                st.warning("Немає фірм для редагування.")
            else:
                selected_label = st.selectbox("Оберіть фірму:", options.keys(), key="edit_comp_select")
                selected_id = options[selected_label]
                company = service.get_company_by_id(selected_id)
                
                with st.form("edit_company_form"):
                    st.text(f"ID: {company.id}")
                    new_name = st.text_input("Назва", value=company.name)
                    submitted = st.form_submit_button("Оновити")
                    
                    if submitted:
                        try:
                            service.update_company(company.id, new_name)
                            st.success(f"Назву фірми оновлено на {new_name}.")
                        except ValidationException as e:
                            st.error(f"Помилка валідації: {e}")
                        except Exception as e:
                            st.error(f"Сталася помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")
            
    with tabs[3]:
        st.subheader("Видалення фірми")
        try:
            companies = service.get_all_companies(sort_by="name")
            options = get_selection_options(companies, 'name', None)
            
            if not options:
                st.warning("Немає фірм для видалення.")
            else:
                selected_label = st.selectbox("Оберіть фірму для видалення:", options.keys(), key="del_comp_select")
                
                if st.button("Видалити", type="primary"):
                    try:
                        company_id = options[selected_label]
                        service.delete_company(company_id)
                        st.success(f"Фірму {selected_label} видалено.")
                        st.rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")