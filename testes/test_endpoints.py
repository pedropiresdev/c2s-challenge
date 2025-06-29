import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.automovel_schemas import AutomovelCreate, TipoCombustivel


@pytest.mark.asyncio
async def test_create_automovel_endpoint(test_client: TestClient):
    """Testa o endpoint POST /automoveis/"""
    automovel_data = {
        "marca": "Hyundai",
        "modelo": "HB20",
        "ano": 2023,
        "cor": "Branco",
        "tipo_combustivel": "Flex",
        "quilometragem": 100.0,
        "numero_portas": 4,
        "placa": "XYZ1A23",
        "chassi": "9BWZZZ5X0JP000001",
        "codigo_fipe": "001002-3",
    }
    response = test_client.post("/automoveis/", json=automovel_data)

    assert response.status_code == 201
    created_automovel = response.json()
    assert created_automovel["id"] is not None
    assert created_automovel["marca"] == automovel_data["marca"]
    assert created_automovel["chassi"] == automovel_data["chassi"]
    assert "created_at" in created_automovel


@pytest.mark.asyncio
async def test_get_all_automoveis_endpoint(test_client: TestClient):
    """Testa o endpoint GET /automoveis/"""
    # Cria alguns dados para testar a listagem
    automovel_data_1 = {
        "marca": "VW",
        "modelo": "Gol",
        "ano": 2020,
        "cor": "Vermelho",
        "tipo_combustivel": "Flex",
        "quilometragem": 50000.0,
        "numero_portas": 4,
        "placa": "ABC1B23",
        "chassi": "ABCD1234EFG567890",
        "codigo_fipe": "001003-4",
    }
    automovel_data_2 = {
        "marca": "Fiat",
        "modelo": "Cronos",
        "ano": 2024,
        "cor": "Azul",
        "tipo_combustivel": "Gasolina",
        "quilometragem": 100.0,
        "numero_portas": 4,
        "placa": "CBA3D21",
        "chassi": "FGHI9876JKL543210",
        "codigo_fipe": "001004-5",
    }
    test_client.post("/automoveis/", json=automovel_data_1)
    test_client.post("/automoveis/", json=automovel_data_2)

    response = test_client.get("/automoveis/")
    assert response.status_code == 200
    automoveis = response.json()
    assert isinstance(automoveis, list)
    assert (
        len(automoveis) >= 2
    )  # Pode ter outros carros de testes anteriores se o DB não for isolado por completo


@pytest.mark.asyncio
async def test_get_automoveis_with_filters_endpoint(test_client: TestClient):
    """Testa o endpoint GET /automoveis/ com filtros."""
    # Garante que há dados para filtrar
    test_client.post(
        "/automoveis/",
        json={
            "marca": "Honda",
            "modelo": "Civic",
            "ano": 2022,
            "cor": "Preto",
            "tipo_combustivel": "Gasolina",
            "quilometragem": 25000.0,
            "numero_portas": 4,
            "placa": "HND1C22",
            "chassi": "CHAS0000000000001",
            "codigo_fipe": "005001-2",
        },
    )
    test_client.post(
        "/automoveis/",
        json={
            "marca": "Honda",
            "modelo": "HRV",
            "ano": 2023,
            "cor": "Branco",
            "tipo_combustivel": "Flex",
            "quilometragem": 10000.0,
            "numero_portas": 4,
            "placa": "HND2H23",
            "chassi": "CHAS0000000000002",
            "codigo_fipe": "005002-3",
        },
    )
    test_client.post(
        "/automoveis/",
        json={
            "marca": "BMW",
            "modelo": "X1",
            "ano": 2024,
            "cor": "Azul",
            "tipo_combustivel": "Diesel",
            "quilometragem": 5000.0,
            "numero_portas": 4,
            "placa": "BMW1X24",
            "chassi": "CHAS0000000000003",
            "codigo_fipe": "006001-4",
        },
    )

    response = test_client.get("/automoveis/?marca=Honda")
    assert response.status_code == 200
    filtered_automoveis = response.json()
    assert len(filtered_automoveis) == 2
    assert all(a["marca"] == "Honda" for a in filtered_automoveis)

    response = test_client.get("/automoveis/?ano_min=2023&tipo_combustivel=Flex")
    assert response.status_code == 200
    filtered_automoveis = response.json()
    assert len(filtered_automoveis) == 1
    assert filtered_automoveis[0]["modelo"] == "HRV"

    response = test_client.get("/automoveis/?quilometragem_max=12000")
    assert response.status_code == 200
    filtered_automoveis = response.json()
    assert len(filtered_automoveis) == 2  # HRV e X1
    assert all(a["quilometragem"] <= 12000 for a in filtered_automoveis)


@pytest.mark.asyncio
async def test_get_automovel_by_id_endpoint(test_client: TestClient):
    """Testa o endpoint GET /automoveis/{id}"""
    automovel_data = {
        "marca": "Nissan",
        "modelo": "Kicks",
        "ano": 2022,
        "cor": "Cinza",
        "tipo_combustivel": "Flex",
        "quilometragem": 30000.0,
        "numero_portas": 4,
        "placa": "NIS1K22",
        "chassi": "CHAS0000000000004",
        "codigo_fipe": "007001-5",
    }
    create_response = test_client.post("/automoveis/", json=automovel_data)
    automovel_id = create_response.json()["id"]

    response = test_client.get(f"/automoveis/{automovel_id}")
    assert response.status_code == 200
    fetched_automovel = response.json()
    assert fetched_automovel["id"] == automovel_id
    assert fetched_automovel["modelo"] == automovel_data["modelo"]

    response_not_found = test_client.get("/automoveis/99999")
    assert response_not_found.status_code == 404
    assert response_not_found.json() == {"detail": "Automóvel não encontrado"}


@pytest.mark.asyncio
async def test_update_automovel_endpoint(test_client: TestClient):
    """Testa o endpoint PUT /automoveis/{id}"""
    automovel_data = {
        "marca": "Hyundai",
        "modelo": "Creta",
        "ano": 2023,
        "cor": "Branco",
        "tipo_combustivel": "Flex",
        "quilometragem": 5000.0,
        "numero_portas": 4,
        "placa": "HYU1C23",
        "chassi": "CHAS0000000000005",
        "codigo_fipe": "008001-6",
    }
    create_response = test_client.post("/automoveis/", json=automovel_data)
    automovel_id = create_response.json()["id"]

    update_data = {"cor": "Vermelho", "quilometragem": 10000.0}
    response = test_client.put(f"/automoveis/{automovel_id}", json=update_data)
    assert response.status_code == 200
    updated_automovel = response.json()
    assert updated_automovel["id"] == automovel_id
    assert updated_automovel["cor"] == "Vermelho"
    assert updated_automovel["quilometragem"] == 10000.0

    response_not_found = test_client.put("/automoveis/99999", json=update_data)
    assert response_not_found.status_code == 404


@pytest.mark.asyncio
async def test_delete_automovel_endpoint(test_client: TestClient):
    """Testa o endpoint DELETE /automoveis/{id}"""
    automovel_data = {
        "marca": "Jeep",
        "modelo": "Renegade",
        "ano": 2021,
        "cor": "Verde",
        "tipo_combustivel": "Diesel",
        "quilometragem": 40000.0,
        "numero_portas": 4,
        "placa": "JEE1R21",
        "chassi": "CHAS0000000000006",
        "codigo_fipe": "009001-7",
    }
    create_response = test_client.post("/automoveis/", json=automovel_data)
    automovel_id = create_response.json()["id"]

    response = test_client.delete(f"/automoveis/{automovel_id}")
    assert response.status_code == 204

    response_get = test_client.get(f"/automoveis/{automovel_id}")
    assert response_get.status_code == 404
