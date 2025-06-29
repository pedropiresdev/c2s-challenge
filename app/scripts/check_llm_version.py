import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Erro: GOOGLE_API_KEY não encontrada no arquivo .env. Certifique-se de que está definida.")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)

async def list_gemini_models():
    #! Esse método foi gerado por IA
    """Lista os modelos Gemini disponíveis e suas capacidades."""
    print("Listando modelos Gemini disponíveis na sua conta...")
    try:
        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                print(f"Nome do Modelo: {model.name}")
                print(f"  Display Name: {model.display_name}")
                print(f"  Description: {model.description}")
                print(f"  Suporta generateContent: Sim")
                print("-" * 30)
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
        print("Verifique se sua GOOGLE_API_KEY está correta e tem permissões.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(list_gemini_models())