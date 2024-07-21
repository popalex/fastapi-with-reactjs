from pydantic import BaseModel
from app.models import PydanticObjectId

class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(ItemCreate):
    id: PydanticObjectId

