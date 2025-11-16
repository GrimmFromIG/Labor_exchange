import json
import os
from typing import List, Dict, Any, Protocol
from abc import ABC, abstractmethod

class IRepository(Protocol):
    @abstractmethod
    def get_all(self, collection: str) -> List[Dict[str, Any]]: ...
        
    @abstractmethod
    def get_by_id(self, collection: str, id: str) -> Dict[str, Any]: ...
        
    @abstractmethod
    def add(self, collection: str, entity: Dict[str, Any]) -> None: ...
        
    @abstractmethod
    def update(self, collection: str, entity: Dict[str, Any]) -> None: ...
        
    @abstractmethod
    def delete(self, collection: str, id: str) -> None: ...

class JsonRepository(IRepository):
    def __init__(self, filepath: str = 'dal/data.json'):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            initial_data = {
                "unemployed": [],
                "companies": [],
                "vacancies": [],
                "resumes": []
            }
            self._save_all(initial_data)

    def _load_all(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {"unemployed": [], "companies": [], "vacancies": [], "resumes": []}

    def _save_all(self, data: Dict[str, List[Dict[str, Any]]]):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Помилка збереження файлу: {e}")

    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        data = self._load_all()
        return data.get(collection, [])

    def get_by_id(self, collection: str, id: str) -> Dict[str, Any]:
        all_items = self.get_all(collection)
        for item in all_items:
            if item.get('id') == id:
                return item
        raise FileNotFoundError(f"Об'єкт з ID {id} не знайдено в {collection}")

    def add(self, collection: str, entity: Dict[str, Any]) -> None:
        data = self._load_all()
        if collection not in data:
            data[collection] = []
        data[collection].append(entity)
        self._save_all(data)

    def update(self, collection: str, entity: Dict[str, Any]) -> None:
        data = self._load_all()
        item_id = entity.get('id')
        if collection not in data:
            raise KeyError(f"Колекція {collection} не існує")
            
        index_to_update = -1
        for i, item in enumerate(data[collection]):
            if item.get('id') == item_id:
                index_to_update = i
                break
                
        if index_to_update == -1:
            raise FileNotFoundError(f"Об'єкт з ID {item_id} не знайдено для оновлення")
            
        data[collection][index_to_update] = entity
        self._save_all(data)

    def delete(self, collection: str, id: str) -> None:
        data = self._load_all()
        if collection not in data:
            raise KeyError(f"Колекція {collection} не існує")

        index_to_delete = -1
        for i, item in enumerate(data[collection]):
            if item.get('id') == id:
                index_to_delete = i
                break
                
        if index_to_delete == -1:
            raise FileNotFoundError(f"Об'єкт з ID {id} не знайдено для видалення")
            
        data[collection].pop(index_to_delete)
        self._save_all(data)