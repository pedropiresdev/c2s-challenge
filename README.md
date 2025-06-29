# c2s-challenge
Código de desafio técnico realizado para a C2S

## Executar o código localmente

### Executar o projeto FastAPI
        uv run uvicorn app.main:app --reload

### Executar o client do agente virtual
        python cli/cli.py

### Configurar Pré Commit
      uv pip install pre-commit
      pre-commit install
        
## Rodar testes
1. Solicite busca de veículos
2. Passe informações como `marca ford ano 2016`
3. Exemplo de retorno:

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
    
