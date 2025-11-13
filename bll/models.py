from dataclasses import dataclass, field
from uuid import uuid4

def get_new_id():
    return str(uuid4())

@dataclass
class Unemployed:
    id: str = field(default_factory=get_new_id)
    name: str = ""
    surname: str = ""

@dataclass
class Company:
    id: str = field(default_factory=get_new_id)
    name: str = ""

@dataclass
class Category:
    id: str = field(default_factory=get_new_id)
    name: str = ""

@dataclass
class Vacancy:
    id: str = field(default_factory=get_new_id)
    title: str = ""
    description: str = ""
    category_id: str = ""

@dataclass
class Resume:
    id: str = field(default_factory=get_new_id)
    title: str = "" 
    unemployed_id: str = ""
    category_id: str = ""
    skills_description: str = ""