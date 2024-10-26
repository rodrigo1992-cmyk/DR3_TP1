from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Optional



router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@router.get("/status")
async def read_status():
    return {"status": "Servidor funcionando"}

class ResponseModelUser(BaseModel):
    username: str
    message: str


bd_users = {
    "Rodrigo": {"username": "Rodrigo", "age": 32},
    "Jonatas": {"username": "Jonatas", "age": 33},
}

@router.get("/consult-user/{username}", response_model=ResponseModelUser)
async def consult_user(username: str):
    if username not in bd_users:
        raise HTTPException(status_code=404, detail="Usuário não cadastrado")
    return ResponseModelUser(username= username, message= f"Bom dia {username}")




class ReceiveModelUser(BaseModel):
    username: Annotated[str, Field(min_length=1)] 
    age: Annotated[int, Field(gt=0)] 


@router.post("/create-user")
async def create_user(user: ReceiveModelUser):
    bd_users[user.username] = {"username": user.username, "age": user.age}
    
    return ResponseModelUser(username= user.username, message= "Cadastro Realizado com Sucesso")




