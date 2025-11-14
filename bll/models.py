from dataclasses import dataclass, field
from uuid import uuid4

def get_new_id():
    return str(uuid4())

@dataclass
class BaseModel:
    id: str = field(default_factory=get_new_id)

@dataclass
class Person(BaseModel):
    name: str = ""
    surname: str = ""

@dataclass
class Unemployed(Person):
    qualifications: str = ""

@dataclass
class Company(BaseModel):
    name: str = ""

@dataclass
class Document(BaseModel):
    title: str = ""
    qualifications: str = ""

@dataclass
class Vacancy(Document):
    company_id: str = ""
    description: str = ""

@dataclass
class Resume(Document):
    unemployed_id: str = ""
    skills_description: str = ""