"use client";
import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { Search, Loader2, Sparkles, TrendingUp, BarChart3, Youtube, Globe, ArrowUpRight } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

// График
const TrendChart = dynamic(() => import('./TrendChart'), { 
  ssr: false,
  loading: () => <div className="h-[400px] flex items-center justify-center text-slate-500">Загрузка графика...</div>
});

const BACKEND_URL = 'https://trend-hunter-api.onrender.com';

export default function Home() {
  const [compareInput, setCompareInput] = useState('');
  const [chartData, setChartData] = useState<any[]>([]);
  const [insights, setInsights] = useState<any>(null); // <-- НОВОЕ: Инсайты
  const [source, setSource] = useState('web'); // <-- НОВОЕ: web или youtube
  
  const [compareLoading, setCompareLoading] = useState(false);
  const [compareStatus, setCompareStatus] = useState('');

  const [aiCategory, setAiCategory] = useState('');
  const [aiResult, setAiResult] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  const handleCompare = async () => {
    if (!compareInput) return;
    setCompareLoading(true);
    setCompareStatus('Загружаю данные...');
    setChartData([]); 
    setInsights(null);

    try {
      const keywords = compareInput.split(',').map(k => k.trim()).filter(k => k);
      if (keywords.length > 5) {
        alert("Максимум 5 слов!");
        setCompareLoading(false);
        return;
      }

      // Отправляем запрос с указанием ИСТОЧНИКА (source)
      const response = await fetch(`${BACKEND_URL}/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keywords: keywords, source: source }),
      });

      const data = await response.json();

      if (data.status === 'success') {
         setChartData(data.data);
         setInsights(data.insights); // Сохраняем инсайты
         setCompareStatus('✅ Готово!');
      } else {
        throw new Error(data.message);
      }
    } catch (error: any) {
      alert(`Ошибка: ${error.message}`);
      setCompareStatus('❌ Ошибка');
    } finally {
      setCompareLoading(false);
    }
  };

  const handleAiAnalyze = async () => {
    if (!aiCategory) return;
    setAiLoading(true);
    setAiResult(null);

    try {
      const response = await fetch(`${BACKEND_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: aiCategory }),
      });

      const data = await response.json();
      if (data.status === 'success') {
        setAiResult(data.analysis);
      } else {
        throw new Error(data.message);
      }
    } catch (error: any) {
      setAiResult(`Ошибка AI: ${error.message}`);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-4 md:p-10 flex flex-col items-center">
      <div className="w-full max-w-6xl">
        
        <h1 className="text-4xl md:text-6xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-4">
          TrendHunter AI Pro
        </h1>
        <p className="text-center text-slate-500 mb-12">Global Market Intelligence Tool</p>

        {/* --- СЕКЦИЯ 1: ПОИСК ТРЕНДОВ --- */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl mb-12">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div className="flex items-center gap-3">
              <TrendingUp className="text-blue-400" size={28} />
              <h2 className="text-2xl font-bold">Анализ Спроса</h2>
            </div>
            
            {/* Переключатель Google / YouTube */}
            <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 self-start">
              <button 
                onClick={() => setSource('web')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${source === 'web' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                <Globe size={16} /> Google
              </button>
              <button 
                onClick={() => setSource('youtube')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${source === 'youtube' ? 'bg-red-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                <Youtube size={16} /> YouTube
              </button>
            </div>
          </div>

          <div className="flex flex-col md:flex-row gap-3 mb-6">
            <input 
              type="text" 
              value={compareInput}
              onChange={(e) => setCompareInput(e.target.value)}
              placeholder="Введите товары (например: Smart Watch, Neck Fan)..."
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-blue-500 transition-colors"
            />
            <button 
              onClick={handleCompare}
              disabled={compareLoading}
              className="bg-blue-600 hover:bg-blue-500 px-8 py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-all min-w-[150px]"
            >
              {compareLoading ? <Loader2 className="animate-spin" /> : <BarChart3 size={20} />}
              Найти
            </button>
          </div>

          {/* ГРАФИК */}
          {chartData.length > 0 && (
            <div className="w-full mt-8 bg-slate-950/50 p-4 rounded-xl border border-slate-800 mb-8">
               <TrendChart data={chartData} />
            </div>
          )}

          {/* --- НОВЫЙ БЛОК: ИНСАЙТЫ (TOP & RISING) --- */}
          {insights && Object.keys(insights).map((keyword) => (
            <div key={keyword} className="mt-8 border-t border-slate-800 pt-6">
              <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center gap-2">
                Инсайты для: <span className="text-blue-400">{keyword}</span>
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* TOP Queries */}
                <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800">
                  <h4 className="text-sm font-bold text-slate-400 mb-3 uppercase tracking-wider">🔥 Популярные запросы</h4>
                  <ul className="space-y-2">
                    {insights[keyword].top.length > 0 ? insights[keyword].top.map((item: any, i: number) => (
                      <li key={i} className="flex justify-between text-sm">
                        <span className="text-slate-300">{item.query}</span>
                        <span className="text-blue-500 font-mono">{item.value}</span>
                      </li>
                    )) : <li className="text-slate-600 text-sm">Нет данных</li>}
                  </ul>
                </div>

                {/* RISING Queries (Самое важное!) */}
                <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-emerald-500/10 blur-2xl rounded-full pointer-events-none"></div>
                  <h4 className="text-sm font-bold text-emerald-400 mb-3 uppercase tracking-wider flex items-center gap-2">
                    <ArrowUpRight size={16} /> Взрывной рост
                  </h4>
                  <ul className="space-y-2">
                    {insights[keyword].rising.length > 0 ? insights[keyword].rising.map((item: any, i: number) => (
                      <li key={i} className="flex justify-between text-sm">
                        <span className="text-slate-300">{item.query}</span>
                        <span className="text-emerald-400 font-mono font-bold">+{item.value}%</span>
                      </li>
                    )) : <li className="text-slate-600 text-sm">Нет растущих трендов</li>}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* --- СЕКЦИЯ 2: AI СТРАТЕГИЯ --- */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <Sparkles className="text-emerald-400" size={28} />
            <h2 className="text-2xl font-bold">AI Маркетолог</h2>
          </div>

          <div className="flex gap-3 mb-6">
            <input 
              type="text" 
              value={aiCategory}
              onChange={(e) => setAiCategory(e.target.value)}
              placeholder="Опишите нишу для анализа..."
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors"
            />
            <button 
              onClick={handleAiAnalyze}
              disabled={aiLoading}
              className="bg-emerald-600 hover:bg-emerald-500 px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all"
            >
              {aiLoading ? <Loader2 className="animate-spin" /> : <Search size={20} />}
              Стратегия
            </button>
          </div>

          {aiResult && (
            <div className="prose prose-invert max-w-none border-t border-slate-800 pt-6 mt-6 bg-slate-950/30 p-6 rounded-xl">
              <ReactMarkdown
                components={{
                  h1: ({node, ...props}) => <h1 className="text-xl font-bold text-blue-400 my-4" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-lg font-bold text-emerald-400 my-3" {...props} />,
                  strong: ({node, ...props}) => <strong className="text-white bg-slate-800 px-1 rounded" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc pl-5 space-y-2 text-slate-300" {...props} />,
                }}
              >
                {aiResult}
              </ReactMarkdown>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
