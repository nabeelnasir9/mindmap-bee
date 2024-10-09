from fastapi import APIRouter, Depends
from app.utils.faiss import cluster_notes
from app.db.session import get_db
from pymongo.database import Database
from app.core.auth import get_current_user  # Import the get_current_user dependency

router = APIRouter()


@router.get("/notes/cluster")
async def cluster_notes_endpoint(
    db: Database = Depends(get_db), current_user: str = Depends(get_current_user)
):
    notes_collection = db.get_collection("notes")

    # Only cluster notes that belong to the authenticated user
    notes = list(notes_collection.find({"user_id": current_user}))

    if not notes:
        return {"clusters": "No notes available for clustering"}

    clusters = cluster_notes(notes)
    return {"clusters": clusters}
