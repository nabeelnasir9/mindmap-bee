from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List

class Embedding(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectId
    note_id: ObjectId
    embedding_vector: List[float]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
