import pytest
from unittest.mock import MagicMock
from bll.models import Unemployed, Resume
from bll.exceptions import ValidationException

# --- ResumeService Tests (>= 50% Coverage) ---

def test_resume_add_polymorphism(resume_service, unemployed_service, mock_repo):
    # Arrange (Polymorphism test)
    person = Unemployed(id="1", name="Анна", surname="К", qualifications="Project Management, Agile")
    mock_repo.get_by_id.return_value = {"id": "1", "name": "Анна", "surname": "К", "qualifications": "Project Management, Agile"}
    unemployed_service.get_by_id = MagicMock(return_value=person)
    
    new_resume = Resume(title="Project Manager", unemployed_id="1", skills_description="Додаткові навички...")
    
    # Act
    resume_service.add(new_resume)
    
    # Assert
    assert new_resume.qualifications == "Project Management, Agile"
    mock_repo.add.assert_called_once()
    added_data = mock_repo.add.call_args[0][1]
    assert added_data['qualifications'] == "Project Management, Agile"

def test_resume_add_validation_error(resume_service):
    # Arrange
    invalid_resume = Resume(title="", unemployed_id="1")
    
    # Act & Assert
    with pytest.raises(ValidationException):
        resume_service.add(invalid_resume)

def test_resume_get_for_unemployed(resume_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "r1", "title": "Dev 1", "unemployed_id": "p1", "qualifications": "", "skills_description": ""},
        {"id": "r2", "title": "Dev 2", "unemployed_id": "p2", "qualifications": "", "skills_description": ""},
        {"id": "r3", "title": "Dev 3", "unemployed_id": "p1", "qualifications": "", "skills_description": ""}
    ]
    
    # Act
    results = resume_service.get_resumes_for_unemployed("p1")
    
    # Assert
    assert len(results) == 2
    assert results[0].title == "Dev 1"
    assert results[1].title == "Dev 3"