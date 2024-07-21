from typing import Annotated, Any, Callable, Optional

from bson import ObjectId
from fastapi import FastAPI
from pydantic import (BaseModel, BeforeValidator, ConfigDict, Field,
                      GetJsonSchemaHandler, WithJsonSchema)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PydanticObjectId = Annotated[str, 
                             BeforeValidator(str), 
                            #  WithJsonSchema({'type': 'string'}, mode='serialization')
                             ]


# class _ObjectIdPydanticAnnotation:
#     # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

#     @classmethod
#     def __get_pydantic_core_schema__(
#         cls,
#         _source_type: Any,
#         _handler: Callable[[Any], core_schema.CoreSchema],
#     ) -> core_schema.CoreSchema:
#         def validate_from_str(input_value: str) -> ObjectId:
#             print(f"****************** {input_value} ***************")
#             return ObjectId(input_value)

#         return core_schema.union_schema(
#             [
#                 # check if it's an instance first before doing any further work
#                 core_schema.is_instance_schema(ObjectId),
#                 core_schema.no_info_plain_validator_function(validate_from_str),
#             ],
#             serialization=core_schema.to_string_ser_schema(),
#         )

# PydanticObjectId = Annotated[
#     ObjectId, _ObjectIdPydanticAnnotation
# ]


class Item(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    name: str
    description: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        )

