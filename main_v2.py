#here we are using sqlite as db
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from databases import Database
from models import items_table
from database import DATABASE_URL, engine, metadata

#create an instance of FastAPI Class, name it app
app = FastAPI() #This app object will be used to define all your routes (URLs) for the CRUD operations.

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict it for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

#Connect to the database:
database = Database(DATABASE_URL)

#Creates tables in th database if they do not exist
metadata.create_all(engine)

# Item model defintion (for Validation with pydantic)
class Item(BaseModel): # for basic explanation back to main copy.py
    name: str
    description: str = None

#Initialize database connection on startup
@app.on_event("startup")
async def startup():
    await database.connect()

#Close Database connection on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# CRUD Routes

#Get All items
@app.get("/items", response_model=List[Item])
async def get_items():
    try:
        query = items_table.select()  # select all items from the table
        results = await database.fetch_all(query)  # Fetch all results
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

#Create a new Item
@app.post("/items", response_model=List[Item])
async def create_item(item: Item):
    try:
        query = items_table.insert().values(name=item.name, description=item.description)
        await database.execute(query)
        return await get_items()  # Call the get_items to return the list after insertion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


#Update an existing item
@app.put("/items/{item_name}", response_model=Item)
async def update_item(item_name: str,item: Item):
    query = items_table.update().where(items_table.c.name == item_name).values(
        name = item.name,
        description = item.description
    )
    result = await database.execute(query) # Excecute the update query
    if result:
        return item # return the updated item
    raise HTTPException(status_code=404, detail=f"Item {item_name} Not Found")

#delete item
@app.delete("/items/{item_name}", response_model=dict)
async def delete_item(item_name: str):
    try:
        # Perform the delete operation
        query = items_table.delete().where(items_table.c.name == item_name)
        print(f"Executing query: {query}")  # Log the query being executed
        
        result = await database.execute(query)  # Execute the delete query
        
        # Check if the item was deleted
        if result:
            return {"message": f"Item {item_name} deleted successfully"}
        else:
            print(f"Item with name '{item_name}' not found.")  # Log when item is not found
            raise HTTPException(status_code=404, detail=f"Item with name '{item_name}' not found")
    except Exception as e:
        # Log any unexpected error
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

