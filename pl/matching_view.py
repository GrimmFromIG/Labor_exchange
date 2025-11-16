import streamlit as st
from pl.utils import get_selection_options

def show_matching_page(resume_service, vacancy_service, company_service, unemployed_service):
    st.header("🤖 Підбір вакансій та резюме")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Знайти вакансії для резюме")
        try:
            resumes = resume_service.get_all()
            options = get_selection_options(resumes, 'title', None)
            
            if not options:
                st.warning("Спочатку додайте резюме.")
            else:
                selected_label = st.selectbox("Оберіть резюме:", options.keys(), key="match_resume_select")
                selected_id = options[selected_label]
                resume = resume_service.get_by_id(selected_id)
                
                st.write(f"**Кваліфікації в резюме:** {resume.qualifications or 'N/A'}")
                
                matches = vacancy_service.find_matches_for_resume(resume)
                
                if matches:
                    st.write(f"Знайдено {len(matches)} вакансій:")
                    for match in matches:
                        score_percent = f"{match['score']*100:.0f}%"
                        
                        try:
                            company = company_service.get_by_id(match['vacancy'].company_id)
                            company_name = company.name
                        except Exception:
                            company_name = "Компанію не знайдено"

                        st.info(f"**{match['vacancy'].title}** | {company_name} ({score_percent} збіг)")
                        st.write(f"**Вимоги:** {match['vacancy'].qualifications}")
                        st.divider()
                else:
                    st.info("Відповідних вакансій не знайдено.")
                    
        except Exception as e:
            st.error(f"Помилка завантаження резюме: {e}")

    with col2:
        st.subheader("Знайти резюме для вакансії")
        try:
            vacancies = vacancy_service.get_all()
            options = get_selection_options(vacancies, 'title', None)
            
            if not options:
                st.warning("Спочатку додайте вакансію.")
            else:
                selected_label = st.selectbox("Оберіть вакансію:", options.keys(), key="match_vacancy_select")
                selected_id = options[selected_label]
                vacancy = vacancy_service.get_by_id(selected_id)
                
                st.write(f"**Вимоги вакансії:** {vacancy.qualifications or 'N/A'}")
                
                all_resumes = resume_service.get_all()
                matches = vacancy_service.find_matches_for_vacancy(vacancy, all_resumes)
                
                if matches:
                    st.write(f"Знайдено {len(matches)} резюме:")
                    for match in matches:
                        score_percent = f"{match['score']*100:.0f}%"
                        
                        try:
                            person = unemployed_service.get_by_id(match['resume'].unemployed_id)
                            person_name = f"{person.surname} {person.name}"
                        except Exception:
                            person_name = "Автора не знайдено"

                        st.info(f"**{match['resume'].title}** | {person_name} ({score_percent} збіг)")
                        st.write(f"**Кваліфікації:** {match['resume'].qualifications}")
                        st.divider()
                else:
                    st.info("Відповідних резюме не знайдено.")
                    
        except Exception as e:
            st.error(f"Помилка завантаження вакансій: {e}")
