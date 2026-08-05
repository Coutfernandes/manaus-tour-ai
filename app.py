import streamlit as st
from backend.src.agent import perguntar_ao_agente

# ----------------------------------------------------
# 1. Configuração da página
# ----------------------------------------------------
st.set_page_config(
    page_title="Manaus Tour AI",
    page_icon=":compass:",
    layout="wide",
    initial_sidebar_state="expanded"
)

PALETA = {
    "verde_escuro": "#0E2517",
    "bege": "#FCFAF1",
    "branco": "#FFFFFF",
    "borda": "#EAE6DF",
}

MENSAGEM_BOAS_VINDAS = (
    "Olá! Eu sou o **Manaus Tour AI**, seu guia inteligente da capital amazônica.\n\n"
    "Fui treinado com documentos locais sobre pontos turísticos, história, gastronomia "
    "e cultura de Manaus. Pergunte-me sobre o Teatro Amazonas, o Encontro das Águas, "
    "pratos típicos, passeios pela floresta e muito mais.\n\n"
    "Como posso te ajudar hoje?"
)

DOCUMENTOS_ATIVOS = [
    {"nome": "pontos_turisticos_manaus.csv", "tamanho": "128 KB", "chunks": 42},
    {"nome": "guia_historico_teatro_amazonas.pdf", "tamanho": "3.4 MB", "chunks": 87},
    {"nome": "gastronomia_amazonica.pdf", "tamanho": "1.8 MB", "chunks": 54},
    {"nome": "encontro_das_aguas_geografia.pdf", "tamanho": "920 KB", "chunks": 23},
    {"nome": "cultura_indigena_manaus.csv", "tamanho": "64 KB", "chunks": 31},
]


def aplicar_estilo() -> None:
    """Injeta o CSS customizado com a paleta de cores do projeto."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {PALETA["bege"]};
            color: {PALETA["verde_escuro"]};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {PALETA["verde_escuro"]};
        }}

        section[data-testid="stSidebar"] * {{
            color: {PALETA["bege"]} !important;
        }}

        div[data-testid="stChatMessage"] {{
            background-color: {PALETA["branco"]};
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.04);
            border: 1px solid {PALETA["borda"]};
            color: {PALETA["verde_escuro"]};
        }}

        div[data-testid="stExpander"] {{
            background-color: {PALETA["branco"]};
            border: 1px solid {PALETA["borda"]};
            border-radius: 8px;
        }}

        .stButton>button {{
            background-color: {PALETA["verde_escuro"]};
            color: {PALETA["bege"]} !important;
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inicializar_estado() -> None:
    """Garante que as chaves usadas no session_state existam."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": MENSAGEM_BOAS_VINDAS}
        ]
    if "ultimas_fontes" not in st.session_state:
        st.session_state.ultimas_fontes = []


def renderizar_sidebar() -> None:
    with st.sidebar:
        st.title("Manaus Tour AI")
        st.caption("Guia inteligente da Amazônia")

        st.success("Agente online")
        st.divider()

        st.write(f"### Documentos ativos ({len(DOCUMENTOS_ATIVOS)})")
        for doc in DOCUMENTOS_ATIVOS:
            st.markdown(
                f"**{doc['nome']}**  \n`{doc['tamanho']} · {doc['chunks']} chunks`"
            )

        st.divider()
        if st.button("Limpar conversa"):
            st.session_state.messages = [
                {"role": "assistant", "content": MENSAGEM_BOAS_VINDAS}
            ]
            st.session_state.ultimas_fontes = []
            st.rerun()


def extrair_resposta_e_fontes(resultado):
    """
    Normaliza o retorno de perguntar_ao_agente.
    Aceita tanto uma string simples quanto um dict {"resposta": ..., "fontes": [...]}.
    """
    if isinstance(resultado, dict):
        resposta = resultado.get("resposta", "")
        fontes = resultado.get("fontes", [])
    else:
        resposta = resultado
        fontes = []
    return resposta, fontes


def renderizar_chat() -> None:
    st.subheader("Chat com o Agente")
    st.caption("Perguntas sobre turismo, história e cultura de Manaus")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    pergunta = st.chat_input(
        "Pergunte sobre Manaus... (Ex: passeios pela floresta, museus, praias de rio)"
    )
    if not pergunta:
        return

    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando base de conhecimento..."):
            try:
                resultado = perguntar_ao_agente(pergunta)
                resposta, fontes = extrair_resposta_e_fontes(resultado)
            except Exception as erro:
                resposta = (
                    "Não consegui consultar a base de conhecimento agora. "
                    "Tente novamente em instantes."
                )
                fontes = []
                st.error(f"Erro ao consultar o agente: {erro}")

            st.markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.session_state.ultimas_fontes = fontes


def renderizar_fontes() -> None:
    st.subheader("Fontes Utilizadas")
    st.caption("Trechos recuperados via RAG")

    fontes = st.session_state.ultimas_fontes
    if not fontes:
        st.info(
            "Nenhuma consulta ativa ainda.\n\n"
            "Faça uma pergunta e veja aqui de quais documentos a IA extraiu a resposta."
        )
    else:
        for fonte in fontes:
            titulo = fonte.get("documento", "Documento") if isinstance(fonte, dict) else str(fonte)
            trecho = fonte.get("trecho") if isinstance(fonte, dict) else None
            with st.expander(titulo):
                if trecho:
                    st.write(trecho)

    st.divider()
    st.markdown(
        "**Pipeline RAG**  \n`Query -> Embeddings -> Vector search -> Contexto -> Gemini -> Resposta`"
    )


def main() -> None:
    aplicar_estilo()
    inicializar_estado()
    renderizar_sidebar()

    col_chat, col_fontes = st.columns([2.5, 1])
    with col_chat:
        renderizar_chat()
    with col_fontes:
        renderizar_fontes()


if __name__ == "__main__":
    main()