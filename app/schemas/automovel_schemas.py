from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List # Adicionado List
from enum import Enum

class TipoCombustivel(str, Enum):
    GASOLINA = "Gasolina"
    ETANOL = "Etanol"
    DIESEL = "Diesel"
    FLEX = "Flex"
    ELETRICO = "Elétrico"
    HIBRIDO = "Híbrido"

class AutomovelBase(BaseModel):
    marca: str = Field(..., example="Toyota", description="Marca do automóvel.")
    modelo: str = Field(..., example="Corolla", description="Modelo específico do automóvel.")
    ano: int = Field(..., ge=1900, le=2100, example=2023, description="Ano de fabricação do automóvel.")
    cor: str = Field(..., example="Preto", description="Cor predominante do automóvel.")
    tipo_combustivel: TipoCombustivel = Field(..., example=TipoCombustivel.FLEX, description="Tipo de combustível que o automóvel utiliza.")
    quilometragem: float = Field(..., ge=0, example=50000.5, description="Quilometragem atual do automóvel.")
    numero_portas: int = Field(..., ge=2, le=5, example=4, description="Número de portas do automóvel (ex: 2, 3, 4, 5).")
    placa: Optional[str] = Field(None, pattern=r"^[A-Z]{3}[ -]?\d[A-Z\d]?\d{2}$", example="ABC1D23", description="Placa do automóvel (formato Mercosul ou antigo). Opcional.")
    chassi: str = Field(..., pattern=r"^[0-9A-Z]{17}$", example="9BWZZZ5X0JP000001", description="Número de chassi do automóvel (17 caracteres alfanuméricos).")
    codigo_fipe: str = Field(..., min_length=6, max_length=10, example="005370-1", description="Código FIPE do automóvel.")


class AutomovelCreate(AutomovelBase):
    pass

class AutomovelUpdate(AutomovelBase):
    marca: Optional[str] = Field(None, example="Honda", description="Marca do automóvel.")
    modelo: Optional[str] = Field(None, example="Civic", description="Modelo específico do automóvel.")
    ano: Optional[int] = Field(None, ge=1900, le=2100, example=2022, description="Ano de fabricação do automóvel.")
    cor: Optional[str] = Field(None, example="Branco", description="Cor predominante do automóvel.")
    tipo_combustivel: Optional[TipoCombustivel] = Field(None, example=TipoCombustivel.GASOLINA, description="Tipo de combustível que o automóvel utiliza.")
    quilometragem: Optional[float] = Field(None, ge=0, example=60000.0, description="Quilometragem atual do automóvel.")
    numero_portas: Optional[int] = Field(None, ge=2, le=5, example=4, description="Número de portas do automóvel.")
    placa: Optional[str] = Field(None, pattern=r"^[A-Z]{3}[ -]?\d[A-Z\d]?\d{2}$", example="XYZ9A87", description="Placa do automóvel (formato Mercosul ou antigo).")
    chassi: Optional[str] = Field(None, pattern=r"^[0-9A-Z]{17}$", example="9BWZZZ5X0JP000002", description="Número de chassi do automóvel (17 caracteres alfanuméricos).")
    codigo_fipe: Optional[str] = Field(None, min_length=6, max_length=10, example="005370-2", description="Código FIPE do automóvel.")

class AutomovelInDataBase(AutomovelBase):
    id: int = Field(..., example=1, description="ID único do automóvel gerado pelo sistema.")
    created_at: datetime = Field(..., example=datetime.now(), description="Data e hora da criação do dado no banco.")

    class Config:
        from_attributes = True

class AutomovelFilter(BaseModel):
    marca: Optional[str] = Field(None, description="Filtrar por marca do automóvel.")
    modelo: Optional[str] = Field(None, description="Filtrar por modelo específico do automóvel.")
    ano_min: Optional[int] = Field(None, ge=1900, description="Filtrar por ano mínimo de fabricação.")
    ano_max: Optional[int] = Field(None, le=2100, description="Filtrar por ano máximo de fabricação.")
    tipo_combustivel: Optional[TipoCombustivel] = Field(None, description="Filtrar por tipo de combustível.")
    quilometragem_max: Optional[float] = Field(None, ge=0, description="Filtrar por quilometragem máxima.")
    numero_portas: Optional[int] = Field(None, ge=2, le=5, description="Filtrar por número de portas.")
    placa_parcial: Optional[str] = Field(None, description="Filtrar por parte da placa (case-insensitive, contém).")
    codigo_fipe: Optional[str] = Field(None, description="Filtrar por código FIPE.")

    class Config:
        use_enum_values = True
