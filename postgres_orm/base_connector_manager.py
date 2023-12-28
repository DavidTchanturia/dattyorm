
import psycopg2


class BaseConnectorManager:
    def __init__(self, table_name):
        """model_class_instance is an instance of the class (table) that will be creating

        class Person() -> creates person table, instance will be instance of Person()

        will be used to get the class attributes and turn them into iterable fields"""
        self.table_name = table_name  # from  <class '__main__.Employee'> get employee as a table name

    def set_connection(self, database_settings: dict) -> None:
        self.connection = psycopg2.connect(**database_settings)
        self.connection.autocommit = True

    def _get_cursor(self):
        return self.connection.cursor()