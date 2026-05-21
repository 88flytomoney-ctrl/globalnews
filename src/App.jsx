import { useState, useEffect } from 'react';
import MarketTicker from './components/MarketTicker.jsx';
import NewsMatrix from './components/NewsMatrix.jsx';

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/globalnews/data/feed.json')
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-slate-400 animate-pulse text-lg">Loading globalnews...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-red-400">Error: {error}</div>
      </div>
    );
  }

  const { generatedAt, assets = [], news = [] } = data || {};

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      {/* Header */}
      <header className="border-b border-slate-700 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">🌐 globalnews</h1>
            <p className="text-xs text-slate-400">Live Market Data + World News</p>
          </div>
          <div className="text-right text-xs text-slate-400">
            <div>Last Updated</div>
            <div>{generatedAt ? new Date(generatedAt).toLocaleString('en-HK') : '—'}</div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
        {/* Market Ticker */}
        <section>
          <h2 className="text-sm font-semibold text-slate-400 mb-3 uppercase tracking-wider">
            📊 Market Data — 5D Trend
          </h2>
          <MarketTicker assets={assets} />
        </section>

        {/* News Matrix */}
        <section>
          <h2 className="text-sm font-semibold text-slate-400 mb-3 uppercase tracking-wider">
            📰 Global News Matrix
          </h2>
          <NewsMatrix news={news} />
        </section>
      </main>

      <footer className="border-t border-slate-700 mt-8 py-4 px-4">
        <div className="max-w-6xl mx-auto text-center text-xs text-slate-500">
          Data for reference only · News sources: BBC, TechCrunch · Market data: Yahoo Finance
        </div>
      </footer>
    </div>
  );
}
