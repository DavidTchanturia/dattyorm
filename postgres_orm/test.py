# from model_manager import BaseModel
from base_database_manager import BaseManager

DB_SETTINGS = {
    'host': 'localhost',
    'port': '5432',
    'database': 'orm',
    'user': 'postgres',
    'password': 'postgres'
}

class Employee():
    table_name = "employees"


employee_fields = {
    "id": "SERIAL PRIMARY KEY",
    "first_name": "VARCHAR(50)",
    "last_name": "VARCHAR(50)",
    "salary": "INTEGER",
    "grade": "VARCHAR(10)"
}

# this is for insertion
employees = [{
    "first_name": "dato",
    "last_name": "tchanturia",
    "salary": "500",
    "grade": "third"
},
{
    "first_name": "giorgi",
    "last_name": "ara chanturia",
    "salary": "2000",
    "grade": "first"
},

]


manager = BaseManager(Employee)
manager.set_connection(DB_SETTINGS)

# Create the Employee table
manager.create_table(employee_fields)
manager.batch_insert(employees)
