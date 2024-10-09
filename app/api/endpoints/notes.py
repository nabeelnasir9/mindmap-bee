from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.session import get_db
from pymongo.database import Database
from bson import ObjectId
from typing import List
from datetime import datetime
from app.core.auth import get_current_user
from app.utils.faiss import cluster_notes  # Import for clustering

router = APIRouter()


class NoteCreate(BaseModel):
    title: str
    content: str
    content_type: str  # 'text', 'drawing', 'image'
    status: str = "incomplete"


# Helper function to convert ObjectId to str
def note_serializer(note):
    note["_id"] = str(note["_id"])
    note["user_id"] = str(note["user_id"])
    return note


# Helper function to validate ObjectId
def validate_object_id(note_id: str):
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID format.")
    return ObjectId(note_id)


# Automatic clustering function
async def auto_cluster_notes(db: Database, user_id: str):
    """
    Automatically cluster user's notes and save the results to the database.

    Args:
        db (Database): Database connection.
        user_id (str): ID of the current user.
    """
    notes_collection = db.get_collection("notes")
    notes = list(notes_collection.find({"user_id": user_id}))
    if not notes:
        return {"clusters": "No notes available for clustering"}

    # Create clusters from notes using the enhanced clustering function
    clusters = cluster_notes(notes)

    # Update or create a cluster document in the database
    db.get_collection("clusters").update_one(
        {"user_id": user_id},
        {"$set": {"clusters": clusters, "updated_at": datetime.utcnow().isoformat()}},
        upsert=True,
    )


@router.get("/notes/cluster")
async def get_clusters(
    db: Database = Depends(get_db), current_user: str = Depends(get_current_user)
):
    clusters_collection = db.get_collection("clusters")
    user_clusters = clusters_collection.find_one({"user_id": current_user})
    if not user_clusters or "clusters" not in user_clusters:
        return {"clusters": "No clusters available"}
    return user_clusters["clusters"]


@router.post("/notes")
async def create_note(
    note_data: NoteCreate,
    db: Database = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    notes_collection = db.get_collection("notes")
    note_data_dict = note_data.dict()
    note_data_dict["user_id"] = current_user
    note_data_dict["created_at"] = datetime.utcnow().isoformat()
    note_data_dict["updated_at"] = note_data_dict["created_at"]
    note_id = notes_collection.insert_one(note_data_dict).inserted_id

    # Perform clustering after note creation
    await auto_cluster_notes(db, current_user)

    return {"note_id": str(note_id)}


@router.get("/notes")
async def get_all_notes(
    db: Database = Depends(get_db), current_user: str = Depends(get_current_user)
):
    notes_collection = db.get_collection("notes")
    notes = list(notes_collection.find({"user_id": current_user}))
    serialized_notes = [note_serializer(note) for note in notes]
    return serialized_notes


@router.get("/notes/{note_id}")
async def get_note(
    note_id: str,
    db: Database = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    note_id_obj = validate_object_id(note_id)
    notes_collection = db.get_collection("notes")
    note = notes_collection.find_one({"_id": note_id_obj, "user_id": current_user})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note_serializer(note)


@router.put("/notes/{note_id}")
async def update_note(
    note_id: str,
    note_data: NoteCreate,
    db: Database = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    note_id_obj = validate_object_id(note_id)
    notes_collection = db.get_collection("notes")
    update_data = note_data.dict()
    update_data["updated_at"] = datetime.utcnow().isoformat()
    update_result = notes_collection.update_one(
        {"_id": note_id_obj, "user_id": current_user}, {"$set": update_data}
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    # Perform clustering after note update
    await auto_cluster_notes(db, current_user)

    return {"message": "Note updated successfully"}


@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: str,
    db: Database = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    note_id_obj = validate_object_id(note_id)
    notes_collection = db.get_collection("notes")
    delete_result = notes_collection.delete_one(
        {"_id": note_id_obj, "user_id": current_user}
    )
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    # Perform clustering after note deletion
    await auto_cluster_notes(db, current_user)

    return {"message": "Note deleted successfully"}
