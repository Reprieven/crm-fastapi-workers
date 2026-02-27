from .connection import create_connection
import psycopg2
from .config import DatabaseConfigInterface
from .iqueries import QueryInterface
from .sql_loader import SQLLoader
class DepartmentQuery(QueryInterface):
    def execute(self, config: DatabaseConfigInterface, department_id: int):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('queries/department_query.sql')
                with conn.cursor() as cursor:
                    cursor.execute(query, (department_id,))
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class EmployeeQuery(QueryInterface):
    def execute(self, config: DatabaseConfigInterface, date: str):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('queries/employee_query.sql')
                with conn.cursor() as cursor:
                    cursor.execute(query, (date,))
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class EmployeeAgeCheckQuery(QueryInterface):
    def execute(self, config: DatabaseConfigInterface, age: int, pos_id: int):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True

                query = SQLLoader.load_sql('queries/employee_age_check_query.sql')
                
                with conn.cursor() as cursor:
                    cursor.execute(query, (age, pos_id))
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise
