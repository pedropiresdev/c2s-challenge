from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.automovel_schemas import AutomovelCreate, AutomovelUpdate, AutomovelInDataBase, AutomovelFilter, TipoCombustivel
from app.repository.models.automovel import Automovel

class AutomovelCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_automoveis(self, filters: AutomovelFilter = None) -> List[AutomovelInDataBase]:
        query = select(Automovel)

        if filters:
            if filters.marca:
                query = query.filter(Automovel.marca.ilike(f"%{filters.marca}%")) # Case-insensitive LIKE
            if filters.modelo:
                query = query.filter(Automovel.modelo.ilike(f"%{filters.modelo}%"))
            if filters.ano_min:
                query = query.filter(Automovel.ano >= filters.ano_min)
            if filters.ano_max:
                query = query.filter(Automovel.ano <= filters.ano_max)
            if filters.tipo_combustivel:
                query = query.filter(Automovel.tipo_combustivel == filters.tipo_combustivel)
            if filters.quilometragem_max:
                query = query.filter(Automovel.quilometragem <= filters.quilometragem_max)
            if filters.numero_portas:
                query = query.filter(Automovel.numero_portas == filters.numero_portas)
            if filters.placa_parcial:
                query = query.filter(Automovel.placa.ilike(f"%{filters.placa_parcial}%"))
            if filters.codigo_fipe:
                query = query.filter(Automovel.codigo_fipe == filters.codigo_fipe)

        result = await self.db_session.execute(query)
        automoveis_orm = result.scalars().all()
        return [AutomovelInDataBase.model_validate(auto) for auto in automoveis_orm]

    async def get_automovel_by_id(self, automovel_id: int) -> Optional[AutomovelInDataBase]:
        result = await self.db_session.execute(
            select(Automovel).filter(Automovel.id == automovel_id)
        )
        automovel_orm = result.scalars().first()
        if automovel_orm:
            return AutomovelInDataBase.model_validate(automovel_orm)
        return None

    async def create_automovel(self, automovel: AutomovelCreate) -> AutomovelInDataBase:
        new_automovel_orm = Automovel(**automovel.model_dump())
        self.db_session.add(new_automovel_orm)
        await self.db_session.commit()
        await self.db_session.refresh(new_automovel_orm)
        return AutomovelInDataBase.model_validate(new_automovel_orm)

    async def update_automovel(self, automovel_id: int, automovel_update: AutomovelUpdate) -> Optional[AutomovelInDataBase]:
        automovel_orm = await self.db_session.get(Automovel, automovel_id)
        if not automovel_orm:
            return None

        for key, value in automovel_update.model_dump(exclude_unset=True).items():
            setattr(automovel_orm, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(automovel_orm)
        return AutomovelInDataBase.model_validate(automovel_orm)

    async def delete_automovel(self, automovel_id: int) -> bool:
        automovel_to_delete = await self.db_session.get(Automovel, automovel_id)
        if not automovel_to_delete:
            return False

        await self.db_session.delete(automovel_to_delete)
        await self.db_session.commit()
        return True