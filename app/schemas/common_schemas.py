from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.automovel_schemas import AutomovelCreate, AutomovelUpdate, AutomovelInDataBase
from crud import automovel_crud # Importa o módulo CRUD

router = APIRouter()

@router.post("/", response_model=AutomovelInDataBase, status_code=status.HTTP_201_CREATED)
async def create_automovel_endpoint(automovel: AutomovelCreate):
    return automovel_crud.create_automovel(automovel)

@router.get("/", response_model=List[AutomovelInDataBase])
async def read_automoveis_endpoint():
    return automovel_crud.get_all_automoveis()

@router.get("/{automovel_id}", response_model=AutomovelInDataBase)
async def read_automovel_endpoint(automovel_id: int):
    automovel = automovel_crud.get_automovel_by_id(automovel_id)
    if not automovel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automóvel não encontrado")
    return automovel

@router.put("/{automovel_id}", response_model=AutomovelInDataBase)
async def update_automovel_endpoint(automovel_id: int, automovel: AutomovelUpdate):
    updated_automovel = automovel_crud.update_automovel(automovel_id, automovel)
    if not updated_automovel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automóvel não encontrado")
    return updated_automovel

@router.delete("/{automovel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automovel_endpoint(automovel_id: int):
    if not automovel_crud.delete_automovel(automovel_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Automóvel não encontrado")
    return