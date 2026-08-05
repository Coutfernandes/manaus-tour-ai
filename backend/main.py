import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.agent import perguntar_ao_agente

app = FastAPI(title="Manaus Tour AI API")

# Libera o acesso para o React (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PerguntaRequest(BaseModel):
    pergunta: str

# Lista de sugestões baseadas no conteúdo da base RAG
SUGESTOES_BASE = [
    "Qual é o horário de visitação do Teatro Amazonas?",
    "Quanto custa para ir na Ponta Negra?",
    "Como funciona o Encontro das Águas?",
    "Como visitar o MUSA e qual o valor do ingresso?",
    "O que encontrar no Mercado Adolpho Lisboa?",
    "Quais são os pratos e bebidas típicas de Manaus?"
]

@app.post("/api/chat")
def chat(payload: PerguntaRequest):
    resposta = perguntar_ao_agente(payload.pergunta)
    return {
        "resposta": resposta,
        "fontes": [
            {
                "arquivo": "pontos_turisticos.json",
                "trecho": "Base de dados local sobre pontos turísticos de Manaus."
            }
        ]
    }

@app.get("/api/sugestoes")
async def obter_sugestoes():
    # Retorna 3 sugestões aleatórias a cada chamada
    sugestoes_aleatorias = random.sample(SUGESTOES_BASE, k=min(3, len(SUGESTOES_BASE)))
    return {"sugestoes": sugestoes_aleatorias}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)