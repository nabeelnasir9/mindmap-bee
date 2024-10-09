from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import get_current_user
from app.db.session import get_db
from pymongo.database import Database
import openai  # Assuming GPT-4 API from OpenAI is being used
from app.core.config import settings
from pydantic import BaseModel

openai.api_key = "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"  # Replace with your OpenAI API key

router = APIRouter()

# 
class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_notes(
    chat_request: ChatRequest,
    # query: str,
    db: Database = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    query = chat_request.query
    clusters_collection = db.get_collection("clusters")
    user_clusters = clusters_collection.find_one({"user_id": current_user})

    if not user_clusters or "clusters" not in user_clusters:
        raise HTTPException(
            status_code=404, detail="No clustered notes available for chat."
        )

    # Extracting note content from clusters to use as context
    context = ""
    for cluster in user_clusters["clusters"].values():
        for note in cluster:
            context += f"Title: {note['title']}\nContent: {note['content']}\n\n"

    if not context:
        return {"response": "No relevant information available from your notes."}

    try:
        # Use GPT to answer based on the clustered notes
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that answers questions based on the provided user notes.",
                },
                {
                    "role": "user",
                    "content": f"Here are the notes: {context} \n\nUser's question: {query}",
                },
            ],
            max_tokens=150,
        )
        answer = response["choices"][0]["message"]["content"]

        # Store chat history
        chat_collection = db.get_collection("chats")
        chat_entry = {
            "user_id": current_user,
            "query": query,
            "response": answer,
            "created_at": datetime.utcnow().isoformat(),
        }
        chat_collection.insert_one(chat_entry)

        return {"response": answer}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in GPT-4 response: {str(e)}"
        )


@router.get("/chat/history")
async def get_chat_history(
    db: Database = Depends(get_db), current_user: str = Depends(get_current_user)
):
    chat_collection = db.get_collection("chats")
    chats = list(chat_collection.find({"user_id": current_user}).sort("created_at", -1))
    return [
        {
            "query": chat["query"],
            "response": chat["response"],
            "created_at": chat["created_at"],
        }
        for chat in chats
    ]
