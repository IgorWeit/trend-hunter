'use client';
import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  // Имитация прогресса для индикатора
  const startProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prev) => (prev >= 90 ? 90 : prev + 10));
    }, 800);
    return interval;
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setResult('');
    const interval = startProgress();

    try {
      const response = await fetch('https://trend-hunter-api.onrender.com/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setResult(data.result);
      setProgress(100);
    } catch (error) {
      setResult('Ошибка при анализе данных.');
    } finally {
      clearInterval(interval);
      setLoading(false);
    }
  };

  // Извлечение данных для карточек из текста ответа (упрощенно)
  const viralScore = result.match(/Viral Score\s*\|\s*(\d+)/)?.[1] || '—';
  const hotCategory = result.match(/Товарная ниша\s*\|\s*([^|]+)/)?.[1]?.trim() || '—';

  return (
    <main className="min-h-screen bg-slate-900 text-white p-8 font-sans">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-green-400">FastMoss Analytics Clone</h1>
        
        {/* Input Section */}
        <div className="flex gap-4 mb-8">
          <input
            type="text"
            className="flex-1 p-3 rounded bg-slate-800 border border-slate-700 focus:border-green-500 outline-none"
            placeholder="Вставьте ссылку на TikTok канал или YouTube Shorts..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-green-600 hover:bg-green-500 px-8 py-3 rounded font-bold transition-all disabled:opacity-50"
          >
            {loading ? 'Анализ...' : 'АНАЛИЗИРОВАТЬ'}
          </button>
        </div>

        {/* Progress Bar */}
        {loading && (
          <div className="w-full bg-slate-800 h-2 rounded-full mb-8 overflow-hidden">
            <div 
              className="bg-green-500 h-full transition-all duration-500" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        )}

        {/* Dashboard Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
            <p className="text-slate-400 text-sm uppercase mb-2">Viral Score</p>
            <p className="text-5xl font-black text-green-400">{viralScore}/10</p>
          </div>
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
            <p className="text-slate-400 text-sm uppercase mb-2">Hot Category</p>
            <p className="text-2xl font-bold text-white truncate">{hotCategory}</p>
          </div>
        </div>

        {/* Analysis Result (Markdown Table Support via basic rendering) */}
        <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-inner overflow-x-auto whitespace-pre-wrap">
          {result ? (
            <div className="prose prose-invert max-w-none">
              {result}
            </div>
          ) : (
            <p className="text-slate-500 text-center">Результаты появятся здесь после завершения анализа...</p>
          )}
        </div>
      </div>
    </main>
  );
}
