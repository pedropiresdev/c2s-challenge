import pytest

from app.schemas.automovel_schemas import (AutomovelCreate, TipoCombustivel, AutomovelBase)
from app.view.automovel_crud import AutomovelCRUD


@pytest.mark.asyncio
async def test_create_automovel(
    automovel_crud: AutomovelCRUD, sample_automovel_data: AutomovelCreate
):
    created_automovel = await automovel_crud.create_automovel(sample_automovel_data)

    assert created_automovel.id is not None
    assert created_automovel.marca == sample_automovel_data.marca
    assert created_automovel.modelo == sample_automovel_data.modelo
    assert created_automovel.ano == sample_automovel_data.ano
    assert created_automovel.created_at is not None


@pytest.mark.asyncio
async def test_get_automovel_by_id(
    automovel_crud: AutomovelCRUD, sample_automovel_data: AutomovelCreate
):
    created_automovel = await automovel_crud.create_automovel(sample_automovel_data)
    fetched_automovel = await automovel_crud.get_automovel_by_id(created_automovel.id)

    assert fetched_automovel is not None
    assert fetched_automovel.id == created_automovel.id
    assert fetched_automovel.modelo == created_automovel.modelo

    not_found_automovel = await automovel_crud.get_automovel_by_id(9999)
    assert not_found_automovel is None


@pytest.mark.asyncio
async def test_get_all_automoveis_no_filters(
    automovel_crud: AutomovelCRUD, sample_automovel_data: AutomovelCreate
):
    await automovel_crud.create_automovel(sample_automovel_data)
    await automovel_crud.create_automovel(
        AutomovelCreate(
            marca="Ford",
            modelo="Ka",
            ano=2020,
            cor="Branco",
            tipo_combustivel=TipoCombustivel.FLEX,
            quilometragem=30000.0,
            numero_portas=4,
            placa="XYZ9A87",
            chassi="1234567890ABCDEF1",
            codigo_fipe="001234-5",
        )
    )
    automoveis = await automovel_crud.get_all_automoveis()
    assert len(automoveis) == 2


@pytest.mark.asyncio
async def test_get_all_automoveis_with_filters(
    automovel_crud: AutomovelCRUD, sample_automovel_data: AutomovelCreate
):
    await automovel_crud.create_automovel(sample_automovel_data)
    await automovel_crud.create_automovel(
        AutomovelCreate(
            marca="Ford",
            modelo="Ka",
            ano=2020,
            cor="Branco",
            tipo_combustivel=TipoCombustivel.FLEX,
            quilometragem=30000.0,
            numero_portas=4,
            placa="XYZ9A87",
            chassi="1234567890ABCDEF1",
            codigo_fipe="001234-5",
        )
    )
    await automovel_crud.create_automovel(
        AutomovelCreate(
            marca="Chevrolet",
            modelo="Cruze",
            ano=2021,
            cor="Preto",
            tipo_combustivel=TipoCombustivel.GASOLINA,
            quilometragem=40000.0,
            numero_portas=4,
            placa="DEF1G23",
            chassi="ABCDEF12345678901",
            codigo_fipe="009876-5",
        )
    )

    filtered_automoveis = await automovel_crud.get_all_automoveis(marca="Chevrolet")
    assert len(filtered_automoveis) == 2
    assert all(a.marca == "Chevrolet" for a in filtered_automoveis)

    filtered_automoveis = await automovel_crud.get_all_automoveis(
        ano_min=2021, quilometragem_max=45000.0
    )
    assert len(filtered_automoveis) == 2  # Onix 2022 e Cruze 2021
    assert all(
        a.ano >= 2021 and a.quilometragem <= 45000.0 for a in filtered_automoveis
    )

    filtered_automoveis = await automovel_crud.get_all_automoveis(
        tipo_combustivel=TipoCombustivel.GASOLINA
    )
    assert len(filtered_automoveis) == 1
    assert filtered_automoveis[0].modelo == "Cruze"


@pytest.mark.asyncio
async def test_update_automovel(
    automovel_crud: AutomovelCRUD, sample_automovel_data: AutomovelCreate
):
    created_automovel = await automovel_crud.create_automovel(sample_automovel_data)

    update_data = AutomovelBase(cor="Azul", quilometragem=20000.0)
    updated_automovel = await automovel_crud.update_automovel(
        created_automovel.id, update_data
    )

    assert updated_automovel is not None
    assert updated_automovel.id == created_automovel.id
    assert updated_automovel.cor == "Azul"
    assert updated_automovel.quilometragem == 20000.0
    assert updated_automovel.marca == created_automovel.marca

    not_found_update = await automovel_crud.update_automovel(9999, update_data)
    assert not_found_update is None


@pytest.mark.asyncio
async def test_delete_automovel(
    automovel_crud: AutomovelCRUD, sample_automovel_data: AutomovelCreate
):
    created_automovel = await automovel_crud.create_automovel(sample_automovel_data)
    assert await automovel_crud.get_automovel_by_id(created_automovel.id) is not None

    deleted = await automovel_crud.delete_automovel(created_automovel.id)
    assert deleted is True
    assert await automovel_crud.get_automovel_by_id(created_automovel.id) is None

    not_found_delete = await automovel_crud.delete_automovel(9999)
    assert not_found_delete is False
