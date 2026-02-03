from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: Optional[Literal["CLIENT", "EXPERT"]] = None # Allow None for new users
    emailverified: bool = False # <--- ADD THIS FIELD

class RoleUpdateRequest(BaseModel):
    role: Literal["CLIENT", "EXPERT"]

class VerifyOTPRequest(BaseModel):
    otp: str