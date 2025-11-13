
import json
import os
from typing import List, Dict, Any

class JsonRepository:
    def __init__(self, filepath: str = 'dal/data.json'):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
        if not os.path.exists(self.filepath):
            initial_data = {
                "categories": [],
                "vacancies": [],
                "resumes": [],
                "unemployed": [],
                "companies": []
            }
            self.save_all_data(initial_data)

    def load_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {
                "categories": [], "vacancies": [], "resumes": [], 
                "unemployed": [], "companies": []
            }

    def save_all_data(self, data: Dict[str, List[Dict[str, Any]]]):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Помилка збереження файлу: {e}")