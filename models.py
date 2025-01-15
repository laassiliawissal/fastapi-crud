from sqlalchemy import Table, Column, String
from database_azure import metadata

# Define the items table
items_table = Table(
    "items",
    metadata,
    Column("name", String(255), primary_key=True),
    Column("description", String),
 )

