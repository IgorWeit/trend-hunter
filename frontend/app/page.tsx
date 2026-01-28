'use client';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function Home() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult('');
    setProgress(20);
    
    try {
      const response = await fetch('https://trend-hunter-api.onrender.com/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      setProgress(70);
      const data = await response.json();
      setResult(data.result);
      setProgress(100);
    } catch (error) {
      setResult('Ошибка при анализе.');
    } finally {
      setLoading(false);
    }
  };

  const viralScore = result.match(/Viral Score\s*\|\s*([\d/]+)/)?.[1] || '—';
  const hotCategory = result.match(/Товарная ниша\s*\|\s*([^|]+)/)?.[1]?.trim() || '—';

  return (
    <main className="min-h-screen bg-[#0f172a] text-white p-4 md:p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-10">
          <h1 className="text-3xl font-black tracking-tighter text-green-400">FAST<span className="text-white">MOSS</span> CLONE</h1>
          <div className="text-xs bg-green-500/10 text-green-400 px-3 py-1 rounded-full border border-green-500/20">Live Analysis Active</div>
        </div>
        
        <div className="bg-slate-800/50 p-6 rounded-2xl border border-slate-700 backdrop-blur-sm mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              className="flex-1 p-4 rounded-xl bg-slate-900 border border-slate-700 focus:border-green-500 focus:ring-1 focus:ring-green-500 outline-none transition-all"
              placeholder="Вставьте ссылку на канал..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="bg-green-600 hover:bg-green-500 text-white font-bold px-10 py-4 rounded-xl transition-all shadow-lg shadow-green-900/20 disabled:opacity-50"
            >
              {loading ? 'ANALYZING...' : 'RUN STRATEGY'}
            </button>
          </div>
          {loading && (
            <div className="mt-6 w-full bg-slate-700 h-1.5 rounded-full overflow-hidden">
              <div className="bg-green-500 h-full transition-all duration-1000" style={{ width: `${progress}%` }}></div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700">
            <p className="text-slate-400 text-xs uppercase tracking-widest font-bold mb-2">Viral Score Index</p>
            <p className="text-6xl font-black text-green-400 tracking-tighter">{viralScore}</p>
          </div>
          <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700">
            <p className="text-slate-400 text-xs uppercase tracking-widest font-bold mb-2">Dominant Category</p>
            <p className="text-2xl font-bold text-white leading-tight">{hotCategory}</p>
          </div>
        </div>

        <div className="bg-slate-800 rounded-2xl border border-slate-700 shadow-2xl overflow-hidden">
          <div className="border-b border-slate-700 p-4 bg-slate-800/50">
            <h3 className="text-sm font-bold uppercase tracking-widest text-slate-400">Market Intelligence Report</h3>
          </div>
          <div className="p-6 md:p-8 prose prose-invert prose-green max-w-none prose-table:border prose-table:rounded-xl">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown>
          </div>
        </div>
      </div>
    </main>
  );
}
