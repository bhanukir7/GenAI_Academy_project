import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Loader2, TrendingUp, TrendingDown, Minus, Send, AlertCircle } from 'lucide-react';

type Classification = 'Bullish' | 'Bearish' | 'Neutral';

const App: React.FC = () => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Classification | null>(null);
  const [error, setError] = useState<{ message: string; suggestion?: string } | null>(null);

  const analyzeSentiment = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze sentiment');
      }

      const data = await response.json();
      
      if (!data || !data.classification) {
        throw new Error('The server returned an unexpected response format.');
      }

      setResult(data.classification as Classification);
    } catch (err: unknown) {
      console.error('Analysis Error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Something went wrong during analysis';
      setError({ 
        message: errorMessage,
        suggestion: 'Ensure the backend is running and GEMINI_API_KEY is set.'
      });
    } finally {
      setLoading(false);
    }
  };

  const [healthInfo, setHealthInfo] = useState<Record<string, unknown> | null>(null);

  const checkHealth = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      setHealthInfo(data);
    } catch (err) {
      console.error('Health Check Error:', err);
      setHealthInfo({ error: 'Could not reach health check endpoint' });
    }
  };

  const getResultStyles = (res: Classification) => {
    switch (res) {
      case 'Bullish':
        return { color: 'text-emerald-500', bg: 'bg-emerald-500/10', icon: TrendingUp };
      case 'Bearish':
        return { color: 'text-rose-500', bg: 'bg-rose-500/10', icon: TrendingDown };
      case 'Neutral':
        return { color: 'text-slate-500', bg: 'bg-slate-500/10', icon: Minus };
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        <div className="p-8 border-b border-slate-100 bg-slate-50/50">
          <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">
            Financial News Classifier
          </h1>
          <p className="text-slate-500 mt-1 text-sm">
            Analyze market sentiment using Gemini 3 Flash
          </p>
        </div>

        <div className="p-8 space-y-6">
          <div className="space-y-2">
            <label htmlFor="news" className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              News Snippet
            </label>
            <textarea
              id="news"
              className="w-full h-32 p-4 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all resize-none text-slate-700"
              placeholder="Enter a financial news headline or snippet..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </div>

          <button
            onClick={analyzeSentiment}
            disabled={loading || !input.trim()}
            className="w-full py-4 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                <Send className="w-4 h-4" />
                Analyze Sentiment
              </>
            )}
          </button>

          <AnimatePresence mode="wait">
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="p-4 bg-rose-50 border border-rose-100 rounded-xl flex flex-col gap-1 text-rose-600"
              >
                <div className="flex items-center gap-3">
                  <AlertCircle className="w-5 h-5 flex-shrink-0" />
                  <p className="text-sm font-semibold">{error.message}</p>
                </div>
                {error.suggestion && (
                  <p className="text-xs ml-8 opacity-80 italic">{error.suggestion}</p>
                )}
              </motion.div>
            )}

            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`p-8 rounded-2xl border flex flex-col items-center justify-center gap-4 ${getResultStyles(result).bg} ${getResultStyles(result).color.replace('text-', 'border-')}`}
              >
                <div className={`p-4 rounded-full ${getResultStyles(result).bg} ring-8 ring-white`}>
                  {React.createElement(getResultStyles(result).icon, { className: "w-8 h-8" })}
                </div>
                <div className="text-center">
                  <p className="text-xs font-semibold uppercase tracking-widest opacity-60">
                    Classification
                  </p>
                  <h2 className={`text-3xl font-bold ${getResultStyles(result).color}`}>
                    {result}
                  </h2>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="px-8 py-4 bg-slate-50 border-t border-slate-100 flex justify-between items-center">
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">System Online</span>
            </div>
            {healthInfo && (
              <div className="text-[8px] text-slate-400 font-mono bg-white p-1 rounded border border-slate-100 max-w-[200px] overflow-hidden text-ellipsis whitespace-nowrap">
                {JSON.stringify(healthInfo)}
              </div>
            )}
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className="text-[10px] text-slate-400 font-medium">Powered by Gemini 3 Flash</span>
            <button 
              onClick={checkHealth}
              className="text-[8px] text-slate-400 hover:text-slate-600 underline"
            >
              Check Health
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
