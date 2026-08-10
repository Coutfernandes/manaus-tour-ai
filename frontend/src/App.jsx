import React, { useState, useEffect } from 'react';
import { Send, FileText, Bot, CheckCircle2, BookOpen, Sparkles } from 'lucide-react';

// De:
// const API_BASE_URL = 'http://localhost:8000';

// Para:
const API_BASE_URL = 'https://manaus-tour-ai-backend.vercel.app';

export default function App() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Olá! Eu sou o Manaus Tour AI, seu guia inteligente da capital amazônica.\n\nFui treinado com documentos locais sobre pontos turísticos, história, gastronomia e cultura de Manaus. Como posso te ajudar hoje?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState([]);
  const [sugestoes, setSugestoes] = useState([]);

  // Função para carregar sugestões do backend FastAPI
  const carregarSugestoes = async (ultimaPergunta = '') => {
    try {
      const url = ultimaPergunta
        ? `${API_BASE_URL}/api/sugestoes?ultima_pergunta=${encodeURIComponent(ultimaPergunta)}`
        : `${API_BASE_URL}/api/sugestoes`;

      const response = await fetch(url);
      const data = await response.json();
      if (data.sugestoes) setSugestoes(data.sugestoes);
    } catch (error) {
      console.error('Erro ao buscar sugestões:', error);
    }
  };

  useEffect(() => {
    carregarSugestoes();
  }, []);

  const handleSend = async (perguntaTexto) => {
    const textToSend = perguntaTexto || input;
    if (!textToSend.trim()) return;

    const newMessages = [...messages, { sender: 'user', text: textToSend }];
    setMessages(newMessages);
    if (!perguntaTexto) setInput('');
    setLoading(true);

    try {
      // Envio de mensagem no chat para o backend FastAPI
      const chatResponse = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pergunta: textToSend }),
      });

      const data = await chatResponse.json();

      setMessages([...newMessages, { sender: 'bot', text: data.resposta }]);
      if (data.fontes) setSources(data.fontes);
      
      // Atualiza as sugestões com base na pergunta recém-enviada
      carregarSugestoes(textToSend);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: 'bot', text: 'Erro ao conectar com o servidor. O backend FastAPI está rodando?' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#FCFAF1] text-[#0E2517] overflow-hidden">
      
      {/* 1. SIDEBAR ESQUERDA - VERDE #0E2517 */}
      <aside className="w-80 bg-[#0E2517] text-[#FCFAF1] p-6 hidden md:flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 mb-6">
            <div>
              <h1 className="font-bold text-lg leading-tight text-white">Manaus Tour AI</h1>
              <span className="text-xs text-emerald-300">Guia inteligente da Amazônia</span>
            </div>
          </div>

          <div className="flex items-center gap-2 bg-emerald-950/60 border border-emerald-800/50 p-3 rounded-lg mb-6 text-xs text-emerald-200">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Agente Online · RAG Ativo</span>
          </div>

          <h2 className="text-xs font-semibold text-emerald-400 tracking-wider uppercase mb-3">Documentos Ativos</h2>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded bg-white/10 border border-white/10 flex items-start gap-2">
              <FileText className="w-4 h-4 text-emerald-300 shrink-0 mt-0.5" />
              <div>
                <p className="font-medium text-white">pontos_turisticos.json</p>
                <p className="text-emerald-300/80 text-[10px]">Teatro, MUSA, Encontro das Águas, Ponta Negra</p>
              </div>
            </div>
          </div>
        </div>

        <div className="text-[11px] text-emerald-400/70 border-t border-white/10 pt-4">
          Alura & Oracle Next Education Challenge
        </div>
      </aside>

      {/* 2. CHAT CENTRAL - BEGE #FCFAF1 */}
      <main className="flex-1 flex flex-col h-full bg-[#FCFAF1]">
        <header className="px-8 py-5 border-b border-stone-300 bg-white/60 backdrop-blur-sm">
          <h2 className="font-bold text-lg text-[#0E2517]">Chat com o Agente</h2>
          <p className="text-xs text-stone-600">Perguntas sobre turismo, história e cultura de Manaus</p>
        </header>

        {/* ÁREA DE MENSAGENS */}
        <div className="flex-1 overflow-y-auto p-8 space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex gap-3 max-w-2xl ${msg.sender === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.sender === 'user' ? 'bg-[#0E2517] text-white' : 'bg-emerald-800 text-white'}`}>
                {msg.sender === 'user' ? 'U' : <Bot className="w-5 h-5" />}
              </div>
              <div className={`p-4 rounded-xl text-sm whitespace-pre-wrap shadow-sm border ${msg.sender === 'user' ? 'bg-[#0E2517] text-white border-[#0E2517]' : 'bg-white text-[#0E2517] border-stone-200'}`}>
                {msg.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-3 max-w-2xl">
              <div className="w-8 h-8 rounded-full bg-emerald-800 text-white flex items-center justify-center">
                <Bot className="w-5 h-5 animate-pulse" />
              </div>
              <div className="p-4 rounded-xl text-sm bg-white border border-stone-200 text-stone-600">
                Consultando base de dados...
              </div>
            </div>
          )}
        </div>

        {/* SUGESTÕES RÁPIDAS & INPUT */}
        <div className="p-6 bg-white/40 border-t border-stone-300 space-y-3">
          {sugestoes.length > 0 && (
            <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
              <span className="flex items-center gap-1 text-emerald-800 font-semibold shrink-0 text-[11px]">
                <Sparkles className="w-3.5 h-3.5" /> Sugestões:
              </span>
              {sugestoes.map((sugestao, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSend(sugestao)}
                  className="px-3 py-1.5 rounded-full bg-white border border-stone-300 text-[#0E2517] hover:border-[#0E2517] transition-colors shrink-0"
                >
                  {sugestao}
                </button>
              ))}
            </div>
          )}

          <div className="flex items-center gap-2 bg-white rounded-xl border border-stone-300 p-2 shadow-sm focus-within:border-[#0E2517] transition-colors">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Pergunte sobre Manaus... (Teatro Amazonas, passeios, etc)"
              className="flex-1 bg-transparent px-3 py-1 text-sm outline-none text-[#0E2517] placeholder:text-stone-400"
            />
            <button
              onClick={() => handleSend()}
              className="bg-[#0E2517] hover:bg-emerald-900 text-white p-2.5 rounded-lg transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </main>

      {/* 3. PAINEL DIREITO - FONTES RECUPERADAS */}
      <aside className="w-80 bg-white border-l border-stone-300 p-6 hidden lg:block">
        <div className="flex items-center gap-2 mb-1">
          <BookOpen className="w-5 h-5 text-emerald-800" />
          <h2 className="font-bold text-base text-[#0E2517]">Fontes Utilizadas</h2>
        </div>
        <p className="text-xs text-stone-600 mb-6">Trechos recuperados via RAG</p>

        {sources.length > 0 ? (
          <div className="space-y-3">
            {sources.map((src, i) => (
              <div key={i} className="p-3 rounded-lg bg-stone-50 border border-stone-200 text-xs">
                <p className="font-semibold text-emerald-900 mb-1">{src.arquivo}</p>
                <p className="text-stone-700">{src.trecho}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 px-4 border-2 border-dashed border-stone-200 rounded-xl">
            <BookOpen className="w-8 h-8 text-stone-300 mx-auto mb-2" />
            <p className="text-xs font-semibold text-stone-600">Nenhuma consulta ainda</p>
            <p className="text-[11px] text-stone-400 mt-1">Faça uma pergunta para ver os documentos consultados em tempo real.</p>
          </div>
        )}
      </aside>

    </div>
  );
}