from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TipoCombustivel(str, Enum):
    GASOLINA = "Gasolina"
    ETANOL = "Etanol"
    DIESEL = "Diesel"
    FLEX = "Flex"
    ELETRICO = "Elétrico"
    HIBRIDO = "Híbrido"


class AutomovelBase(BaseModel):
    marca: Optional[str] = Field(..., example="Toyota", description="Marca do automóvel.")
    modelo: Optional[str] = Field(
        ..., example="Corolla", description="Modelo específico do automóvel."
    )
    ano: Optional[int] = Field(
        ...,
        ge=1900,
        le=2100,
        example=2023,
        description="Ano de fabricação do automóvel.",
    )
    cor: Optional[str] = Field(..., example="Preto", description="Cor predominante do automóvel.")
    tipo_combustivel: TipoCombustivel = Field(
        ...,
        example=TipoCombustivel.FLEX,
        description="Tipo de combustível que o automóvel utiliza.",
    )
    quilometragem: Optional[float] = Field(
        ..., ge=0, example=50000.5, description="Quilometragem atual do automóvel."
    )
    numero_portas: Optional[int] = Field(
        ...,
        ge=2,
        le=5,
        example=4,
        description="Número de portas do automóvel (ex: 2, 3, 4, 5).",
    )
    placa: Optional[str] = Field(
        None,
        pattern=r"^[A-Z]{3}[ -]?\d[A-Z\d]?\d{2}$",
        example="ABC1D23",
        description="Placa do automóvel (formato Mercosul ou antigo). Opcional.",
    )
    chassi: Optional[str] = Field(
        ...,
        pattern=r"^[0-9A-Z]{17}$",
        example="9BWZZZ5X0JP000001",
        description="Número de chassi do automóvel (17 caracteres alfanuméricos).",
    )
    codigo_fipe: Optional[str] = Field(
        ...,
        min_length=6,
        max_length=10,
        example="005370-1",
        description="Código FIPE do automóvel.",
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AutomovelCreate(AutomovelBase):
    pass


class AutomovelInDataBase(AutomovelBase):
    id: int = Field(
        ..., example=1, description="ID único do automóvel gerado pelo sistema."
    )
    created_at: datetime = Field(
        ...,
        example=datetime.now(),
        description="Data e hora da criação do dado no banco.",
    )

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)


class AutomovelFilter(BaseModel):
    marca: Optional[str] = Field(None, description="Filtrar por marca do automóvel.")
    modelo: Optional[str] = Field(
        None, description="Filtrar por modelo específico do automóvel."
    )
    ano_min: Optional[int] = Field(
        None, ge=1900, description="Filtrar por ano mínimo de fabricação."
    )
    ano_max: Optional[int] = Field(
        None, le=2100, description="Filtrar por ano máximo de fabricação."
    )
    tipo_combustivel: Optional[TipoCombustivel] = Field(
        None, description="Filtrar por tipo de combustível."
    )
    quilometragem_max: Optional[float] = Field(
        None, ge=0, description="Filtrar por quilometragem máxima."
    )
    numero_portas: Optional[int] = Field(
        None, ge=2, le=5, description="Filtrar por número de portas."
    )
    placa_parcial: Optional[str] = Field(
        None, description="Filtrar por parte da placa (case-insensitive, contém)."
    )
    codigo_fipe: Optional[str] = Field(None, description="Filtrar por código FIPE.")

    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)
