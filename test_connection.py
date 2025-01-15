# script to test the connection to your Azure SQL Database
import pyodbc

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:sqldbserver-w.database.windows.net,1433;"
    "Database=itemsDB;"
    "Uid=wissal;"
    "Pwd=Almaghribia@123;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
