export default function ProbabilityBar({ etiqueta, probabilidad, color }) {
  const valor = Math.max(0, Math.min(100, Number(probabilidad) || 0))

  return (
    <div>
      <div className="mb-1 flex items-baseline justify-between gap-3">
        <span className="font-titulo text-sm font-semibold text-texto">{etiqueta}</span>
        <span
          className="font-titulo text-sm font-bold tabular-nums"
          style={{ color }}
        >
          {valor.toFixed(1)}%
        </span>
      </div>
      <div
        className="h-3 w-full overflow-hidden rounded-full bg-slate-200"
        role="progressbar"
        aria-label={`Probabilidad de ${etiqueta}`}
        aria-valuenow={Number(valor.toFixed(1))}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className="h-full rounded-full transition-[width] duration-500"
          style={{ width: `${valor}%`, backgroundColor: color }}
        />
      </div>
    </div>
  )
}