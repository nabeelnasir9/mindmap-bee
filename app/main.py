from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, notes, chat, clustering, ocr, localization
from app.db.base import init_db

app = FastAPI(title="Note Taking App", description="API for managing notes with advanced features")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering routers
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(notes.router, prefix="/api/v1", tags=["Notes"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
# app.include_router(clustering.router, prefix="/api/v1", tags=["Clustering"])
app.include_router(ocr.router, prefix="/api/v1", tags=["OCR"])
app.include_router(localization.router, prefix="/api/v1", tags=["Localization"])

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Note Taking App API"}

# Run with uvicorn: uvicorn app.main:app --reload
