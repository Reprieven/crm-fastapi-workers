import os
from typing import Dict

class SQLLoader:
    
    @classmethod
    def load_sql(cls, file_path: str) -> str:
        base_dir = os.path.join(os.path.dirname(__file__), 'sql')
        full_path = os.path.join(base_dir, file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"SQL файл не найден: {full_path}")
        except Exception as e:
            raise Exception(f"Ошибка загрузки SQL файла {file_path}: {e}")
    