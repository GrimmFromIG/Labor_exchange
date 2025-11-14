import pytest
from unittest.mock import MagicMock
from dal.repository import IRepository
from bll.models import Unemployed, Resume, Vacancy
from bll.unemployed_service import UnemployedService
from bll.resume_service import ResumeService
from bll.vacancy_service import VacancyService

@pytest.fixture
def mock_repo():
    return MagicMock(spec=IRepository)

@pytest.fixture
def unemployed_service(mock_repo):
    return UnemployedService(mock_repo)

@pytest.fixture
def resume_service(mock_repo, unemployed_service):
    return ResumeService(mock_repo, unemployed_service)

@pytest.fixture
def vacancy_service(mock_repo):
    return VacancyService(mock_repo)

def test_get_unemployed_statistics(unemployed_service, mock_repo):
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Іван", "surname": "А", "qualifications": "Python, SQL"},
        {"id": "2", "name": "Марія", "surname": "Б", "qualifications": "Java, SQL"},
        {"id": "3", "name": "Петро", "surname": "В", "qualifications": "Python, JavaScript"}
    ]
    
    stats = unemployed_service.get_statistics()
    
    assert stats["total_unemployed"] == 3
    assert stats["top_qualification"] in ["python", "sql"]

def test_resume_inherits_qualifications_on_add(resume_service, unemployed_service, mock_repo):
    person = Unemployed(id="1", name="Анна", surname="К", qualifications="Project Management, Agile")
    
    mock_repo.get_by_id.return_value = {"id": "1", "name": "Анна", "surname": "К", "qualifications": "Project Management, Agile"}
    
    new_resume = Resume(title="Project Manager", unemployed_id="1", skills_description="Додаткові навички...")
    
    resume_service.add(new_resume)
    
    assert new_resume.qualifications == "Project Management, Agile"
    
    args, kwargs = mock_repo.add.call_args
    added_data = args[1]
    assert added_data['qualifications'] == "Project Management, Agile"

def test_vacancy_matching(vacancy_service):
    resume = Resume(qualifications="Python, SQL, Git")
    
    vacancies_data = [
        {"id": "v1", "title": "Python Dev", "qualifications": "Python, SQL, Git", "description": "", "company_id": "c1"},
        {"id": "v2", "title": "Data Analyst", "qualifications": "SQL, Python, Pandas", "description": "", "company_id": "c1"},
        {"id": "v3", "title": "Frontend Dev", "qualifications": "JavaScript, React", "description": "", "company_id": "c2"},
        {"id": "v4", "title": "Python Junior", "qualifications": "Python", "description": "", "company_id": "c3"},
    ]
    
    vacancy_service.get_all = MagicMock(return_value=[Vacancy(**data) for data in vacancies_data])
    
    matches = vacancy_service.find_matches_for_resume(resume)
    
    assert len(matches) == 3
    assert matches[0]["vacancy"].title == "Python Dev"
    assert matches[0]["score"] == 1.0
    
    assert matches[1]["vacancy"].title == "Data Analyst"
    assert matches[1]["score"] == (2/3)
    
    assert matches[2]["vacancy"].title == "Python Junior"
    assert matches[2]["score"] == (1/3)