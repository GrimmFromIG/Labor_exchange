import streamlit as st
from pl.utils import get_selection_options

def show_matching_page(resume_service, vacancy_service, company_service):
    st.header("🤖 Підбір вакансій та резюме")

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
