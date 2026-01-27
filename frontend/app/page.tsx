"use client";
import React, { useState } from 'react';
import dynamic from 'next/dynamic'; // <--- Магия Next.js
import { Search, Loader2, Sparkles, TrendingUp, BarChart3 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

// --- ИМПОРТИРУЕМ ГРАФИК БЕЗ SSR (Server Side Rendering) ---
// Это полностью убивает ошибку width(-1), так как график грузится только в браузере
const TrendChart = dynamic(() => import('./TrendChart'), { 
  ssr: false,
  loading: () => <div className="h-[400px] flex items-center justify-center text-slate-500">Загрузка графика...</div>
});

// ВАШ АДРЕС БЭКЕНДА
const BACKEND_URL = 'https://trend-backend-6fsl.onrender.com';

export default function Home() {
  // --- STATE ---
  const [compareInput, setCompareInput] = useState('');
  const [chartData, setChartData] = useState<any[]>([]);
  const [compareLoading, setCompareLoading] = useState(false);
  const [compareStatus, setCompareStatus] = useState('');

  const [aiCategory, setAiCategory] = useState('');
  const [aiResult, setAiResult] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  // --- ЛОГИКА 1: ГРАФИКИ ---
  const handleCompare = async () => {
    if (!compareInput) return;
    
    setCompareLoading(true);
    setCompareStatus('Загружаю данные из Google Trends...');
    setChartData([]); 

    try {
      const keywords = compareInput.split(',').map(k => k.trim()).filter(k => k);
      if (keywords.length > 5) {
        alert("Максимум 5 слов!");
        setCompareLoading(false);
        return;
      }

      const response = await fetch(`${BACKEND_URL}/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keywords: keywords }),
      });

      const data = await response.json();

      if (data.status === 'success') {
         setChartData(data.data);
         setCompareStatus('✅ График построен!');
      } else {
        throw new Error(data.message);
      }
    } catch (error: any) {
      alert(`Ошибка: ${error.message}`);
      setCompareStatus('❌ Ошибка загрузки');
    } finally {
      setCompareLoading(false);
    }
  };

  // --- ЛОГИКА 2: AI ---
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
      alert(`Ошибка: ${error.message}`);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-4 md:p-10 flex flex-col items-center">
      <div className="w-full max-w-5xl">
        
        <h1 className="text-4xl md:text-6xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-12">
          TrendHunter AI Pro
        </h1>

        {/* --- СЕКЦИЯ ГРАФИКОВ --- */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl mb-12">
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="text-blue-400" size={28} />
            <h2 className="text-2xl font-bold">Битва Трендов</h2>
          </div>
          
          <p className="text-slate-400 mb-4">
            Введите темы через запятую (макс 5):
          </p>

          <div className="flex gap-3 mb-6">
            <input 
              type="text" 
              value={compareInput}
              onChange={(e) => setCompareInput(e.target.value)}
              placeholder="iPhone, Samsung, Xiaomi"
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 text-white outline-none focus:border-blue-500 transition-colors"
            />
            <button 
              onClick={handleCompare}
              disabled={compareLoading}
              className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all"
            >
              {compareLoading ? <Loader2 className="animate-spin" /> : <BarChart3 size={20} />}
              Сравнить
            </button>
          </div>

          {compareStatus && <div className="text-sm text-blue-400 mb-4 font-mono">{compareStatus}</div>}

          {/* ВСТАВЛЯЕМ НАШ НОВЫЙ "УМНЫЙ" КОМПОНЕНТ */}
          {chartData.length > 0 && (
            <div className="w-full mt-8 bg-slate-950/50 p-4 rounded-xl border border-slate-800">
               <TrendChart data={chartData} />
            </div>
          )}
        </div>

        {/* --- СЕКЦИЯ AI СТРАТЕГИИ --- */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 md:p-8 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <Sparkles className="text-emerald-400" size={28} />
            <h2 className="text-2xl font-bold">AI Стратегия</h2>
          </div>

          <div className="flex gap-3 mb-6">
            <input 
              type="text" 
              value={aiCategory}
              onChange={(e) => setAiCategory(e.target.value)}
              placeholder="Ниша (например: Fitness)"
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors"
            />
            <button 
              onClick={handleAiAnalyze}
              disabled={aiLoading}
              className="bg-emerald-600 hover:bg-emerald-500 px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all"
            >
              {aiLoading ? <Loader2 className="animate-spin" /> : <Search size={20} />}
              Анализ
            </button>
          </div>

          {aiResult && (
            <div className="prose prose-invert max-w-none border-t border-slate-800 pt-6 mt-6">
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