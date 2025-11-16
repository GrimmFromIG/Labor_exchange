import streamlit as st

def show_statistics_page(unemployed_service):
    st.header("📊 Статистика")

    try:
        stats = unemployed_service.get_statistics()
        
        col1, col2 = st.columns(2)
        col1.metric("Загальна кількість безробітних", stats["total_unemployed"])
        col2.metric("Найпопулярніша кваліфікація", stats["top_qualification"])
        
    except Exception as e:
        st.error(f"Помилка при розрахунку статистики: {e}")