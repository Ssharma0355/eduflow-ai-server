from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: Optional[Literal["CLIENT", "EXPERT"]]

class RoleUpdateRequest(BaseModel):
    role: Literal["CLIENT", "EXPERT"]
