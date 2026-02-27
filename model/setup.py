from .connection import create_connection
import psycopg2
from .config import DatabaseConfigInterface, DataBaseConfig
from typing import List
from .isetup import DatabaseCreator, TableCreator, ViewCreator, FunctionCreator
from .sql_loader import SQLLoader

class PostgresDatabaseCreator(DatabaseCreator):
    def create(self, config: DatabaseConfigInterface) -> None:
        postgres_config = DataBaseConfig.for_postgres()
        try:
            with create_connection(postgres_config) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", 
                        (config.db_name,)
                    )
                    if not cursor.fetchone():
                        cursor.execute(f"CREATE DATABASE {config.db_name}")
                        print('База данных создана')
                    else:
                        print('База данных уже существует')
        except psycopg2.Error as e:
            raise RuntimeError(f"Ошибка создания БД: {e}")

class DepartmentsTableCreator(TableCreator):
    def create(self, cursor) -> None:
        query = SQLLoader.load_sql('tables/departments.sql')
        cursor.execute(query)

class PositionsTableCreator(TableCreator):
    def create(self, cursor) -> None:
        query = SQLLoader.load_sql('tables/positions.sql')
        cursor.execute(query)

class ScheduleTableCreator(TableCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('tables/schedule.sql')
        cursor.execute(query)

class EmployeeTableCreator(TableCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('tables/employees.sql')
        cursor.execute(query)

class WorkHistoryTableCreator(TableCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('tables/workhistory.sql')
        cursor.execute(query)

class DepartmentView(ViewCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('view/department_view.sql')
        cursor.execute(query)

class AgeFunction(FunctionCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('func/age_function.sql')
        cursor.execute(query)

class EmployeeFunction(FunctionCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('func/employee_function.sql')
        cursor.execute(query)

class CheckGradeFunction(FunctionCreator):
    def create(self, cursor)->None:
        query = SQLLoader.load_sql('func/check_grade_function.sql')
        cursor.execute(query)
        
class DeleteById(FunctionCreator):
    def create(self, cursor):
        query = SQLLoader.load_sql('procedures/delete_by_id.sql')
        cursor.execute(query)
        
class DatabaseSetup:
    def __init__(
        self, 
        config: DatabaseConfigInterface,
        db_creator: DatabaseCreator = None,
        table_creators: List[TableCreator] = None,
        view_creators: List[ViewCreator] = None,
        func_creators: List[FunctionCreator] = None
    ):
        self.config = config
        self.db_creator = db_creator or PostgresDatabaseCreator()
        self.table_creators = table_creators 
        self.view_creators = view_creators 
        self.func_creators = func_creators

    def create_db(self) -> None:
        self.db_creator.create(self.config)

    def create_tables(self) -> None:
        try:
            with create_connection(self.config) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    for creator in self.table_creators:
                        creator.create(cursor)
                print('Все таблицы успешно созданы')
        except psycopg2.Error as e:
            print(f'Ошибка создания таблиц: {e}')
            raise

    def create_views(self)->None:
        try:
            with create_connection(self.config) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    for creator in self.view_creators:
                        creator.create(cursor)
                print('Все представления успешно созданы')
        except psycopg2.Error as e:
            print(f'Ошибка создания представлений: {e}')
            raise

    def create_functions(self)->None:
        try:
            with create_connection(self.config) as conn:
                conn.autocommit = True
                with conn.cursor() as cursor:
                    for creator in self.func_creators:
                        creator.create(cursor)
                print('Все функции успешно созданы')
        except psycopg2.Error as e:
            print(f'Ошибка создания функции: {e}')
            raise