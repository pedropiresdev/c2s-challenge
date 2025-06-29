import os
import httpx
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
from dotenv import load_dotenv

load_dotenv()


class AutomovelFilterToolSchema(BaseModel):
    marca: Optional[str] = Field(None, description="Marca do automóvel.")
    modelo: Optional[str] = Field(None, description="Modelo específico do automóvel.")
    ano_min: Optional[int] = Field(
        None, description="Ano mínimo de fabricação (ex: 2010)."
    )
    ano_max: Optional[int] = Field(
        None, description="Ano máximo de fabricação (ex: 2023)."
    )
    tipo_combustivel: Optional[str] = Field(
        None,
        description="Tipo de combustível (Gasolina, Etanol, Diesel, Flex, Elétrico, Híbrido).",
    )
    quilometragem_max: Optional[float] = Field(
        None, description="Quilometragem máxima."
    )
    numero_portas: Optional[int] = Field(
        None, description="Número de portas (ex: 2, 4, 5)."
    )
    placa_parcial: Optional[str] = Field(
        None, description="Parte da placa para busca (ex: ABC)."
    )
    codigo_fipe: Optional[str] = Field(None, description="Código FIPE do automóvel.")


class AutomovelAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_automoveis(self, filters: AutomovelFilterToolSchema) -> str:
        params = eval(filters) if isinstance(filters, str) else filters
        # params = filters.model_dump(exclude_none=True)
        try:
            response = await self.client.get(
                f"{self.base_url}/automoveis/", params=params
            )
            breakpoint()
            response.raise_for_status()
            automoveis = response.json()
            if automoveis:
                formatted_results = []
                for auto in automoveis[:5]:
                    formatted_results.append(
                        f"ID: {auto['id']}, Marca: {auto['marca']}, Modelo: {auto['modelo']}, "
                        f"Ano: {auto['ano']}, Cor: {auto['cor']}, Combustível: {auto['tipo_combustivel']}, "
                        f"KM: {auto['quilometragem']}, Portas: {auto['numero_portas']}, Placa: {auto['placa'] or 'N/A'}, "
                        f"Chassi: {auto['chassi']}, FIPE: {auto['codigo_fipe']}"
                    )
                return (
                    "Resultados encontrados:\n"
                    + "\n".join(formatted_results)
                    + (
                        f"\n...e mais {len(automoveis) - 5} resultados."
                        if len(automoveis) > 5
                        else ""
                    )
                )
            else:
                return "Nenhum automóvel encontrado com os filtros fornecidos."
        except httpx.RequestError as exc:
            return f"Ocorreu um erro de rede ao tentar acessar a API: {exc.request.url!r} - {exc}"
        except httpx.HTTPStatusError as exc:
            return f"Erro na resposta da API {exc.response.status_code}: {exc.response.text}"
        except Exception as e:
            return f"Erro inesperado ao consultar automóveis: {e}"


api_client = AutomovelAPIClient()

tools = [
    Tool(
        name="consultar_automoveis",
        func=lambda filters: asyncio.run(
            api_client.get_automoveis(filters)
        ),  # Wrapper síncrono para func
        coroutine_func=api_client.get_automoveis,
        description="""Útil para consultar automóveis no estoque.
        Use esta ferramenta para encontrar veículos com base em filtros como marca, modelo, ano (min/max),
        tipo de combustível, quilometragem máxima, número de portas, placa parcial, ou código FIPE.
        A entrada para esta ferramenta deve ser um objeto JSON com os filtros do automóvel,
        por exemplo: {"marca": "Toyota", "ano_min": 2020}.
        Os campos disponíveis para filtro são: marca, modelo, ano_min, ano_max, tipo_combustivel,
        quilometragem_max, numero_portas, placa_parcial, codigo_fipe.
        Para tipo_combustivel, os valores válidos são: Gasolina, Etanol, Diesel, Flex, Elétrico, Híbrido.
        """,
        args_schema=AutomovelFilterToolSchema,
    )
]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)

template = """
Você é um assistente virtual especializado em automóveis de uma concessionária.
Seu objetivo é ajudar o usuário a encontrar veículos e responder perguntas sobre eles.
Use as ferramentas disponíveis para consultar o estoque de veículos.
Quando o usuário pedir informações sobre veículos, use a ferramenta `consultar_automoveis`.
Sempre tente extrair os filtros mais específicos da pergunta do usuário para a ferramenta `consultar_automoveis`.
Se precisar de mais informações para refinar a busca (ex: "qual marca você prefere?", "qual o ano mínimo?"), peça ao usuário.
Se não encontrar veículos, informe ao usuário e sugira outros filtros.

Responda usando o formato Thought/Action/Observation/Final Answer.

Formato de Resposta Esperado:
Thought: Eu preciso usar uma ferramenta para responder à pergunta do usuário.
Action: consultar-automoveis
Action Input: {{chave: valor, outra_chave: outro_valor}}
Observation: O resultado da ferramenta aqui.
Thought: Com base na observação, posso formar uma resposta final.
Final Answer: Minha resposta final ao usuário.

Ferramentas disponíveis:
{tools}

Formato de resposta da ferramenta:
{tool_names}

Histórico da conversa:
{agent_scratchpad}

Pergunta do usuário: {input}
"""
prompt = PromptTemplate.from_template(template)


agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)


async def run_agent(input_text: str) -> str:
    response = await agent_executor.ainvoke({"input": input_text})
    return response["output"]
