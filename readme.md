# Step1: Install fastAPI and Uvicorn
THEY WILL BE USED TO RUN your application
```bash
pip install fastapi uvicorn
```

```bash

``` 

# Step 2: 
create main.py:
    - import fastAPI
    - Create an instance of FastAPI class


# Step 3: Define a Simple Object for CRUD Operations
```bash
from typing import List

# A simple in-memory list to store items
items = []

# Item model definition (this is just a dictionary for simplicity)
class Item:
    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description

```

When you create an Item object, like this:
item1 = Item(name="Laptop", description="A personal computer")
The __init__ method is automatically invoked, and the name and description attributes are initialized with the provided values.

# Step 4: Create a Read Operation (GET)

We’ll start by adding a route to read all items in the "database" (our in-memory list).

FastAPI provides the @app.get decorator for GET requests. Here’s how we can create a simple endpoint to get all items:
```bash
@app.get("/items", response_model=List[Item])
async def get_items():
    return items
```

What’s happening here:
-  @app.get("/items") sets up a route at /items that responds to GET requests.
- response_model=List[Item] tells FastAPI that the response will be a list of Item objects.
- get_items is the function that handles the request. It simply returns the list of items.


The **async** keyword is used in Python to define asynchronous functions. When used with FastAPI, it allows the endpoint to handle requests asynchronously, meaning that the server can handle other tasks while waiting for I/O-bound operations (like database queries, network requests, etc.) to complete.

# ERROR: FIXED
The error you're encountering happens because FastAPI expects the response model to be a Pydantic model, but you're using a regular Python class (Item). **FastAPI requires Pydantic models for request and response validation**.

Solution:
You need to convert the Item class into a Pydantic model. Here's how you can fix it:

- Import Pydantic's BaseModel: The BaseModel class from Pydantic is used to create models that FastAPI can automatically validate and serialize.
- Change Item class to inherit from BaseModel.

# Step 5: Create a Create Operation (POST)
Now, we'll add a POST request to allow adding new items to the in-memory list.

Here’s how to add a route to create a new item:

from fastapi import HTTPException
```bash
@app.post("/items", response_model=Item)
async def create_item(item: Item):
    # Adding the item to the in-memory database (list)
    items.append(item)
    return item
```
What’s happening here:
- @app.post("/items") sets up a route at /items that responds to POST requests.
- item: Item means that the incoming request should contain an Item object (FastAPI automatically handles parsing the request body and converting it into an Item).
- The item is added to the items list, and then the newly created item is returned.


# Step 7: Add an Update Operation (PUT)
In this step, we'll create an endpoint to update an existing item. Since we're not using a database, we’ll identify the item by its index in the list (you can also add more sophisticated identifiers if you like).

Here’s how to implement it:
```bash
from fastapi import HTTPException

@app.put("/items/{item_name}", response_model=Item)
async def update_item(item_name: str, item: Item):
    # Try to find the item by name
    for idx, existing_item in enumerate(items):
        if existing_item.name == item_name:
            items[idx] = item  # Update the item in the list
            return item  # Return the updated item

    # If the item is not found, raise a 404 error
    raise HTTPException(status_code=404, detail="Item not found")
```
What’s happening here:

- The @app.put("/items/{item_name}") route uses a PUT method and a path parameter (item_name) to identify the item.
- We loop through the items list to find the item by name.
- If the item is found, we update it in the list and return the updated item.
- If the item isn’t found, we raise a 404 error with HTTPException.


# Step 8: Add a Delete Operation (DELETE)
In this step, we'll create an endpoint to delete an item by its name. Here's how you can implement the DELETE method:

```bash

@app.delete("/items/{item_name}", response_model=Item)
async def delete_item(item_name: str):
    for idx, existing_item in enumerate(items):
        if existing_item.name == item_name:
            deleted_item = items.pop(idx)  # Remove the item from the list
            return deleted_item  # Return the deleted item

    raise HTTPException(status_code=404, detail="Item not found")

```

What’s happening here:

The @app.delete("/items/{item_name}") decorator sets up the DELETE route, where the item is identified by its name.
We loop through the items list, and if the item is found, we remove it using pop().
If the item is not found, we raise a 404 error with HTTPException.


# STEP THTA FOLLOWS:
    ## Connect the app to a local sql Database.
    ## Connect the app to a cloud sql Database.
        - Azure
        _ sql database

# Steps to Set Up Azure Account and SQL Server with Firewall Rule
# Azure SQL Database Setup

## Steps to Set Up Azure Account and SQL Server with Firewall Rule

### 1. Create Azure Account
- Sign up for a free Azure account at [Azure Portal](https://portal.azure.com).

### 2. Create Azure SQL Database and Server
- Navigate to **Create a Resource** > **Databases** > **Azure SQL**.
- Select **Single Database** and create a new server by:
  - Specifying the **server name** and **region**.
  - Enabling **SQL Authentication** with an admin username and password.
- Choose the **Free Tier (Basic)** pricing option.

### 3. Enable Public Access to the Database
- Go to the **SQL Server** settings under **Networking**.
- Enable **Public endpoint** access.
- Add your client IP address to the **Firewall Rules** using the **Add your client IPv4 address** option.
- Save the settings to allow your app to connect to the database.

### 4. Obtain Connection String
- Navigate to the database's **Connection Strings** section.
- Copy the **ODBC (SQL authentication)** string for use in the app.

Driver={ODBC Driver 18 for SQL Server};Server=tcp:sqldbserver-w.database.windows.net,1433;Database=itemsDB;Uid=wissal;Pwd=Almaghribia@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

### install ODBC Driver on local system to be able to connect to the remote ODBC DATABASE (this is important):
https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15


# NEXT STEP_ test itemsDB from Azure sql from my python code:

To test your app’s connection to the Azure SQL Database, follow these steps:

1. Install Required Libraries (Locally)
Ensure pyodbc is installed on your local machine:

pip install pyodbc
2. Test Connection Using Python Script
Create a Python script (test_connection.py) to test the connection to your Azure SQL Database. Replace the placeholders with your actual Azure SQL credentials:

import pyodbc

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:sqldbserver-w.database.windows.net,1433;"
    "Database=itemsDB;"
    "Uid=wissal;"
    "Pwd=YourSecurePasswordHere;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

try:
    connection = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print("Error:", e)
3. Run the Script Locally
Execute the script from your terminal to check if the connection is successful:

python test_connection.py
Success: If the connection is successful, you will see "Connection successful!" in the terminal.
Failure: If there's an error, the message will provide details. Common errors to check for:
Incorrect credentials: Verify your username and password.
Firewall issue: Ensure your public IP is allowed in the Azure SQL Database firewall settings.


# NEXT STEP:
###  FAST API AND AZURE SQL SERVER (MSSQL) USING 
USE **FastAPI** to api handling, **SQLAlchemy** for database interaction, pyodbc for connecting to Azure SQL Server.

- ODBC drivers (like ODBC Driver 18 for SQL Server) are installed seperatly acts as a bridge between the python api and the SQL Server database.
- the connection string: you can get it from azure, but to use it with SQLAlchemy you will have to encode it, Use urllib.parse.quote_plus to encode special characters in the string.
- SQLAlchemy engine represents the connection to the database; Use create_engine() to initialize the engine with you connection string
- Use Events in FastAPI, use ```bash  @app.on_event("startup") ``` to define the code that runs when the fastAPI server starts (like testing the database connection)
- SQLAlchemy uses the MetaData object to define and manage the database schema (tables, columns ...)
- use ```bash engine.connect() ``` to ensure the connection to the database works
- QUERY ```bash  INFORMATION_SHCEMA.TABLES ```


### Summary of What to Memorize
#### Libraries:
FastAPI for API handling, SQLAlchemy for database interaction, and pyodbc for connecting to SQL Server.
#### Steps to Connect:
Use pyodbc connection string format for Azure SQL.
Encode the connection string with urllib.parse.quote_plus.
Use create_engine() to create a database engine in SQLAlchemy.
#### FastAPI Integration:
Use the @app.on_event("startup") decorator to handle setup tasks like testing the database connection.
#### Debugging Tips:
Always verify the connection string format.
Ensure the correct ODBC driver is installed.
Use echo=True in create_engine to enable SQLAlchemy logs for troubleshooting.

(https://stackoverflow.com/questions/53704187/connecting-to-an-azure-database-using-sqlalchemy-in-python )


##### Working Database Connection Code
```bash
# Connect Python API to Azure SQL Server with FastAPI, SQLAlchemy, and pyodbc

from fastapi import FastAPI # Import fastAPI for building the API
from sqlalchemy import create_engine, MetaData, text  # Import SQLAlchemy Components
import urllib # Import urllib to handle the url encoding for the connection string

app = FastAPI() # Initialize the fastAPI Application

# Encode the connection string
params = urllib.parse.quote_plus( # Encode the connection string to make URL Safe #  The r before the string in Python denotes a raw string literal. It tells Python to treat the string exactly as it is, without interpreting escape characters.
    r'Driver={ODBC Driver 18 for SQL Server};' # Specify the ODBC Driver
    r'Server=tcp:sqldbserver-w.database.windows.net,1433;' # Azure SQL hostname and port
    r'Database=itemsDB;' # Database name
    r'Uid=wissal;' # username for authentification
    r'Pwd=Almaghribia@123;' # pwd for auth
    r'Encrypt=yes;' # Encrypt communication with the database
    r'TrustServerCertificate=no;' # Do not trust the server certificate (requires proper validation)
    r'Connection Timeout=30;' # timeout setting for establishing the connection
)

#format the connection string for SQLAlchemy
conn_str = f'mssql+pyodbc:///?odbc_connect={params}' # use the encoded parameters for SQLAlchemy

# Create the SQLAlchemy engine
engine = create_engine(conn_str, echo=True) # the engine manages the database connection and interaction, echo=True logs SQL Commands
metadata = MetaData() # Matadata is a container for schema-level information about the database

# Event triggerd when fastAPI app starts
@app.on_event("startup")
async def startup_event():
    try:
        # Test the connection
        with engine.connect() as conn: # Establish a connection using engine
            print("Connection to the database is successful!")
            # Use the `text` function to execute raw SQL
            result = conn.execute(text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")) # query the database for tables names
            tables = result.fetchall()  # Fetch all rows from the result of the query
            print("Tables in the database:", [table[0] for table in tables])  # Display table names (The first element (table[0]) of each tuple contains the name of the table.)
    except Exception as e:
        # handle any errors within db connection or db query excecution
        print(f"Database connection failed: {e}")


```

###### Code excecution results:

```bash
(base) laassiliawissal@macbookpro fastapi_crud_101 % uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/laassiliawissal/fastAPI/fastapi_crud_101']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [61836] using WatchFiles
INFO:     Started server process [61838]
INFO:     Waiting for application startup.
2025-01-13 12:30:13,150 INFO sqlalchemy.engine.Engine SELECT CAST(SERVERPROPERTY('ProductVersion') AS VARCHAR)
2025-01-13 12:30:13,151 INFO sqlalchemy.engine.Engine [raw sql] ()
2025-01-13 12:30:13,222 INFO sqlalchemy.engine.Engine SELECT schema_name()
2025-01-13 12:30:13,222 INFO sqlalchemy.engine.Engine [generated in 0.00024s] ()
2025-01-13 12:30:13,436 INFO sqlalchemy.engine.Engine SELECT CAST('test max support' AS NVARCHAR(max))
2025-01-13 12:30:13,436 INFO sqlalchemy.engine.Engine [generated in 0.00023s] ()
2025-01-13 12:30:13,508 INFO sqlalchemy.engine.Engine SELECT 1 FROM fn_listextendedproperty(default, default, default, default, default, default, default)
2025-01-13 12:30:13,508 INFO sqlalchemy.engine.Engine [generated in 0.00021s] ()
Connection to the database is successful!
2025-01-13 12:30:13,650 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-01-13 12:30:13,650 INFO sqlalchemy.engine.Engine SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
2025-01-13 12:30:13,650 INFO sqlalchemy.engine.Engine [generated in 0.00030s] ()
Tables in the database: ['database_firewall_rules']
2025-01-13 12:30:13,723 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     Application startup complete.

```

###### Code result explanation:

""

Let's go through the output line by line and explain what each part means:

1. Startup Logs:
uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/laassiliawissal/fastAPI/fastapi_crud_101']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [61836] using WatchFiles
INFO:     Started server process [61838]
uvicorn main:app --reload: This starts your FastAPI app using the Uvicorn server in development mode (--reload enables auto-reloading if the code changes).
Will watch for changes in these directories: Uvicorn monitors the fastapi_crud_101 folder for code changes.
127.0.0.1:8000: Your FastAPI app is running on localhost (127.0.0.1) at port 8000.
Started reloader and server process: Uvicorn has started two processes:
One for monitoring and reloading code changes.
The other for serving your application.
2. SQLAlchemy Engine Initialization:
INFO:     Waiting for application startup.
2025-01-13 12:30:13,150 INFO sqlalchemy.engine.Engine SELECT CAST(SERVERPROPERTY('ProductVersion') AS VARCHAR)
2025-01-13 12:30:13,151 INFO sqlalchemy.engine.Engine [raw sql] ()
Waiting for application startup: FastAPI waits for all @app.on_event("startup") functions to complete.
SELECT CAST(SERVERPROPERTY('ProductVersion') AS VARCHAR):
SQLAlchemy sends this query to the database to get the SQL Server version.
The result confirms the SQL Server is accessible.
[raw sql] (): This indicates no parameters were passed to the query.
3. Database Schema Queries:
2025-01-13 12:30:13,222 INFO sqlalchemy.engine.Engine SELECT schema_name()
2025-01-13 12:30:13,222 INFO sqlalchemy.engine.Engine [generated in 0.00024s] ()
SELECT schema_name(): SQLAlchemy checks the current database schema.
[generated in 0.00024s]: The query execution time is 0.24 milliseconds.
4. Test Compatibility:
2025-01-13 12:30:13,436 INFO sqlalchemy.engine.Engine SELECT CAST('test max support' AS NVARCHAR(max))
2025-01-13 12:30:13,436 INFO sqlalchemy.engine.Engine [generated in 0.00023s] ()
SELECT CAST('test max support' AS NVARCHAR(max)): SQLAlchemy tests the database's support for large text fields (NVARCHAR(max)).
5. Extended Properties:
2025-01-13 12:30:13,508 INFO sqlalchemy.engine.Engine SELECT 1 FROM fn_listextendedproperty(default, default, default, default, default, default, default)
2025-01-13 12:30:13,508 INFO sqlalchemy.engine.Engine [generated in 0.00021s] ()
SELECT 1 FROM fn_listextendedproperty(...): SQLAlchemy checks for database properties like constraints or extended metadata.
6. Connection Success:
Connection to the database is successful!
This is a log from your Python code indicating the database connection was established successfully.
7. List Tables:
2025-01-13 12:30:13,650 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2025-01-13 12:30:13,650 INFO sqlalchemy.engine.Engine SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
2025-01-13 12:30:13,650 INFO sqlalchemy.engine.Engine [generated in 0.00030s] ()
Tables in the database: ['database_firewall_rules']
2025-01-13 12:30:13,723 INFO sqlalchemy.engine.Engine ROLLBACK
BEGIN (implicit): SQLAlchemy starts a transaction to run the query.
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES: This query lists all table names in the database. The result is:
['database_firewall_rules']: The only table in your database currently is database_firewall_rules.
ROLLBACK: Since the operation didn’t modify data, SQLAlchemy rolls back the transaction.
8. Application Ready:
INFO:     Application startup complete.
Your FastAPI application is fully initialized and ready to handle requests.
Summary of Results:
The database connection is successful.
Your database currently has one table: database_firewall_rules.
All the SQLAlchemy initialization queries confirm compatibility and support.
The app is ready to serve HTTP requests.
You can now proceed to add more tables or create API endpoints to interact with the database!

""




### SQLAlchemy Overview
- SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM) that provides developers with powerful tools for interacting with databases. It is designed to simplify the process of working with relational databases in Python, offering flexibility, performance, and a clear abstraction of database operations.


### Data validation
Pydantic is a data validation and settings management library for Python. It uses Python type annotations to validate data, ensuring the data conforms to expected types and constraints. It's often used with FastAPI to define models and validate request data.

Here’s a simple example:

```bash from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

- Example usage
```bash
user = User(name="John", age=30)
print(user)
```
In this example, Pydantic automatically validates the types of name and age when creating a User instance. If the data doesn't match the expected types, Pydantic raises a ValidationError.


### Create the BASE Model:
```bash
class Item(BaseModel):
    name: str
    description : Optional[str] = None
```


###  Post endpoint to add the data to the database:

```bash

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    # Prepare the data for insertion
    new_item={
        "name": item.name,
        "description": item.description
    }
    try:
        with engine.connect() as conn:
            #Insertthe item into the items table
            conn.execute(insert(items_table).values(new_item))
            conn.commit()
            return {"message": f"Item created successfully {new_item}"}
    except Exception as e :
        # Handle any errors that occur during insertion
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error inserting item: {e}"
        )


```