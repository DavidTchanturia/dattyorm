import pandas as pd
import logging
from .base_connector_manager import BaseConnectorManager
from utils.orm_logger import setup_logging
import psycopg2

setup_logging()
logger = logging.getLogger(__name__)


class BaseManager(BaseConnectorManager):
    def __init__(self, table_name, columns_dict, db_settings=None):
        super().__init__(table_name)
        self.columns_dict = columns_dict
        self.set_connection(db_settings)
        self.table_manager = TableManager(self.table_name, self._get_cursor())

    def create_table(self):
        """
        Creates a table based on the provided columns_dict.
        """
        table_name = self.table_name
        fields = [f"{field} {data_type}" for field, data_type in self.columns_dict.items()]
        field_definitions = ", ".join(fields)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})"

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
        query = f"SELECT {select_fields} FROM {self.table_name} LIMIT {batch_size}"

        with self._get_cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

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
        insert_query = f"INSERT INTO {self.table_name} ({', '.join(fields)}) VALUES ({values_template})"

        with self._get_cursor() as cursor:
            try:
                rows_to_insert = [[row[field] for field in fields] for row in rows]
                cursor.executemany(insert_query, rows_to_insert)
            except KeyError as e:
                logger.error(f"trying to insert with invalid key")

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
        query = f"UPDATE {self.table_name} SET {set_values} WHERE {identifier_column_name} = %s"

        with self._get_cursor() as cursor:

            values_to_update = list(new_data.values())
            values_to_update.append(identifier_value)

            cursor.execute(query, values_to_update)
            self.connection.commit()

    def delete(self, identifier_column_name, column_value):
        """
        based on identifier provided, delete a row or rows from the table.

        args
        identifier_column_name: column name to identify row with
        column_value: value of the given column name to select single or multiple rows
        """
        query = f"DELETE FROM {self.table_name} WHERE {identifier_column_name} = %s"

        with self._get_cursor() as cursor:
            cursor.execute(query, (column_value,))
            self.connection.commit()

    def export_data_as_csv(self, path_to_csv_file):
        """
        export all the data from table to a csv file

        args
        path_to_csv_file: absolute or relative path to the csv file
        """
        df = self._get_data_for_export()
        # export the current dataframe to csv file
        df.to_csv(path_to_csv_file, index=False)
        logger.info(f"Data exported to {path_to_csv_file} successfully.")

    def export_data_as_json(self, path_to_json_file):
        """
        export all the data from table to a json file

        args
        path_to_csv_file: absolute or relative path to the json file
        """
        df = self._get_data_for_export()

        df.to_json(path_to_json_file, orient="records", indent=4)
        logger.info(f"data successfully exported to {path_to_json_file}")

    def _get_data_for_export(self) -> pd.DataFrame:
        """
        select all the data from table and return them as pandas Dataframe
        """
        cursor = self._get_cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()

        if not rows:
            logger.info(f"no data in the table {self.table_name}")
            return

        # Get column names from the cursor description
        columns = [desc[0] for desc in cursor.description]

        # Convert rows to a DataFrame using pandas
        df = pd.DataFrame(rows, columns=columns)

        return df


class TableManager:
    def __init__(self, model_class_name: str, cursor):
        self.model_class_name = model_class_name
        self.cursor = cursor

    # def add_column_to_table(self, column_name, column_class) -> None:
    #     try:
    #         if not isinstance(column_class, columns.Column):
    #             logger.error(f"Column class: {column_class} not a valid column")
    #
    #         query = f"ALTER TABLE {self.model_class_name} ADD COLUMN {column_name} {column_class.type}"
    #
    #         self.cursor.execute(query)
    #     except psycopg2.errors.DuplicateColumn:
    #         logger.error(f"column {column_name} already exists")

    def drop_column(self, column_name,) -> None:
        try:
            query = f"ALTER TABLE {self.model_class_name} DROP COLUMN {column_name}"

            self.cursor.execute(query)
        except psycopg2.errors.UndefinedColumn as e:
            logger.error(f"column {column_name} does not exists")

    def drop_table(self):
        try:
            query = f"DROP TABLE {self.model_class_name}"

            self.cursor.execute(query)
        except psycopg2.errors.UndefinedTable:
            logger.error(f"table {self.model_class_name} does not")