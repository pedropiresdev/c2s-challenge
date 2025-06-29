from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.sql import func

from app.repository.connection import Base
from app.schemas.automovel_schemas import TipoCombustivel


class Automovel(Base):
    __tablename__ = "automoveis"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(String(30), nullable=False)
    tipo_combustivel = Column(
        Enum(TipoCombustivel, name="tipo_combustivel_enum"), nullable=False
    )
    quilometragem = Column(Float, nullable=False)
    numero_portas = Column(Integer, nullable=False)
    placa = Column(String(10), unique=True, nullable=True)
    chassi = Column(String(17), unique=True, nullable=False)
    codigo_fipe = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

    def __repr__(self):
        return (
            f"<Automovel(id={self.id}, modelo='{self.modelo}', chassi={self.chassi})>"
        )
