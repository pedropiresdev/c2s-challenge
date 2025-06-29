# 🚗 API e Agente de Automóveis com FastAPI e Google Gemini

Este projeto é uma aplicação web e um assistente de terminal para gerenciar e consultar informações sobre automóveis. Ele combina uma API RESTful robusta, construída com **FastAPI** e **SQLAlchemy** (assíncrono com PostgreSQL), e um agente virtual interativo no terminal, impulsionado por uma **Large Language Model (LLM)** da **Google Gemini**.

---

## 🌟 Funcionalidades Principais

* **API RESTful Completa**: Gerencia automóveis com operações CRUD (Criar, Ler, Atualizar, Deletar).
* **Filtragem Avançada**: Endpoints de consulta de automóveis com múltiplos filtros (marca, modelo, ano, tipo de combustível, etc.), utilizando o padrão MCP (Model Context Protocol).
* **Banco de Dados Persistente**: Utiliza **PostgreSQL** para armazenamento de dados, acessado via **SQLAlchemy ORM** com drivers assíncronos (`asyncpg`).
* **Dockerização Completa**: A aplicação e o banco de dados são orquestrados com **Docker Compose**, garantindo um ambiente de desenvolvimento e produção consistente.
* **Agente Virtual no Terminal**: Um assistente conversacional que interage com o usuário, entende suas perguntas e consulta a API de automóveis para fornecer respostas, impulsionado pelo **Google Gemini**.
* **Gerenciamento de Dependências Moderno**: Utiliza `pyproject.toml` e `uv` para uma gestão de pacotes eficiente.
* **Testes Abrangentes**: Inclui testes de unidade/integração para o CRUD e os endpoints da API, utilizando Pytest com banco de dados SQLite em memória para isolamento.
* **Qualidade de Código**: Enforce o estilo de código com `Black` e `isort` via `pre-commit hooks`.

---

## 🛠️ Tecnologias Utilizadas

* **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
* **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/)
* **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (com `asyncpg` para async)
* **Gerenciamento de Pacotes**: [uv](https://github.com/astral-sh/uv)
* **LLM/Agente**: [Google Gemini](https://ai.google.dev/models/gemini) via [LangChain](https://www.langchain.com/) (`langchain-google-genai`, `langchain-community`)
* **Geração de Dados Falsos**: [Faker](https://faker.readthedocs.io/) e [faker-vehicle](https://pypi.org/project/faker-vehicle/)
* **Interface CLI**: [Rich](https://rich.readthedocs.io/)
* **Testes**: [Pytest](https://docs.pytest.org/) e [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) com [aiosqlite](https://pypi.org/project/aiosqlite/)
* **Formatação de Código**: [Black](https://github.com/psf/black) e [isort](https://pycqa.github.io/isort/)
* **Containerização**: [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

Certifique-se de ter instalado em sua máquina:

* [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) (recomendado) ou **Docker Engine** e **Docker Compose V2** (comando `docker compose` sem hífen).
* Uma chave de API do **Google Gemini**.
* (Opcional, para rodar scripts localmente fora do Docker) **Python 3.11** (o `uv` e `pyproject.toml` estão configurados para `~=3.11`).

### Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git) # Substitua pela URL do seu repositório
    cd seu-repositorio
    ```

2.  **Crie e configure o arquivo `.env`:**
    Na raiz do projeto, crie um arquivo chamado `.env` com as seguintes variáveis de ambiente. Substitua os valores entre `""` pelos seus.

    ```dotenv
    # Variáveis para o Banco de Dados PostgreSQL (Docker)
    DB_NAME="sua_database_name"
    DB_USER="seu_usuario_db"
    DB_PASSWORD="sua_senha_db"
    DATABASE_URL="postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}"

    # Chave da API Google Gemini
    GOOGLE_API_KEY="sua_chave_api_google_aqui"
    ```

### Rodando com Docker Compose (Recomendado)

Esta é a maneira mais fácil e consistente de rodar a aplicação completa (API + Banco de Dados).

1.  **Suba os serviços do Docker Compose:**
    Este comando construirá as imagens (se necessário) e iniciará os contêineres do FastAPI (`app`) e do PostgreSQL (`db`).

    ```bash
    docker compose up --build -d
    ```
    O flag `-d` executa os contêineres em segundo plano.

2.  **Aguarde o banco de dados estar pronto:**
    O serviço `db` pode levar alguns segundos para iniciar completamente.

3.  **Crie as tabelas no banco de dados:**
    Execute este comando para criar as tabelas a partir dos seus modelos SQLAlchemy. Isso deve ser feito **apenas uma vez** ou quando houver alterações nos modelos.

    ```bash
    docker compose exec app python scripts/create_tables.py
    ```

4.  **Popule o banco de dados com dados falsos (opcional):**
    Para ter dados para testar a API e o agente, popule o banco de dados.

    ```bash
    docker compose exec app python scripts/seed_data.py
    ```

5.  **Acesse a API e a Documentação:**
    Sua API estará acessível em: `http://localhost:8000`
    A documentação interativa (Swagger UI) está em: `http://localhost:8000/docs`
    A documentação Redoc está em: `http://localhost:8000/redoc`

6.  **Interaja com o Agente Virtual no Terminal:**
    Para iniciar o agente CLI:

    ```bash
    docker compose exec -it app python app/cli/cli.py
    ```
    * `exec -it app`: Executa o comando no contêiner `app` de forma interativa.

    Você poderá então digitar suas perguntas e interagir com o assistente. Para sair, digite `sair`.

      - Solicite busca de veículos
   
      - Passe informações como `marca ford ano 2016`
   
      - Exemplo de retorno:


            Olá! Encontrei duas ótimas opções da Ford, ano 2016, em nosso estoque. Veja os detalhes:                                                                                                                                │
           │                                                                                                                                                                                                                         │
           │ 1.  **Ford Convertible 2016**                                                                                                                                                                                           │
           │     *   **Cor:** Vermelho enegrecido                                                                                                                                                                                    │
           │     *   **Combustível:** Flex                                                                                                                                                                                           │
           │     *   **Quilometragem:** 81.804 km                                                                                                                                                                                    │
           │     *   **Portas:** 2                                                                                                                                                                                                   │
           │     *   **Placa:** IUL-5058                                                                                                                                                                                             │
           │                                                                                                                                                                                                                         │
           │ 2.  **Ford Genesis Coupe 2016**                                                                                                                                                                                         │
           │     *   **Cor:** Bege                                                                                                                                                                                                   │
           │     *   **Combustível:** Híbrido                                                                                                                                                                                        │
           │     *   **Quilometragem:** 194.227 km                                                                                                                                                                                   │
           │     *   **Portas:** 4                                                                                                                                                                                                   │
           │     *   **Placa:** WBJ-5483                                                                                                                                                                                             │
           │                                                                                                                                                                                                                         │
           │ Algum desses modelos te interessa? Posso fornecer mais detalhes ou agendar uma visita 

7.  **Para derrubar os serviços:**
    Quando terminar, você pode parar e remover os contêineres:

    ```bash
    docker compose down
    ```
    Para remover também os dados persistentes do banco de dados (volume `pg_data`), use:
    ```bash
    docker compose down -v
    ```

---

## 🧪 Rodando Testes

Você pode executar os testes da aplicação para garantir que tudo está funcionando como esperado.

1.  **Garanta que o ambiente Docker está de pé (`docker compose up -d`).**
2.  **Execute os testes dentro do contêiner `app`:**
    ```bash
    docker compose exec app pytest
    ```

---

## 🎨 Formatação de Código (Pre-commit Hooks)

O projeto está configurado para usar `Black` e `isort` para formatação automática de código através de `pre-commit hooks`.

1.  **Instale os ganchos Git (uma única vez):**
    ```bash
    docker compose exec app pre-commit install
    ```
2.  **Formate o código:**
    Ao fazer `git commit`, o `Black` e o `isort` serão executados automaticamente nos arquivos modificados. Se eles alterarem o código, o commit será abortado e você precisará adicionar as mudanças formatadas (`git add .`) e tentar o commit novamente.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.