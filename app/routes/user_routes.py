from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import db
from app.schemas.user_schema import RoleUpdateRequest, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])
users = db["users"]

@router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(user_id: str, data: RoleUpdateRequest):
    result = users.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": data.role}},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(result["_id"]),
        "full_name": result["full_name"],
        "email": result["email"],
        "role": result["role"]
    }
