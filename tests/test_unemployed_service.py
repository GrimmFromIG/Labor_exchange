import pytest
from unittest.mock import MagicMock
from bll.models import Unemployed
from bll.exceptions import EntityNotFoundException, ValidationException

# --- UnemployedService Tests (100% Coverage) ---

def test_unemployed_add_success(unemployed_service, mock_repo):
    # Arrange (Triple A)
    new_person = Unemployed(name="Іван", surname="Петренко", qualifications="Python")
    
    # Act
    unemployed_service.add(new_person)
    
    # Assert
    mock_repo.add.assert_called_once()
    added_data = mock_repo.add.call_args[0][1]
    assert added_data['name'] == "Іван"
    assert added_data['qualifications'] == "Python"

def test_unemployed_get_all(unemployed_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Іван", "surname": "А", "qualifications": "Python"},
        {"id": "2", "name": "Марія", "surname": "Б", "qualifications": "Java"}
    ]
    
    # Act
    persons = unemployed_service.get_all()
    
    # Assert
    assert len(persons) == 2
    assert persons[0].name == "Іван"
    assert isinstance(persons[1], Unemployed)

def test_unemployed_get_by_id(unemployed_service, mock_repo):
    # Arrange
    mock_repo.get_by_id.return_value = {"id": "1", "name": "Іван", "surname": "А", "qualifications": "Python"}
    
    # Act
    person = unemployed_service.get_by_id("1")
    
    # Assert
    assert person.name == "Іван"
    assert person.id == "1"

def test_unemployed_get_by_id_not_found(unemployed_service, mock_repo):
    # Arrange
    mock_repo.get_by_id.side_effect = FileNotFoundError
    
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        unemployed_service.get_by_id("invalid_id")

def test_unemployed_update(unemployed_service, mock_repo):
    # Arrange
    person = Unemployed(id="1", name="Іван", surname="Петренко", qualifications="Python")
    
    # Act
    person.name = "Іван Оновлений"
    unemployed_service.update(person)
    
    # Assert
    mock_repo.update.assert_called_once()
    updated_data = mock_repo.update.call_args[0][1]
    assert updated_data['name'] == "Іван Оновлений"

def test_unemployed_delete(unemployed_service, mock_repo):
    # Arrange
    person_id = "1"
    
    # Act
    unemployed_service.delete(person_id)
    
    # Assert
    mock_repo.delete.assert_called_with("unemployed", "1")

def test_unemployed_find_by_keyword(unemployed_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Іван", "surname": "Петренко", "qualifications": ""},
        {"id": "2", "name": "Петро", "surname": "Іваненко", "qualifications": ""}
    ]
    
    # Act
    results = unemployed_service.find_by_keyword("петро")
    
    # Assert
    assert len(results) == 1
    assert results[0].name == "Петро"

def test_unemployed_find_by_qualification(unemployed_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Іван", "surname": "А", "qualifications": "Python, SQL"},
        {"id": "2", "name": "Марія", "surname": "Б", "qualifications": "Java, SQL"}
    ]
    
    # Act
    results = unemployed_service.find_by_qualification("python")
    
    # Assert
    assert len(results) == 1
    assert results[0].name == "Іван"

def test_unemployed_get_statistics(unemployed_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Іван", "surname": "А", "qualifications": "Python, SQL"},
        {"id": "2", "name": "Марія", "surname": "Б", "qualifications": "Java, SQL"},
        {"id": "3", "name": "Петро", "surname": "В", "qualifications": "Python, JavaScript"}
    ]
    
    # Act
    stats = unemployed_service.get_statistics()
    
    # Assert
    assert stats["total_unemployed"] == 3
    assert stats["top_qualification"] in ["python", "sql"]