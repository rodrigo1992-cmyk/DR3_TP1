from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@router.get("/status")
async def read_status():
    return {"status": "Servidor funcionando"}

class UserResponse(BaseModel):
    username: str
    message: str

@router.get("/user/{username}", response_model=UserResponse)
async def get_user(username: str):
    return UserResponse(username= username, message= f"Bom dia {username}")