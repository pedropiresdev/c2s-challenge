FROM python:3.11-slim-bookworm

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv && \
    uv pip install . --system

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]