from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas.user_schema import SignupRequest, UserResponse
from app.utils.security import hash_password
from datetime import datetime
from app.utils.otp import generate_otp
from app.utils.email import send_otp_email

router = APIRouter(prefix="/auth", tags=["Auth"])
users = db["users"]

@router.post("/signup", response_model=UserResponse)
def signup(data: SignupRequest):
    if users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    otp, hashed_otp, expires_at = generate_otp()

    user = {
        "full_name": data.full_name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": None,
        "emailverified": False,
        "email_otp": hashed_otp,
        "email_otp_expires": expires_at,
        "created_at": datetime.utcnow()
    }

    result = users.insert_one(user)

    send_otp_email(data.email, otp)

    return {
        "id": str(result.inserted_id),
        "full_name": data.full_name,
        "email": data.email,
        "role": None,
        "emailverified": False
    }
