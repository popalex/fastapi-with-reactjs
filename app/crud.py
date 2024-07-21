from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.schemas import ItemCreate, ItemResponse
from app.models import PydanticObjectId

async def create_item(db: AsyncIOMotorClient, item: ItemCreate) -> ItemResponse:
    item_dict = item.model_dump()
    result = await db["database_name"]["items"].insert_one(item_dict)
    item_dict["id"] = result.inserted_id
    return ItemResponse(**item_dict)

async def get_item(db: AsyncIOMotorClient, id: str) -> ItemResponse:
    item = await db["database_name"]["items"].find_one({"_id": ObjectId(id)})
    if item:
        item["id"] = item["_id"]
        return ItemResponse(**item)

async def get_items(db: AsyncIOMotorClient, skip: int = 0, limit: int = 10) -> list[ItemResponse]:
    cursor = db["database_name"]["items"].find().skip(skip).limit(limit)
    items = []
    async for item in cursor:
        item["id"] = item["_id"]
        items.append(ItemResponse(**item))
    return items

async def update_item(db: AsyncIOMotorClient, id: str, item: ItemCreate) -> ItemResponse:
    result = await db["database_name"]["items"].update_one({"_id": ObjectId(id)}, {"$set": item.model_dump()})
    if result.modified_count:
        updated_item = await get_item(db, id)
        return updated_item

async def delete_item(db: AsyncIOMotorClient, id: str) -> int:
    result = await db["database_name"]["items"].delete_one({"_id": ObjectId(id)})
    return result.deleted_count
