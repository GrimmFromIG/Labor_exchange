import pytest
from unittest.mock import MagicMock
from bll.models import Company

# --- CompanyService Tests (>= 50% Coverage) ---

def test_company_add_success(company_service, mock_repo):
    # Arrange
    new_company = Company(name="TestCorp")
    
    # Act
    company_service.add(new_company)
    
    # Assert
    mock_repo.add.assert_called_once()
    added_data = mock_repo.add.call_args[0][1]
    assert added_data['name'] == "TestCorp"

def test_company_get_all(company_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Alpha"},
        {"id": "2", "name": "Beta"}
    ]
    
    # Act
    companies = company_service.get_all()
    
    # Assert
    assert len(companies) == 2
    assert companies[0].name == "Alpha"

def test_company_update(company_service, mock_repo):
    # Arrange
    company = Company(id="1", name="Alpha")
    
    # Act
    company.name = "AlphaUpdated"
    company_service.update(company)
    
    # Assert
    mock_repo.update.assert_called_once()
    updated_data = mock_repo.update.call_args[0][1]
    assert updated_data['name'] == "AlphaUpdated"

def test_company_find_by_name(company_service, mock_repo):
    # Arrange
    mock_repo.get_all.return_value = [
        {"id": "1", "name": "Alpha Inc"},
        {"id": "2", "name": "Beta LLC"}
    ]
    
    # Act
    results = company_service.find_by_name("alpha")
    
    # Assert
    assert len(results) == 1
    assert results[0].name == "Alpha Inc"