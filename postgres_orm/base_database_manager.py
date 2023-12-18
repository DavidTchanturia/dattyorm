import pandas as pd
import psycopg2
from base_connector_manager import BaseConnectorManager


class BaseManager(BaseConnectorManager):
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

    def update(self, id, new_data: dict):
        set_values = ", ".join([f"{key} = %s" for key in new_data.keys()])

        # Construct the UPDATE query
        query = f"UPDATE {self.model_class_name} SET {set_values} WHERE id = %s"  # Replace 'index_column' with the actual column name for indexing

        cursor = self._get_cursor()

        try:
            values_to_update = list(new_data.values())
            values_to_update.append(id)

            cursor.execute(query, values_to_update)
            self.connection.commit()
            print("Update successful.")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def delete(self, identifier_column_name, column_value):
        query = f"DELETE FROM {self.model_class_name} WHERE {identifier_column_name} = %s"

        cursor = self._get_cursor()
        try:
            cursor.execute(query, (column_value,))
            self.connection.commit()
            print("Delete successful.")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def export_data_as_csv(self, path_to_csv_file):
        try:
            df = self._get_data_for_export()
            # Export DataFrame to a CSV file
            df.to_csv(path_to_csv_file, index=False)
            print(f"Data exported to {path_to_csv_file} successfully.")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def export_data_as_json(self, path_to_json_file):
        try:
            df = self._get_data_for_export()

            df.to_json(path_to_json_file, orient="records", indent=4)
            print(f"data successfully exported to {path_to_json_file}")
        except psycopg2.Error:
            print(f"Error while exporting")

    def _get_data_for_export(self):
        cursor = self._get_cursor()
        cursor.execute(f"SELECT * FROM {self.model_class_name}")
        rows = cursor.fetchall()

        if not rows:
            print("No data to export.")
            return

        # Get column names from the cursor description
        columns = [desc[0] for desc in cursor.description]

        # Convert rows to a DataFrame using pandas
        df = pd.DataFrame(rows, columns=columns)

        return df
