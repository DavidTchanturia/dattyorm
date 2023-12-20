from model_manager import BaseModel
from base_database_manager import BaseManager
import columns

DB_SETTINGS = {
    'host': 'localhost',
    'port': '5432',
    'database': 'orm',
    'user': 'postgres',
    'password': 'postgres'
}

class Employee(BaseModel):
    """will create a table with the name as same as class name, but lower case"""
    id = columns.PrimaryKey()
    first_name = columns.VarChar(nullable=False, size=50)
    last_name = columns.VarChar(nullable=False, size=255)
    salary = columns.Integer(default=5000)
    grade = columns.Text()

employee_instance = Employee()  # Instantiate the Employee class
manager = BaseManager(employee_instance)

# always remember to close connection at the end
manager.set_connection(DB_SETTINGS)

# Create the Employee table
# manager.create_table(employee_instance)
manager.batch_insert([{"first_name": "John", "last_name": "doe", "grade": "XII"},
                        {"first_name": "ilia", "last_name": "doe", "salary": 104353, "grade": "XII"},
                        {"first_name": "svinia", "last_name": "dode", "salary": 35430, "grade": "XII"},
                        {"first_name": "kolia", "last_name": "doe", "salary": 106, "grade": "XII"},
                        {"first_name": "zolia", "last_name": "doe", "salary": 1030, "grade": "XII"}
                      ])

#
# manager.update({"last_name": "tchanturia", "salary": 0}, "first_name", "John" )
#
# manager.export_data_as_csv("employee.csv")
# manager.export_data_as_json("employee.json")