import secrets # <--- Use secrets instead of random
import string
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp():
    # Generate a cryptographically secure 6-digit number
    otp = ''.join(secrets.choice(string.digits) for i in range(6))
    
    hashed_otp = pwd_context.hash(otp)
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    return otp, hashed_otp, expires_at

def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
    return pwd_context.verify(plain_otp, hashed_otp)