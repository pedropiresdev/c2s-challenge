import asyncio
import sys
import os
import random
from datetime import datetime
from faker import Faker
from faker.providers import automotive, color

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.repository.connection import get_db_session
from app.schemas.automovel_schemas import AutomovelCreate, TipoCombustivel
from app.view.automovel_crud import AutomovelCRUD
from sqlalchemy.exc import IntegrityError

NUM_VEICULOS_TO_GENERATE = 120

fake = Faker('pt_BR')
fake.add_provider(automotive)
fake.add_provider(color)


def generate_fipe_code():
    """Gera um código FIPE simulado no formato D+DDDDD-D."""
    group1 = str(random.randint(0, 999)).zfill(3)
    group2 = str(random.randint(0, 999)).zfill(3)
    last_digit = str(random.randint(0, 9))
    return f"{group1}{group2}-{last_digit}"[:10]

def generate_chassi():
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choices(chars, k=17))

def get_random_enum_value(enum_class):
    return random.choice(list(enum_class)).value

def generate_automovel_create_data() -> AutomovelCreate:
    data = {
        "marca": fake.vehicle_make(),
        "modelo": fake.vehicle_model(),
        "ano": random.randint(1990, datetime.now().year + 1),
        "cor": fake.color_name(),
        "tipo_combustivel": get_random_enum_value(TipoCombustivel),
        "quilometragem": round(random.uniform(0.0, 300000.0), 2),
        "numero_portas": random.choice([2, 4, 5]),
        "placa": fake.license_plate() if random.random() > 0.1 else None,
        "chassi": generate_chassi(),
        "codigo_fipe": generate_fipe_code(),
    }
    return AutomovelCreate(**data)

async def seed_automoveis_data(num_veiculos: int):
    """
    Popula a tabela de automóveis com dados fake.
    """
    print(f"Iniciando a inserção de {num_veiculos} veículos falsos.")
    inserted_count = 0
    attempts = 0
    max_attempts_per_vehicle = 5 # Tive que criar essa tentativa para o caso de vir chassi ou placa duplicados.

    async for db_session in get_db_session():
        crud = AutomovelCRUD(db_session)
        while inserted_count < num_veiculos and attempts < num_veiculos * max_attempts_per_vehicle:
            attempts += 1
            try:
                automovel_data = generate_automovel_create_data()
                await crud.create_automovel(automovel_data)
                inserted_count += 1
                if inserted_count % 10 == 0:
                    print(f"  -> Inseridos {inserted_count} veículos até agora...")
            except IntegrityError as e:
                print(f"  Erro de integridade (provável chassi/placa duplicado): {e}. Tentando novamente com novo dado...")
                await db_session.rollback()
            except Exception as e:
                print(f"  Ocorreu um erro inesperado: {e}")
                await db_session.rollback()
                break

        break

    print(f"\nConcluída a inserção. Total de {inserted_count} veículos inseridos com sucesso.")
    if inserted_count < num_veiculos:
        print(f"Atenção: Não foi possível inserir o número total desejado de veículos ({num_veiculos}).")


if __name__ == "__main__":
    asyncio.run(seed_automoveis_data(NUM_VEICULOS_TO_GENERATE))