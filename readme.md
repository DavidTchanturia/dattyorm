# Datty ORM

Datty-ORM is a program written in python that is compatible and works with **CSV**, **JSON** **files**, **PostgresSQL**
and Redis. Lets take a look at how we would work with postgres.

# Postgres ORM

This design of ORM lets the users works with databases and tables in Postgres, users can create, tables, perform CRUD
operation and write table information in CSV or JSON files.

#### setting up

to install the whole package, run the following command
```
pip install datty
```

import all the necessary modules

```
from postgres_orm import columns
from postgres_orm import BaseModel
from postgres_orm import BaseManager
```

BaseModel is a metaclass responsible for creating retrieving user defined class variables to create fields of tables using them.
BaseManager implements all the necessary CRUD methods and columns has all the column types defined in them.
columns is a py, file containing mappings of most of the SQL column types, each one represented as a class.

#### creating employees table and an example

```
class Employee(BaseModel):    
    id = columns.PrimaryKey()  
    first_name = columns.VarChar(nullable=False)  
    last_name = columns.VarChar(nullable=False)  
    salary = columns.Integer(default="123")  
    grade = columns.Text()
```

after connecting to the database you can create a table by defining a class, whatever the class name is, the table name
will be same. the definition of columns happens by the classes in columns.py, you can even specify primary keys, nullable,
default, unique columns.

#### connecting to the database

once the database setting have been defined, connection is established as follows:

```
employee_instance = Employee()  # Instantiate the Employee class
manager = BaseManager(employee_instance, DB_SETTINGS)  # to create instance working with our employee table

# Create the Employee table
manager.create_table(employee_instance)
```
#### adding a new column to existing table
after you have connected to a database and have instantiated a class that connects to a table, you can also add a new column
to the table. manager instance has a composite part, called table_manager, which lets to modify table directly. here are
exampls to add column, drop column, drop table

```
manager.table_manager.add_column_to_table("rame", columns.VarChar())
manager.table_manager.drop_column("last_name")
manager.table_manager.drop_table()
```

add_column_to_table(), takes in two arguments, name of the new column, and a type class from columns.py, that will
map it to appropriate SQL type. drop_column just needs the column name. drop table drops the table.

## Basic CRUD operations

#### update

```
manager.update({"last_name": "tchanturia", "salary": 0}, "first_name", "John" )
```

update method takes three arguments, new data as a dictionary, column name and the column value to find the column and update it.
for instance the code above will update all the rows with first name of John and set their last_name -> tchanturia, salary -> 0.
to update single rows, it would be preferable to use primary key. e.g id


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
method takes a list of dicts as an argument, even if we are inserting one row, it should be wrapped around [],
and the method inserts all of them in the table.

#### delete
```
manager.delete("last_name", "tchanturia")
```
similarly to update, this method takes in two arguments, column name and the value that the column has, deletes all occurances
of rows that have the column name set to that value. In this case, all the rows with tchanturia as a last name, would be deleted.

### Exporting data to CSV or Json
these two methods are quite similar, both of them need to take a relative or an absolute path of the file as an argument
and the rest will be handled by the orm, at first the data is converted to pandas DataFrame and then inserted into file

```
# to insert data in json
manager.export_data_as_json("file_path")

# to insert data in csv
manager.export_data_as_csv("file_path")

```

# JSON and CSV file handlers

This part of the module works with json and csv data files, uses pandas to perform CRUD operations.
implements pydantics BaseModel class to validate file names and create them like that. lets take a look at
JsonDataOperator, CSVDataOperator is quite similar since they inherit from one common parent class.

### setting up
importing necessary classes is simple in this case, you'll have to either import CSVDataOperator or JSONDataOperator

```
from data_operators import JsonDataOperator
from data_operators import CSVDataOperator
```

### reading files
to create an instance of CSVDataOperator and read a file, follow the steps
```
# to create and validate non-existent file
json_operator = JsonDataOperator("test.json")  # before creating, validates name te*st.json -> test.json
json_operator.get_data()

# print out file content and file metadata
print(json_operator.df)
print(json_operator.file_metadata)  # you can view file metadata, and dataframe column names:types
```

### inserting data
all CRUD operations and modifications made to **json_operator** will be reflected to df, not the actual file.
to save the modification to the file, use the following method

```
json_operator.commit_to_file()  # overwrites changes to the file initially created
```

to insert data, use insert_data method and pass the data as dict as an arguments. Assume we have name, age, address.city, address.street
in the dataframe.

```
new_data = {
    "name": "new person",
    "age": 123,
    "address.city": "New York",
    "address.street": "some address in new york"
}

json_operator.insert_data(new_data)
print(json_operator.df)  # prints out df where new row has been added

```

### update data
method works, straight forward, it takes in the identifier column name by which you want
to identify row to update and the value, then new data to update with.
For instance, if you want to update rows that have name "dato". follow these steps:

```
# only need to specify the values you are changing, or you can do all
updated_data = {
    "name": "this was updated",
}

json_operator.update_data("name", "dato", updated_data)
print(json_operator.df)
```

### delete data
works like update data, gets identifier column and identifier value as arguments and deletes them

```
json_operator.delete_data("name", "keti")
print(json_operator.df)
```

#### moving json data to csv
both with csv and json, you can move data to the other extension.
json <-> csv
```
json_operator.write_data_into_csv("your/file/path.csv")
```

# Redis orm
simple orm that lets the user perform CRUD with redis.

### setting up
start by connecting to redis server on your local machine. In terminal
run the following command:

```
redis-server
```
<br>

then in your python program, import redis ORM
```
from redis_orm import RedisORM
```

to create a connection to redis from python, instantiate RedisORM class
by defaults host=localhost, port=6379, you can change them if needed


### insert data
to store data into redis, use insert_into_redis method, since there are 
no relationships or tables in redis and everything is saved on RAM, 
try to save values that cna be identifier or grouped with similar keys.
for instance, you can use insert_into_redis method as follows:

```
redis_orm = RedisORM()

redis_orm.insert_into_redis("user:1", {'name':'John', 'age':23})
redis_orm.insert_into_redis("user:2", {'name':'John', 'age':223})
```

### select
simple way to select is to use key and get the value. you can also use select_all, 
that allows you to select values based on key patterns. you can select all of the data by default
that is currently on redis. to select all of the values that have a key starting with "user",
you'd have to do following:

```
users = redis_orm.select_all(pattern="user*") # be careful with selecting everything without specified patterns
```

### update
update works simply by finding a value using a key and passing values to be updated to the method

### exporting
This ORM also implements methods that let you export all the data from redis to csv or json file.
both methods work similarly so lets take a look at one.

```
redis_orm.export_all_to_csv(pattern="user*", file_path="redis_data.csv")
```
to make sure you are exporting all the data about related topics and not just everything from redis
it is advised to specify the pattern. this creates a csv file and then writes all the selected
data in it.


# Important Note
program automatically creates orm_log.txt file when you install it and will log any necessary and important
errors or info messages.