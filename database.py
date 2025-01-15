from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args= {"check_same_thread" : False})
metadata = MetaData()


#####################################################################################
#create_engine : used to create a connection to the database. it acts as an interface for SQLAlchemy to interact with the database
# MetaData: A container that holds informations about the structure of the database(tables, columns, contraints ...)


# SQLAlchemy: is not a database server. Instead, it is a Python library that provides tools for interacting with databases. 
# It acts as a bridge between Python code and a wide variety of relational databases (like SQLite, PostgreSQL, MySQL, etc.)

# sqlite:///./test.db: Specifies the SQLite database file to use.
    ## sqlite:// indicates the use of SQLite
    ## ./test.db means the database file will be created in the current directory with the name test.db  

#create_engine: Establishes the connection to the SQLite database using the DATABASE_URL
#connect_args={"check_same_thread": False}: SQLite by default restricts the same database connection to one thread. This argument disables that restriction, allowing multiple threads to use the same connection.

# MetaData(): Initializes a metadata object that will store the structure of the database, such as tables, columns, and constraints.


