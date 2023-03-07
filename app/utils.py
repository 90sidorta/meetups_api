from fastapi import status
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password: str):
    return pwd_context.hash(password)

def verify_pass(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)
