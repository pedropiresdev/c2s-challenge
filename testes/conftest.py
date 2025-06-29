import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest_asyncio
import sys
import os

from app.core.config import AppSettings, settings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.repository.connection import Base, get_db_session
from app.repository.models.automovel import Automovel
from app.main import app
from app.view.automovel_crud import AutomovelCRUD
from app.schemas.automovel_schemas import AutomovelCreate, TipoCombustivel
from fastapi.testclient import TestClient

@pytest_asyncio.fixture(name="test_engine", scope="session")
async def test_engine_fixture():
    engine = create_async_engine(
        settings.DATABASE_URL_TEST,
        echo=False,
        poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(name="test_db_session", scope="function")
async def test_db_session_fixture(test_engine):
    async_session = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    # Abre a sessão aqui
    session = async_session()
    yield session
    await session.rollback()
    await session.close()


@pytest_asyncio.fixture(name="override_get_db_session", scope="function")
@pytest.mark.asyncio
async def override_get_db_session_fixture(test_db_session: AsyncSession):
    """
    Sobrescreve a dependência get_db_session do FastAPI para usar a sessão de teste.
    Deve produzir a sessão de teste como um gerador assíncrono.
    """
    yield test_db_session


@pytest.fixture(name="test_client", scope="function")
def test_client_fixture(override_get_db_session):
    """
    Cria um cliente de teste FastAPI com a dependência de DB sobrescrita.
    """
    async def _get_test_db():
        yield override_get_db_session

    app.dependency_overrides[get_db_session] = _get_test_db # <--- Alteração aqui
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}

@pytest_asyncio.fixture(name="automovel_crud", scope="function")
@pytest.mark.asyncio
async def automovel_crud_fixture(test_db_session: AsyncSession):
    return AutomovelCRUD(test_db_session)

@pytest.fixture(name="sample_automovel_data")
def sample_automovel_data_fixture():
    return AutomovelCreate(
        marca="Chevrolet",
        modelo="Onix",
        ano=2022,
        cor="Prata",
        tipo_combustivel=TipoCombustivel.FLEX,
        quilometragem=15000.0,
        numero_portas=4,
        placa="ABC1D23",
        chassi="1GNSK1359L3000001",
        codigo_fipe="004567-8"
    )