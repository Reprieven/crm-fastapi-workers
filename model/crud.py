from .connection import create_connection
import psycopg2
from .config import DatabaseConfigInterface
from .sql_loader import SQLLoader
from .queries import QueryInterface
class Insert:
    def insert_record(self, config: DatabaseConfigInterface, table_name: str, values: dict):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                columns = ','.join(values.keys())
                placeholders = ','.join(['%s'] * len(values))
                sql_template = SQLLoader.load_sql('crud/insert.sql')
                query = sql_template.format(
                    table_name=table_name,
                    columns=columns,
                    placeholders=placeholders
                )
                
                with conn.cursor() as cursor:
                    cursor.execute(query, list(values.values()))
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class Delete:
    def delete_record(self, config: DatabaseConfigInterface, table_name: str, record_id: int):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('crud/delete.sql')
                with conn.cursor() as cursor:
                    cursor.execute(query, (table_name,record_id))
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class Update:
    def update_record(self, config: DatabaseConfigInterface, table_name: str, record_id: int, column: str, value):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('crud/update.sql')
                formatted_query = query.format(table_name=table_name, column=column)

                with conn.cursor() as cursor:
                    cursor.execute(formatted_query, (value, record_id))
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class SelectGeneral(QueryInterface):
    def execute(self, config:DatabaseConfigInterface, table_name: str):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('crud/select_general.sql')
                formated_query = query.format(table_name=table_name)

                with conn.cursor() as cursor:
                    cursor.execute(formated_query)
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class SelectId(QueryInterface):
    def execute(self, config:DatabaseConfigInterface, table_name: str, id: int):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('crud/select_id.sql')
                formated_query = query.format(table_name=table_name)

                with conn.cursor() as cursor:
                    cursor.execute(formated_query, (id,))
                    row = cursor.fetchone()
                    if not row:
                        return None
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, row))
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class SelectOffset(QueryInterface):
    def execute(self, config:DatabaseConfigInterface, table_name: str, num: int, start: int):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('crud/select_offset.sql')
                formated_query = query.format(table_name=table_name)

                with conn.cursor() as cursor:
                    cursor.execute(formated_query, (num, start))
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise

class SelectByColumn(QueryInterface):
    def execute(self, config:DatabaseConfigInterface, table_name: str,column: str, value:str):
        try:
            with create_connection(config) as conn:
                conn.autocommit = True
                query = SQLLoader.load_sql('crud/select_by_column.sql')
                formated_query = query.format(table_name=table_name, column=column)

                with conn.cursor() as cursor:
                    cursor.execute(formated_query, (value,))
                    columns = [desc[0] for desc in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except psycopg2.OperationalError as e:
            print(f'Ошибка psycopg2: {e}')
            raise