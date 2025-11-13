
import pytest
from unittest.mock import MagicMock, patch

from bll.services import LaborExchangeService
from bll.exceptions import ValidationException, EntityNotFoundException
from bll.models import Unemployed

@pytest.fixture
def mock_repo():
    mock = MagicMock()
    
    mock.db = {
        "unemployed": [],
        "companies": [],
        "vacancies": [],
        "resumes": [],
        "categories": []
    }
    
    def load_data():
        return mock.db
        
    def save_data(data):
        mock.db = data
        
    mock.load_all_data.side_effect = load_data
    mock.save_all_data.side_effect = save_data
    
    return mock

@pytest.fixture
def service(mock_repo):
    return LaborExchangeService(repository=mock_repo)

def test_add_unemployed_success(service: LaborExchangeService):
    name = "Іван"
    surname = "Петренко"
    
    person = service.add_unemployed(name, surname)
    
    assert person.name == name
    assert person.surname == surname
    assert len(service.get_all_unemployed()) == 1
    assert service.get_all_unemployed()[0].name == "Іван"

def test_add_unemployed_validation_error(service: LaborExchangeService):
    with pytest.raises(ValidationException) as exc_info:
        service.add_unemployed(name="", surname="Сидоренко")
    
    assert "Ім'я та прізвище не можуть бути порожніми" in str(exc_info.value)
    
    assert len(service.get_all_unemployed()) == 0

def test_get_all_unemployed_sorting(service: LaborExchangeService):
    service.add_unemployed("Марія", "Василенко") 
    service.add_unemployed("Петро", "Авраменко") 
    
    sorted_list = service.get_all_unemployed(sort_by="surname")
    
    assert len(sorted_list) == 2
    assert sorted_list[0].surname == "Авраменко"
    assert sorted_list[1].surname == "Василенко"

def test_find_unemployed_by_keyword(service: LaborExchangeService):
    service.add_unemployed("Іван", "Петренко")
    service.add_unemployed("Петро", "Іваненко")
    
    results = service.find_unemployed_by_keyword("іван")
    
    assert len(results) == 2 
    
    results_petro = service.find_unemployed_by_keyword("петро")
    assert len(results_petro) == 1
    assert results_petro[0].name == "Петро"

def test_delete_unemployed(service: LaborExchangeService):
    person = service.add_unemployed("Олег", "Скрипка")
    person_id = person.id
    assert len(service.get_all_unemployed()) == 1
    
    service.delete_unemployed(person_id)
    
    assert len(service.get_all_unemployed()) == 0

def test_delete_unemployed_not_found(service: LaborExchangeService):
    service.add_unemployed("Олег", "Скрипка")
    
    with pytest.raises(EntityNotFoundException):
        service.delete_unemployed("неіснуючий-id")