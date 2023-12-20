import pandas as pd
import psycopg2
import logging
from .base_connector_manager import BaseConnectorManager
from utils.orm_logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class BaseManager(BaseConnectorManager):
    def create_table(self, model_class_instance):
        """
        creates a table base on the class name that inherits from BaseModel.
        -------
        class Example(BaseManager): -> creates example table

        args:
        - `model_class_instance`: an instance of class representing the table in the db.
        """
        table_name = self.model_class_name
        fields = [f"{field} {data_type}" for field, data_type in model_class_instance.fields.items()]
        # construct create table query
        field_definitions = ", ".join(fields)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})"

        # Ill be using with to make sure cursor is closed every time
        with self._get_cursor() as cursor:
            cursor.execute(query)

    def select(self, *field_names, batch_size=1000):
        """
        select data from the database, can select custom fields and sizes

        args:
        - `field_names`: list of fields to be selected, if not specified, select all
        - `batch_size`: size of the batch to be selected, if not specified, select first 1000

        returns:
        - list of the rows selected by the query"""
        if not field_names:
            field_names = ["*"]  # if field names are not specified, select all

        # construct select query
        select_fields = ", ".join(field_names)
        query = f"SELECT {select_fields} FROM {self.model_class_name} LIMIT {batch_size}"

        cursor = self._get_cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def batch_insert(self, rows: list[dict]):
        """
        insert single or multiple rows of data in the table.

        args:
        - `rows`: list containing dictionaries of individual data instances. even if inserting single data.
        dict should be wrapped in the list.
        """
        if not rows:
            return

        fields = list(rows[0].keys())  # row headers
        values_template = ", ".join(["%s"] * len(fields))  # the values to insert
        insert_query = f"INSERT INTO {self.model_class_name} ({', '.join(fields)}) VALUES ({values_template})"

        cursor = self._get_cursor()
        try:
            rows_to_insert = [[row[field] for field in fields] for row in rows]
            cursor.executemany(insert_query, rows_to_insert)
        except KeyError as e:
            logger.error(f"KeyError: {e}")

    def update(self, new_data: dict, identifier_column_name, identifier_value):
        """
        update single or many rows of data. in each row of data, all of the values or selected values
        could be modified

        args:
        - `new_data`: dict of the column-value pairs to be updated.
        - `identifier_column_name`: column name to identify which columns to update.
        - `identifier_value`: find the columns that have given value to update them.
        """
        set_values = ", ".join([f"{key} = %s" for key in new_data.keys()])

        # Construct the UPDATE query
        query = f"UPDATE {self.model_class_name} SET {set_values} WHERE {identifier_column_name} = %s"

        cursor = self._get_cursor()

        try:
            values_to_update = list(new_data.values())
            values_to_update.append(identifier_value)

            cursor.execute(query, values_to_update)
            self.connection.commit()
            print("Update successful.")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def delete(self, identifier_column_name, column_value):
        """
        based on identifier provided, delete a row or rows from the table.

        args
        identifier_column_name: column name to identify row with
        column_value: value of the given column name to select single or multiple rows
        """
        query = f"DELETE FROM {self.model_class_name} WHERE {identifier_column_name} = %s"

        cursor = self._get_cursor()
        try:
            cursor.execute(query, (column_value,))
            self.connection.commit()
            print("Delete successful.")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def export_data_as_csv(self, path_to_csv_file):
        """
        export all the data from table to a csv file

        args
        path_to_csv_file: absolute or relative path to the csv file
        """
        try:
            df = self._get_data_for_export()
            # Export DataFrame to a CSV file
            df.to_csv(path_to_csv_file, index=False)
            print(f"Data exported to {path_to_csv_file} successfully.")
        except psycopg2.Error as e:
            print(f"Error: {e}")

    def export_data_as_json(self, path_to_json_file):
        """
        export all the data from table to a json file

        args
        path_to_csv_file: absolute or relative path to the json file
        """
        try:
            df = self._get_data_for_export()

            df.to_json(path_to_json_file, orient="records", indent=4)
            print(f"data successfully exported to {path_to_json_file}")
        except psycopg2.Error:
            print(f"Error while exporting")

    def _get_data_for_export(self) -> pd.DataFrame:
        """
        select all the data from table and return them as pandas Dataframe
        """
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
