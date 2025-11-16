from typing import TypeVar, Generic, List, Type
from dataclasses import asdict, is_dataclass
from dal.repository import IRepository
from bll.models import BaseModel

T = TypeVar('T', bound=BaseModel)

class GenericService(Generic[T]):
    def __init__(self, repository: IRepository, collection: str, model_type: Type[T]):
        self._repository = repository
        self._collection = collection
        self._model_type = model_type

    def get_all(self) -> List[T]:
        all_data = self._repository.get_all(self._collection)
        return [self._model_type(**data) for data in all_data]

    def get_by_id(self, id: str) -> T:
        data = self._repository.get_by_id(self._collection, id)
        return self._model_type(**data)

    def add(self, entity: T) -> T:
        if not is_dataclass(entity):
            raise TypeError("Entity must be a dataclass instance.")
        self._repository.add(self._collection, asdict(entity))
        return entity

    def update(self, entity: T) -> T:
        if not is_dataclass(entity):
            raise TypeError("Entity must be a dataclass instance.")
        self._repository.update(self._collection, asdict(entity))
        return entity

    def delete(self, id: str) -> None:
        self._repository.delete(self._collection, id)