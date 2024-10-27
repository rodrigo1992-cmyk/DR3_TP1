from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Optional, Dict
from datetime import datetime, timedelta


router = APIRouter()

#-------------------Exercício 2 -------------------
@router.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

#-------------------Exercícios 3 a 6 -------------------
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



#-------------------Exercícios 7 e 8 -------------------

class ReceiveModelUser(BaseModel):
    username: Annotated[str, Field(min_length=1)] 
    age: Annotated[int, Field(gt=0)] 


@router.post("/create-user")
async def create_user(user: ReceiveModelUser):
    bd_users[user.username] = {"username": user.username, "age": user.age}
    
    return ResponseModelUser(username= user.username, message= "Cadastro Realizado com Sucesso")




#-------------------Exercícios 9 e 10-------------------
bd_usersV2: Dict[int, Dict[str, str]] = {
    1: {"name": "Rodrigo", "age": 31},
    2: {"name": "Jonatas", "age": 32},
}

class ResponseModelId(BaseModel):
    name: str
    age: int


@router.get("/item/{item_id}", response_model=ResponseModelId)
async def get_item(item_id: int = Path(..., gt=0, description="item_id precisa ser um número inteiro positivo")):
    if item_id not in bd_usersV2:
        raise HTTPException(status_code=404, detail="ID não cadastrado")
    return ResponseModelId(**bd_usersV2[item_id])


@router.delete("/item/{item_id}")
async def delete_item(item_id: int = Path(..., gt=0, description="item_id precisa ser um número inteiro positivo")):
    if item_id not in bd_usersV2:
        raise HTTPException(status_code=404, detail="ID não cadastrado")
    deleted_item = bd_usersV2.pop(item_id)
    return {"message": f"Usuário'{deleted_item['name']}' removido do sistema."}


#-------------------Exercício 11 -------------------
# Modelo de dados para entrada
class ReceiveModelBday(BaseModel):
    name: str
    bday: datetime = Field(..., description="Data de aniversário no formato YYYY-MM-DD")

@router.post("/birthday")
async def calculate_birthday(dados: ReceiveModelBday):
    today = datetime.today().date()

    #Substitui o ano de nascimento pelo ano atual
    next_bday = dados.bday.replace(year = today.year).date()
    
    #Se o aniversário já passou este ano, soma 1 para jogar pro ano seguinte
    if next_bday < today:
        next_bday = next_bday.replace(year = today.year + 1)
        
    # Calcula a diferença em dias até o próximo aniversário
    delta = (next_bday - today).days
    return {
        "message": f"Faltam {delta} dias para o seu aniversário {dados.name}."
    }