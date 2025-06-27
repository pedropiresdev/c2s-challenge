from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.schemas.automovel_schemas import AutomovelCreate, AutomovelUpdate, AutomovelInDataBase
from app.repository.models.automovel import Automovel

class AutomovelCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_automoveis(self) -> List[AutomovelInDataBase]:
        result = await self.db_session.execute(select(Automovel))
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
        self.db_session.add(new_automovel_orm) # Adiciona ao stage da sessão
        await self.db_session.commit() # Salva no banco de dados
        await self.db_session.refresh(new_automovel_orm) # Atualiza o objeto com os dados gerados pelo DB (ex: id, created_at)
        return AutomovelInDataBase.model_validate(new_automovel_orm)

    async def update_automovel(self, automovel_id: int, automovel_update: AutomovelUpdate) -> Optional[AutomovelInDataBase]:
        # Primeiro, busca o automóvel existente
        automovel_orm = await self.db_session.get(Automovel, automovel_id)
        if not automovel_orm:
            return None

        # Atualiza os atributos do objeto ORM com os dados do Pydantic
        # exclude_unset=True garante que apenas os campos fornecidos sejam atualizados
        for key, value in automovel_update.model_dump(exclude_unset=True).items():
            setattr(automovel_orm, key, value)

        await self.db_session.commit()
        await self.db_session.refresh(automovel_orm)
        return AutomovelInDataBase.model_validate(automovel_orm)

    async def delete_automovel(self, automovel_id: int) -> bool:
        # Busca o automóvel para deletar
        automovel_to_delete = await self.db_session.get(Automovel, automovel_id)
        if not automovel_to_delete:
            return False

        await self.db_session.delete(automovel_to_delete)
        await self.db_session.commit()
        return True
