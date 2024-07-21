from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models import Item
from app.schemas import ItemCreate, ItemResponse
from app.database import get_database
from app.crud import create_item, get_item, get_items, update_item, delete_item
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/items/", response_model=ItemResponse)
async def create_item_endpoint(item: ItemCreate, db: AsyncIOMotorClient = Depends(get_database)):
    return await create_item(db, item)

@app.get("/items/{id}", response_model=ItemResponse)
async def read_item(id: str, db: AsyncIOMotorClient = Depends(get_database)):
    item = await get_item(db, id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items/", response_model=list[ItemResponse])
async def read_items(skip: int = 0, limit: int = 10, db: AsyncIOMotorClient = Depends(get_database)):
    return await get_items(db, skip=skip, limit=limit)

@app.put("/items/{id}", response_model=ItemResponse)
async def update_item_endpoint(id: str, item: ItemCreate, db: AsyncIOMotorClient = Depends(get_database)):
    updated_item = await update_item(db, id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{id}", response_model=dict)
async def delete_item_endpoint(id: str, db: AsyncIOMotorClient = Depends(get_database)):
    deleted_count = await delete_item(db, id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
