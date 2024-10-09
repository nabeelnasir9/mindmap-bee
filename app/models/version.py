from pydantic import BaseModel, Field
from bson import ObjectId

class Version(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    note_id: ObjectId
    version_number: int
    content: str
    timestamp: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
