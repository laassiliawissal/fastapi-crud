#here we are using a python list to store data
#import FastAPI from fastapi
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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

# a simple in-memory list to store the items
items = []

# Item model defintion (this is justa model for simplicity)
class Item(BaseModel): #FastAPI requires Pydantic models (BaseModel) for request and response validation*
    name: str
    description: str = None
#@app.get("/items") : sets up a route at /items that responds to GET requests.
#response_model=List[Item] tells fastAPI that the response will be a list of Item object
#get_items is the function that handles the request. It simply returns the list of items.
#      ||||||    SEE
#      vvvvvv    HERE

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.post("/items", response_model=List[Item])
async def create_item(item: Item):
    items.append(item)
    return items

@app.put("/items/{item_name}", response_model=Item)
async def update_item(item_name: str,item: Item):
    #find the item by its name
    for idx, existing_item in enumerate(items):
        if existing_item.name == item_name:
            items[idx] = item #
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_name} Not Found")

@app.delete("/items/{item_name}", response_model=Item)
async def delete_item(item_name: str):
    for idx, existing_item in enumerate(items):
        if existing_item.name == item_name:
            deleted_item = items.pop(idx)
            return deleted_item
