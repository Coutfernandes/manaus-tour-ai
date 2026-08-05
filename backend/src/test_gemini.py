import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Carrega a chave salva no arquivo .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(" ERRO: A chave GEMINI_API_KEY não foi encontrada no arquivo .env!")
else:
    print(" Chave detectada com sucesso! Conectando ao Gemini...")

    # 2. Inicializa com o modelo atualizado (gemini-2.5-flash)
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=api_key
    )

    # 3. Envia uma pergunta simples
    resposta = llm.invoke("Responda em uma frase: Qual a importância do Teatro Amazonas para a cidade de Manaus?")
    
    print("\n Resposta do Gemini:")
    print(resposta.content)