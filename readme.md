# 🌿 Manaus Tour AI — Guia Turístico Inteligente da Amazônia

![Vercel Status](https://img.shields.io/badge/Vercel-Deploy%20Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![React](https://img.shields.io/badge/React-18-61DAFB)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC)

> Agente virtual interativo baseado em RAG (Retrieval-Augmented Generation) para fornecer informações turísticas, históricas, gastronômicas e culturais sobre a cidade de Manaus de forma precisa e contextualizada.

---

## 🔗 Links Úteis

* 🌐 **Aplicação em Produção:** [Manaus Tour AI](https://manaus-tour-ai.vercel.app/)
* 🐙 **Repositório GitHub:** [manaus-tour-ai](https://github.com/Coutfernandes/manaus-tour-ai)
* 📊 **Quadro Kanban (Trello):** [Gerenciamento do Projeto](https://trello.com/invite/b/6a6a5394c539aa5845d27800/ATTI9d884159fe2d763dd1e845500f5dc90410FF18B3/manaus-tour)

---

## 📌 Descrição Geral do Projeto

O **Manaus Tour AI** é um assistente virtual criado para guiar turistas e moradores locais sobre os encantos da capital amazonense. 

Utilizando a técnica de **RAG (Retrieval-Augmented Generation)** alimentada pelo modelo de linguagem **Google Gemini**, o agente consulta dados curados sobre pontos turísticos (como o Teatro Amazonas, Encontro das Águas, MUSA, Ponta Negra, entre outros), pratos típicos e dicas locais antes de formular uma resposta. Isso garante respostas confiáveis, evitando "alucinações" do modelo de IA.

---

## 🏗️ Arquitetura da Solução

O sistema foi desenvolvido utilizando uma arquitetura desacoplada em duas camadas principais, ambas implantadas como Serverless na **Vercel**:

┌────────────────┐          HTTP / JSON          ┌─────────────────────────┐
│   Frontend     │ ───────────────────────────>  │    Backend (FastAPI)    │
│ (React + Vite) │ <───────────────────────────  │                         │
└────────────────┘   https://.../api/chat        └────────────┬────────────┘
│
┌─────────────────┴─────────────────┐
│                                   │
┌────────▼────────┐                 ┌────────▼────────┐
│ Base RAG Local  │                 │  Google Gemini  │
│ (JSON Curado)   │                 │     API Key     │
└─────────────────┘                 └─────────────────┘

1. **Frontend:** Interface moderna construída em React e Vite, estilizada com Tailwind CSS, responsável por gerenciar a conversa com o usuário e renderizar sugestões dinâmicas.
2. **Backend:** API REST em FastAPI rodando no ecossistema Python. Processa a requisição, busca o contexto no acervo documental local (`data/pontos_turisticos.json`) e aciona a API da Google para gerar a resposta enriquecida.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

### **Metodologia e Gestão**
* **Kanban no Trello:** Organização de tarefas, fluxo de trabalho (*A Fazer*, *Em Andamento*, *Concluído*) e acompanhamento de entregas.

### **Frontend**
* **React:** Biblioteca JavaScript para construção da interface de usuário.
* **Vite:** Bundler de alta performance.
* **Tailwind CSS:** Estilização utilitária moderna e responsiva.
* **Lucide React:** Biblioteca de ícones interativos.

### **Backend**
* **Python 3.10+:** Linguagem principal do servidor.
* **FastAPI:** Framework web moderno, rápido e assíncrono para construção das rotas.
* **Uvicorn:** Servidor ASGI para desenvolvimento e execução da API.
* **Google Generative AI SDK:** Integração com a LLM Gemini da Google.

### **Deploy e Infraestrutura**
* **Vercel:** Hospedagem Serverless do Frontend e Backend desacoplados.
* **Git & GitHub:** Controle de versão e histórico do código-fonte.

---

## 💡 Exemplos de Uso do Agente

### ❓ Perguntas Suportadas
* *"O que fazer no Teatro Amazonas?"*
* *"Como funciona o passeio para o Encontro das Águas?"*
* *"Qual é o melhor lugar para ver o pôr do sol em Manaus?"*
* *"Quais pratos típicos da gastronomia amazonense eu devo provar?"*

### 💬 Exemplo de Interação

> **Usuário:** *Qual a história do Teatro Amazonas e o horário de visitação?*  
>   
> **Manaus Tour AI 🤖:**  
> *O Teatro Amazonas é o principal símbolo do Ciclo da Borracha, inaugurado em 1896. Ele conta com uma arquitetura renascentista e uma cúpula composta por 36 mil peças nas cores da bandeira do Brasil.*  
>   
> *📍 **Localização:** Centro Histórico de Manaus.*  
> *⏰ **Visitação:** Aberto para visitas guiadas de terça a sábado, das 9h às 17h, e aos domingos das 9h às 13h.*

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Node.js (v18+)
* Python (v3.10+)
* Uma chave de API da Google Gemini (`GEMINI_API_KEY`)

---

### Clonar o Repositório
```bash
git clone [https://github.com/Coutfernandes/manaus-tour-ai.git](https://github.com/Coutfernandes/manaus-tour-ai.git)
cd manaus-tour-ai

👨‍💻 Desenvolvedor
Desenvolvido por Matheus Coutinho como parte do projeto de assistentes virtuais inteligentes com RAG e IA Generativa.
