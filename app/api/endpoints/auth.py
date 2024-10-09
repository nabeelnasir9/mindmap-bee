from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User
from pymongo.database import Database
from datetime import timedelta
from bson import ObjectId

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "password": "strongpassword123",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "nasirnabeel36@gmail.com",
                "password": "nasirnabeel36@gmail.com",
            }
        }


@router.post("/signup")
async def signup(user_data: UserCreate, db: Database = Depends(get_db)):
    user_collection = db.get_collection("users")
    user_exists = user_collection.find_one({"email": user_data.email.lower()})
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email.lower(),
        password_hash=hashed_password,
    )
    user_collection.insert_one(user.dict(by_alias=True))
    return {"message": "User created successfully"}


@router.post("/login")
async def login(user_data: UserLogin, db: Database = Depends(get_db)):
    user_collection = db.get_collection("users")
    user = user_collection.find_one({"email": user_data.email.lower()})

    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
