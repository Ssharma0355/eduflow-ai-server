from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas.user_schema import SignupRequest, UserResponse
from app.utils.security import hash_password
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])
users = db["users"]

@router.post("/signup", response_model=UserResponse)
def signup(data: SignupRequest):
    if users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    user = {
        "full_name": data.full_name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": None,
        "created_at": datetime.utcnow()
    }

    result = users.insert_one(user)
    user["_id"] = result.inserted_id

    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"]
    }
