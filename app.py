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
    ["Безробітні", "Фірми-замовники", "Вакансії", "Резюме"]
)

def get_selection_options(entity_list, name_attr='name', surname_attr='surname'):
    options = {}
    for item in entity_list:
        if hasattr(item, surname_attr) and getattr(item, surname_attr):
            label = f"{getattr(item, surname_attr)} {getattr(item, name_attr)} (ID: {item.id})"
        else:
            label = f"{getattr(item, name_attr)} (ID: {item.id})"
        options[label] = item.id
    return options

if menu_option == "Безробітні":
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
                        st.experimental_rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

elif menu_option == "Фірми-замовники":
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
                        st.experimental_rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

elif menu_option == "Вакансії":
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
        keyword_vac = st.text_input("Введіть ключове слово для пошуку (в назві або описі):")
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
                        st.experimental_rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")

elif menu_option == "Резюме":
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
                        st.experimental_rerun() 
                    except EntityNotFoundException as e:
                        st.error(f"Помилка: {e}")
                    except Exception as e:
                        st.error(f"Непередбачена помилка: {e}")
        except Exception as e:
            st.error(f"Помилка завантаження списку: {e}")