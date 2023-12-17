import psycopg2


class BaseManagerConnector:
    def __init__(self, model_class_instance):
        self.model_class = model_class_instance.__class__ # since I pass the isntance as an agrument, to get the actual class
        self.model_class_name = model_class_instance.__class__.__name__  # from  <class '__main__.Employee'> get employee as a table name

    def set_connection(self, database_settings):
        self.connection = psycopg2.connect(**database_settings)
        self.connection.autocommit = True

    def _get_cursor(self):
        return self.connection.cursor()

    def _close_connection(self):
        self.connection.close()


class BaseManager(BaseManagerConnector):
    def create_table(self, model_class):
        table_name = self.model_class_name
        fields = [f"{field} {data_type}" for field, data_type in model_class.fields.items() if field != 'table_name']

        # Constructing the CREATE TABLE query
        field_definitions = ", ".join(fields)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})"

        # Execute the query
        cursor = self._get_cursor()
        cursor.execute(query)


    def select(self, *field_names, batch_size=1000):
        if not field_names:
            field_names = ["*"]  # if field names are not specified, select all

        select_fields = ", ".join(field_names)
        query = f"SELECT {select_fields} FROM {self.model_class_name} LIMIT {batch_size}"

        cursor = self._get_cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print(f"Error: {e}")



    def batch_insert(self, rows: list):
        if not rows:
            return

        fields = list(rows[0].keys())  # row headers
        values_template = ", ".join(["%s"] * len(fields))  # the values to insert
        insert_query = f"INSERT INTO {self.model_class_name} ({', '.join(fields)}) VALUES ({values_template})"

        cursor = self._get_cursor()
        try:
            rows_to_insert = [[row[field] for field in fields] for row in rows]
            cursor.executemany(insert_query, rows_to_insert)
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def update(self, new_data: dict):
        pass

    def delete(self):
        pass


