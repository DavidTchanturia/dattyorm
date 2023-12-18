# Datty ORM

Datty-ORM is a program written in oython that is compatible and works with **CSV**, **JSON** **files**, **PostgresSQL** and Redis. Lets take a look at how we would work with postgres.

# Postgres ORM

This design of ORM lets the users works with databases and tables in Postgres, users can create, tables, perform CRUD operation and write table information in CSV or JSON files.

#### setting up

we start by importing all the necessary modules

```
from model_manager import BaseModel  
from base_database_manager import BaseManager  
import columns
```

BaseModel is a metaclass responsible for creating retrieving user defined class variables to create fields of tables using them. BaseManager implements all the necessary CRUD methods and columns has all the column types defined in them.

#### creating employees table ans an example

```
class Employee(BaseModel):    
    id = columns.PrimaryKey()  
    first_name = columns.VarChar(nullable=False)  
    last_name = columns.VarChar(nullable=False)  
    salary = columns.Integer(default="123")  
    grade = columns.Text()
```

after connecting to the database you can create a table by defining a class, whatever the class name is, the table name will be same. the definition of columns happens by the classes in columns.py, you can even specify primary keys, nullable, default, unique columns.

#### connecting to the database

once the database setting have been defined, connection is established as follows:

```
employee_instance = Employee()  # Instantiate the Employee class  
manager = BaseManager(employee_instance) # to create instance working with our employee table
  
manager.set_connection(DB_SETTINGS)  
  
# Create the Employee table  
manager.create_table(employee_instance)
```

## Basic CRUD operations

#### update

```
manager.update({"last_name": "tchanturia", "salary": 0}, "first_name", "John" )
```

update method takes three arguments, new data as a dictionary, column name and the column value to find the column and update it. for instance the code above will update all the rows with first name of John and set their last_name -> tchanturia, salary -> 0. to update single rows, it would be preferable to use primary key. e.g id


```
manager.update({"last_name": "tchanturia", "salary": 0}, id, 6 )
```


#### select

```
data = manager.select() # by default selects all columns and first 1000

# another version
data = manager.select("first_name", batch_size=500) # selects 500 first_names
```


#### batch insert
```
manager.batch_insert([{"first_name": "John", "last_name": "doe", "grade": "XII"},
                        {"first_name": "ilia", "last_name": "doe", "salary": 104353, "grade": "XII"},
                        {"first_name": "svinia", "last_name": "dode", "salary": 35430, "grade": "XII"}]
```
method takes a list of dicts as an argument, even if we are inserting one row, it should be wrapped around [], and the method inserts all of them in the table.

#### delete
```
manager.delete("last_name", "tchanturia")
```
similarly to update, this method takes in two arguments, column name and the value that the column has, deletes all occurances of rows that have the column name set to that value. In this case, all the rows with tchanturia as a last name, would be deleted.

### Exporting data to CSV or Json
these two methods are quite similar, both of them need to take a relative or an absolute path of the file as an argument and the rest will be handled by the orm, at first the data is converted to pandas DataFrame and then inserted into file

```
# to insert data in json
manager.export_data_as_json("file_path")

# to insert data in csv
manager.export_data_as_csv("file_path")

```