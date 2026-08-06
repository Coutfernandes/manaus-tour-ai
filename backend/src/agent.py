import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Carregar variáveis de ambiente (.env)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não configurada no .env!")

# 2. Função para carregar a base de dados dos pontos turísticos
def carregar_dados_turismo():
    caminho_arquivo = os.path.join("data", "pontos_turisticos.json")
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return json.dumps(dados, ensure_ascii=False, indent=2)

# 3. Criar o modelo Gemini via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=api_key,
    temperature=0.2  # Baixa temperatura para evitar invenções (alucinação)
)

# 4. Criar o Prompt do Agente Corporativo RAG
template_prompt = """
Você é o Assistente Virtual Oficial do "Manaus Tour".
Sua função é responder dúvidas de visitantes e colaboradores sobre os pontos turísticos de Manaus baseando-se EXCLUSIVAMENTE nas informações fornecidas no Contexto abaixo.

REGRAS OBRIGATÓRIAS:
1. Responda APENAS com base nos dados do CONTEXTO.
2. CITE O NOME DO PONTO TURÍSTICO que serviu de fonte para a sua resposta.
3. Se a informação solicitada NÃO estiver no contexto, responda exatamente:
   "Desculpe, não encontrei essa informação na minha base de dados sobre os pontos turísticos de Manaus."
4. Não invente ou adicione informações externas ao contexto.

---
CONTEXTO DE DADOS:
{contexto}
---

PERGUNTA DO USUÁRIO:
{pergunta}

RESPOSTA:
"""

prompt = ChatPromptTemplate.from_template(template_prompt)

# 5. Função principal para fazer perguntas ao Agente
def perguntar_ao_agente(pergunta_usuario: str):
    contexto = carregar_dados_turismo()
    
    # Conecta o Prompt ao Modelo LLM
    chain = prompt | llm
    
    # Executa enviando o contexto e a pergunta
    resposta = chain.invoke({
        "contexto": contexto,
        "pergunta": pergunta_usuario
    })
    
    # Trata o retorno para extrair o texto limpo
    conteudo = resposta.content
    if isinstance(conteudo, list) and len(conteudo) > 0 and 'text' in conteudo[0]:
        return conteudo[0]['text']
    return str(conteudo)

# 6. Função para gerar sugestões contextuais usando a mesma instância llm
def gerar_sugestoes_contextuais(ultima_pergunta: str = None) -> list[str]:
    """Gera 3 sugestões de perguntas relevantes usando o Gemini."""
    try:
        if ultima_pergunta:
            prompt_texto = f"""
            O usuário acabou de perguntar sobre turismo em Manaus: "{ultima_pergunta}".
            Gere exatamente 3 sugestões curtas de perguntas de acompanhamento que o usuário gostaria de fazer a seguir.
            Retorne APENAS as 3 perguntas, uma por linha, sem numeração, tópicos ou textos adicionais.
            """
        else:
            prompt_texto = """
            Gere 3 perguntas curtas e variadas que um turista faria sobre pontos turísticos, cultura ou gastronomia de Manaus.
            Retorne APENAS as 3 perguntas, uma por linha, sem numeração, tópicos ou textos adicionais.
            """

        # Usando llm.invoke com o LangChain
        resposta = llm.invoke(prompt_texto)
        texto_resposta = resposta.content if hasattr(resposta, 'content') else str(resposta)
        
        linhas = [linha.strip() for linha in texto_resposta.strip().split("\n") if linha.strip()]
        
        # Garante que teremos até 3 sugestões limpas
        return linhas[:3]
    except Exception as e:
        print(f"Erro ao gerar sugestões contextuais: {e}")
        # Fallback caso ocorra alguma falha na API
        return [
            "O que fazer no Centro Histórico?",
            "Quais são os pratos típicos de Manaus?",
            "Como agendar o passeio do Encontro das Águas?"
        ]

# TESTE INTERATIVO NO TERMINAL
if __name__ == "__main__":
    print("--- AGENTE MANAUS TOUR PRONTO ---")
    
    # Teste 1: Pergunta que EXISTE na base
    pergunta_1 = "Qual é o horário de visitação do Teatro Amazonas?"
    print(f"\nPergunta 1: {pergunta_1}")
    print(f"Resposta:\n{perguntar_ao_agente(pergunta_1)}")
    
    # Teste 2: Teste de sugestões contextuais
    print("\nTestando geração de sugestões:")
    sugestoes = gerar_sugestoes_contextuais(pergunta_1)
    for i, sug in enumerate(sugestoes, 1):
        print(f"{i}. {sug}")