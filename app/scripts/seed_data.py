# your_fastapi_project/scripts/seed_data.py

import asyncio
import os
from datetime import datetime
from typing import List
from faker import Faker
from faker_vehicle import VehicleProvider
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.repository.models.automovel import Automovel, Base

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

fake = Faker('pt_BR')
fake.add_provider(VehicleProvider) # <--- Adiciona o provedor de veículos

def generate_fake_automovel_data(num_automoveis: int) -> List[Automovel]:
    automoveis = []
    for _ in range(num_automoveis):
        ano = fake.random_int(min=1990, max=datetime.now().year + 1) # Adicionado +1 para incluir o ano atual

        tipos_combustivel = ["Gasolina", "Etanol", "Diesel", "Flex", "Elétrico", "Híbrido"]
        tipo_combustivel = fake.random_element(elements=tipos_combustivel)

        letras = ''.join(fake.random_letters(length=3)).upper()
        numeros = str(fake.random_int(min=0, max=9))
        mercosul_num = str(fake.random_int(min=0, max=9))
        final_numeros = str(fake.random_int(min=0, max=99)).zfill(2) # Garante 2 dígitos
        placa = f"{letras}-{numeros}{mercosul_num}{final_numeros}"

        automoveis.append(
            Automovel(
                marca=fake.vehicle_make(),
                modelo=fake.vehicle_model(),
                ano=ano,
                cor=fake.color_name(),
                tipo_combustivel=tipo_combustivel,
                quilometragem=fake.random_int(min=0, max=200000),
                numero_portas=fake.random_element(elements=[2, 4]),
                placa=placa,
                chassi=fake.vin(),
                codigo_fipe=str(fake.random_int(min=100000, max=999999))
            )
        )
    return automoveis


async def insert_fake_data(num_automoveis: int):
    automoveis = generate_fake_automovel_data(num_automoveis)
    async with AsyncSessionLocal() as session:
        session.add_all(automoveis)
        await session.commit()
    print(f"Inseridos {num_automoveis} veículos falsos no banco de dados.")

# --- Execução Principal ---
async def main():
    try:
        print(f"Iniciando a inserção de {120} veículos falsos.")
        await insert_fake_data(120)
        print("Operação de seed concluída com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(main())