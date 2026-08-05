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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)