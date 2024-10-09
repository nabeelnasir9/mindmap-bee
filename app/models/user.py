from pydantic import BaseModel, Field
from bson import ObjectId

class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    email: str
    password_hash: str
    profile_data: dict = {}

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
