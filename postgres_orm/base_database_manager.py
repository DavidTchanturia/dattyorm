import psycopg2


class BaseManagerConnector:
    def __init__(self, model_class):
        self.model_class = model_class
        self.connection = None

    def set_connection(self, database_settings):
        self.connection = psycopg2.connect(**database_settings)
        self.connection.autocommit = True

    def _get_cursor(self):
        return self.connection.cursor()

    def _close_connection(self):
        self.connection.close()


class BaseManager(BaseManagerConnector):
    def create_table(self, fields):
        field_names = [f"{field} {data_type}" for field, data_type in fields.items()]
        fields_format = ", ".join(field_names)
        query = f"CREATE TABLE IF NOT EXISTS {self.model_class.table_name} ({fields_format})"
        cursor = self._get_cursor()
        cursor.execute(query)

    def select(self, *field_names):
        pass

    def batch_insert(self, rows: list):
        if not rows:
            return

        fields = list(rows[0].keys())  # row headers
        values_template = ", ".join(["%s"] * len(fields))  # the values to insert
        insert_query = f"INSERT INTO {self.model_class.table_name} ({', '.join(fields)}) VALUES ({values_template})"

        cursor = self._get_cursor()
        try:
            rows_to_insert = [[row[field] for field in fields] for row in rows]
            cursor.executemany(insert_query, rows_to_insert)
        except psycopg2.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            self._close_connection()

    def update(self, new_data: dict):
        pass

    def delete(self):
        pass


