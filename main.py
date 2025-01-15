# Connect Python API to Azure SQL Server with FastAPI, SQLAlchemy, and pyodbc

from typing import Optional, List
from fastapi import FastAPI, HTTPException, status # Import fastAPI for building the API
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from sqlalchemy import text, select, insert, update, delete  # Import SQLAlchemy Components

from pydantic import BaseModel
import uvicorn

from models import items_table
from database_azure import engine, metadata



app = FastAPI() # Initialize the fastAPI Application

#CORS setup for cross-origin request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, for security, restrict if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# create a Pydantic model to handle input validation for creating and updating items.
class Item(BaseModel):
    name: str
    description : Optional[str] = None

# Event triggerd when fastAPI app starts
@app.on_event("startup")
async def startup_event():
    try:
        #create tables if they don't exist
        metadata.create_all(engine)
        # Test the connection
        with engine.connect() as conn: # Establish a connection using engine
            print("Connection to the database is successful!")
            # Use the `text` function to execute raw SQL
            result = conn.execute(text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")) # query the database for tables names # INFORMATION_SCHEMA.TABLES is a special system view in SQL that provides metadata about all the tables in a database.
            tables = result.fetchall()  # Fetch all rows from the result of the query
            print("Tables in the database:", [table[0] for table in tables])  # Display table names (The first element (table[0]) of each tuple contains the name of the table.)

            # Check if 'items' table exists
            table_names = [table[0] for table in tables]
            if 'items' in table_names:
                print("The 'items' table exists. Selecting all items...")
                # Select al rows from items-table
                result = conn.execute(select(items_table))
                items = result.fetchall()
                print("items rows", items)
            else:
                print("The 'items' table was not created.")

    except Exception as e:
        # handle any errors within db connection or db query excecution
        print(f"Database connection failed: {e}")

#Create endpoint with POST

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


#GET ALL ITEMS FROM Item db
@app.get('/items', response_model=List[Item], status_code=status.HTTP_200_OK)
async def get_items():
    try:
        with engine.connect() as conn:
            #Select all items from the items table
            result = conn.execute(select(items_table))
            items = result.fetchall()

            if not items:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No items found")
            
            #Convert rows to a list of dict
            all_items = [{"name":item.name, "description": item.description} for item in items]
            return all_items 

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error retrieviing Item {e}")

# GET ENDPOINT. getItembyId

# PUT
@app.put('/items/{item_name}', status_code=status.HTTP_200_OK)
async def update_item(item_name: str, item: Item):
    #Prepare the item for update
    updated_item = {
        "name": item.name,
        "description": item.description
    }
    try:
        #
        with engine.connect() as conn:
            #Update the item by replacing its data completly 
            result = conn.execute(update(items_table).where(items_table.c.name == item_name).values(updated_item))
            conn.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item_name} not found")
            
            return {"message" : "Item updated successfully", "item": updated_item}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating item: {e}")

#DELETE
@app.delete('/items/{item_name}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_name: str):
    try:
        with engine.connect() as conn:
            #DELETE THE ITEM BASE ON ITS NAME
            result = conn.execute(items_table.delete().where(items_table.c.name == item_name))
            conn.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {item_name} not found")
            
    except Exception as e:
        raise HTTPException()