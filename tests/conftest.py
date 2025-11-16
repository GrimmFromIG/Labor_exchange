import pytest
from unittest.mock import MagicMock
from dal.repository import IRepository
from bll.unemployed_service import UnemployedService
from bll.company_service import CompanyService
from bll.vacancy_service import VacancyService
from bll.resume_service import ResumeService

@pytest.fixture
def mock_repo():
    return MagicMock(spec=IRepository)

@pytest.fixture
def unemployed_service(mock_repo):
    return UnemployedService(mock_repo)

@pytest.fixture
def company_service(mock_repo):
    return CompanyService(mock_repo)

@pytest.fixture
def vacancy_service(mock_repo):
    return VacancyService(mock_repo)

@pytest.fixture
def resume_service(mock_repo, unemployed_service):
    return ResumeService(mock_repo, unemployed_service)