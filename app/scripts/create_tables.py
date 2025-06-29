import asyncio
import sys
import os

# Tive que adicionar o diretório raiz do projeto ao PATH para que as importações funcionem devido exception que estava
# ocorrendo dos imports. Essa solução veio de IA.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.repository.connection import engine, Base
from app.repository.models.automovel import Automovel # Tive que importar para o Base.metada conseguir encontrar

async def create_db_and_tables():
    print("Iniciando a criação de tabelas no banco de dados...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("Tabelas criadas com sucesso ou já existentes no banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao criar tabelas: {e}")

if __name__ == "__main__":
    asyncio.run(create_db_and_tables())