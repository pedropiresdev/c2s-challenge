from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.connection import get_db_session
from app.schemas.automovel_schemas import (AutomovelFilter, AutomovelInDataBase, AutomovelBase)
from app.view.automovel_crud import AutomovelCRUD

router = APIRouter()


# O Depends(get_db_session) injeta uma sessão de DB para cada requisição
@router.post(
    "/", response_model=AutomovelInDataBase, status_code=status.HTTP_201_CREATED
)
async def create_automovel_endpoint(
    automovel: AutomovelBase, db_session: AsyncSession = Depends(get_db_session)
):
    crud = AutomovelCRUD(db_session)
    return await crud.create_automovel(automovel)


@router.get("/", response_model=List[AutomovelInDataBase], operation_id="get_automoveis")
async def read_automoveis_endpoint(
    filters: AutomovelFilter = Depends(),
    db_session: AsyncSession = Depends(get_db_session),
):
    """
    Retorna uma lista de automóveis, com a opção de aplicar filtros.
    Exemplos de uso:
    - /automoveis/?marca=Toyota
    - /automoveis/?ano_min=2020&quilometragem_max=50000
    - /automoveis/?tipo_combustivel=Gasolina
    """
    crud = AutomovelCRUD(db_session)
    return await crud.get_all_automoveis(filters=filters)


@router.get("/{automovel_id}", response_model=AutomovelInDataBase)
async def read_automovel_endpoint(
    automovel_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    crud = AutomovelCRUD(db_session)
    automovel = await crud.get_automovel_by_id(automovel_id)
    if not automovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Automóvel não encontrado"
        )

    return automovel


@router.put("/{automovel_id}", response_model=AutomovelInDataBase)
async def update_automovel_endpoint(
    automovel_id: int,
    automovel_update: AutomovelBase,
    db_session: AsyncSession = Depends(get_db_session),
):
    crud = AutomovelCRUD(db_session)
    updated_automovel = await crud.update_automovel(automovel_id, automovel_update)
    if not updated_automovel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Automóvel não encontrado"
        )

    return updated_automovel


@router.delete("/{automovel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automovel_endpoint(
    automovel_id: int, db_session: AsyncSession = Depends(get_db_session)
):
    crud = AutomovelCRUD(db_session)
    if not await crud.delete_automovel(automovel_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Automóvel não encontrado"
        )
