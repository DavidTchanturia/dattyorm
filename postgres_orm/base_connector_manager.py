import psycopg2


class BaseConnectorManager:
    def __init__(self, model_class_instance):
        self.model_class = model_class_instance.__class__ # since I pass the isntance as an agrument, to get the actual class
        self.model_class_name = model_class_instance.__class__.__name__  # from  <class '__main__.Employee'> get employee as a table name

    def set_connection(self, database_settings: dict) -> None:
        self.connection = psycopg2.connect(**database_settings)
        self.connection.autocommit = True

    def _get_cursor(self):
        return self.connection.cursor()

    def _close_connection(self):
        self.connection.close()