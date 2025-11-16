import pytest
from unittest.mock import MagicMock
from bll.models import Vacancy, Resume

# --- VacancyService Tests (>= 50% Coverage) ---

def test_vacancy_add_success(vacancy_service, mock_repo):
    # Arrange
    new_vacancy = Vacancy(title="Python Dev", company_id="c1", qualifications="Python")
    
    # Act
    vacancy_service.add(new_vacancy)
    
    # Assert
    mock_repo.add.assert_called_once()
    added_data = mock_repo.add.call_args[0][1]
    assert added_data['title'] == "Python Dev"

def test_vacancy_get_for_company(vacancy_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "v1", "title": "Dev 1", "company_id": "c1", "qualifications": "", "description": ""},
        {"id": "v2", "title": "Dev 2", "company_id": "c2", "qualifications": "", "description": ""},
        {"id": "v3", "title": "Dev 3", "company_id": "c1", "qualifications": "", "description": ""}
    ]
    
    # Act
    results = vacancy_service.get_vacancies_for_company("c1")
    
    # Assert
    assert len(results) == 2
    assert results[0].title == "Dev 1"
    assert results[1].title == "Dev 3"

def test_vacancy_matching(vacancy_service, mock_repo):
    # Arrange
    resume = Resume(qualifications="Python, SQL, Git")
    vacancies_data = [
        {"id": "v1", "title": "Python Dev", "qualifications": "Python, SQL, Git", "description": "", "company_id": "c1"},
        {"id": "v2", "title": "Data Analyst", "qualifications": "SQL, Python, Pandas", "description": "", "company_id": "c1"},
        {"id": "v3", "title": "Frontend Dev", "qualifications": "JavaScript, React", "description": "", "company_id": "c2"},
    ]
    vacancy_service.get_all = MagicMock(return_value=[Vacancy(**data) for data in vacancies_data])
    
    # Act
    matches = vacancy_service.find_matches_for_resume(resume)
    
    # Assert
    assert len(matches) == 2
    assert matches[0]["vacancy"].title == "Python Dev"
    assert matches[0]["score"] == 1.0
    assert matches[1]["vacancy"].title == "Data Analyst"
    assert matches[1]["score"] == (2/3)