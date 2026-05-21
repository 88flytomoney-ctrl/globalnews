const CATEGORY_LABELS = {
  WORLD: '🌍 WORLD',
  BUSINESS: '💼 BUSINESS',
  TECH: '💻 TECH',
};

function NewsCard({ item }) {
  const snippet = item.snippet || item.description || '';
  const shortSnippet = snippet.length > 120 ? snippet.slice(0, 120) + '…' : snippet;

  return (
    <div className="bg-slate-800 rounded-lg p-4 flex flex-col gap-2">
      <a
        href={item.link}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sm font-medium text-slate-100 hover:text-cyan-400 leading-snug line-clamp-3 transition-colors"
      >
        {item.title}
      </a>
      {shortSnippet && (
        <p className="text-xs text-slate-400 leading-relaxed">{shortSnippet}</p>
      )}
      <a
        href={item.link}
        target="_blank"
        rel="noopener noreferrer"
        className="text-xs text-cyan-500 hover:text-cyan-300 mt-auto pt-1"
      >
        Read more →
      </a>
    </div>
  );
}

export default function NewsMatrix({ news }) {
  if (!news || news.length === 0) {
    return (
      <div className="text-slate-400 py-8 text-center">Loading news...</div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {['WORLD', 'BUSINESS', 'TECH'].map((cat) => {
        const items = news.filter((n) => n.category === cat).slice(0, 10);
        return (
          <div key={cat} className="flex flex-col gap-3">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider border-b border-slate-700 pb-2">
              {CATEGORY_LABELS[cat]}
            </h3>
            {items.length === 0 ? (
              <p className="text-slate-500 text-xs py-4">No items available.</p>
            ) : (
              items.map((item, idx) => (
                <NewsCard key={idx} item={item} />
              ))
            )}
          </div>
        );
      })}
    </div>
  );
}
