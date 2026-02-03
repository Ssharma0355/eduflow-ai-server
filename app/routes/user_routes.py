from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo import ReturnDocument
from datetime import datetime  # <--- ADD THIS IMPORT
from app.database import db
from app.schemas.user_schema import RoleUpdateRequest, UserResponse, VerifyOTPRequest
from app.utils.otp import verify_otp

router = APIRouter(prefix="/users", tags=["Users"])
users = db["users"]


router = APIRouter(prefix="/users", tags=["Users"])
users = db["users"]


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(user_id: str, data: RoleUpdateRequest):
    result = users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": data.role}},
        return_document=ReturnDocument.AFTER
    )

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(result["_id"]),
        "full_name": result["full_name"],
        "email": result["email"],
        "role": result["role"],
        "emailverified": result["emailverified"],
    }



@router.post("/{user_id}/verify-email-otp", response_model=UserResponse)
def verify_email_otp(user_id: str, data: VerifyOTPRequest):
    user = users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("emailverified"):
        raise HTTPException(status_code=400, detail="Email already verified")

    if not user.get("email_otp") or not user.get("email_otp_expires"):
        raise HTTPException(status_code=400, detail="OTP not found or already used")

    if datetime.utcnow() > user["email_otp_expires"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    if not verify_otp(data.otp, user["email_otp"]):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    result = users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {
            "$set": {"emailverified": True},
            "$unset": {"email_otp": "", "email_otp_expires": ""}
        },
        return_document=ReturnDocument.AFTER
    )

    return {
        "id": str(result["_id"]),
        "full_name": result["full_name"],
        "email": result["email"],
        "role": result["role"],
        "emailverified": result["emailverified"],
    }