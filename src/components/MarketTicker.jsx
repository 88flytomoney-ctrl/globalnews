export default function MarketTicker({ assets }) {
  if (!assets || assets.length === 0) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-slate-800 rounded-lg p-4 animate-pulse h-24" />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      {assets.map((asset) => {
        const isPositive = asset.pctChange >= 0;
        const isForex = asset.isForex;

        return (
          <div
            key={asset.name}
            className="bg-slate-800 rounded-lg p-4 flex flex-col gap-1"
          >
            <div className="text-xs text-slate-400 truncate">{asset.name}</div>
            <div className="text-base font-semibold text-white">
              {isForex
                ? `${asset.current.toFixed(2)}`
                : `$${asset.current.toFixed(2)}`}
            </div>
            <div className="text-xs text-slate-500">
              5D: {isForex
                ? `${(asset.prev5d).toFixed(2)}`
                : `$${asset.prev5d.toFixed(2)}`}
            </div>
            <div
              className={`text-sm font-bold mt-1 ${
                isPositive ? 'text-green-400' : 'text-red-400'
              }`}
            >
              {isPositive ? '+' : ''}{asset.pctChange.toFixed(2)}%
            </div>
          </div>
        );
      })}
    </div>
  );
}
