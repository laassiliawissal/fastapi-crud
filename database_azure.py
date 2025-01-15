from sqlalchemy import create_engine, MetaData
import urllib

# Update DATABASE_URL to connect to Azure SQL Database using aioodbc
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
