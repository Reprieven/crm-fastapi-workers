from dotenv import load_dotenv
import os
from abc import ABC, abstractmethod

load_dotenv()

class DatabaseConfigInterface(ABC):
    @abstractmethod
    def get_connection_params(self) -> dict:
        pass

class DataBaseConfig(DatabaseConfigInterface):
    def __init__(self, db_name=None):
        self.db_name = db_name or os.getenv('DB_NAME', 'mydb')
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', '')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
    
    def get_connection_params(self) -> dict:
        return {
            'database': self.db_name,
            'user': self.db_user,
            'password': self.db_password,
            'host': self.db_host,
            'port': self.db_port
        }
    
    @classmethod
    def for_postgres(cls):
        return cls('postgres')