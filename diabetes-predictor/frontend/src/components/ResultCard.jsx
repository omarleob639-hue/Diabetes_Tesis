const ETIQUETAS = {
  tipo_1: 'Diabetes tipo 1',
  tipo_2: 'Diabetes tipo 2',
  gestacional: 'Diabetes gestacional',
  sano: 'Sin diabetes',
}

const ORDEN = ['tipo_1', 'tipo_2', 'gestacional', 'sano']

const CAMPOS_PROBABILIDAD = {
  tipo_1: 'probabilidad_tipo1',
  tipo_2: 'probabilidad_tipo2',
  gestacional: 'probabilidad_gestacional',
  sano: 'probabilidad_sano',
}

export default function ResultCard({ prediccion }) {
  if (!prediccion) {
    return null
  }

  const { resultado } = prediccion

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">Resultado</h2>

      <div className="rounded-lg border border-sky-200 bg-sky-50 p-4">
        <p className="text-sm text-sky-700">Clase con mayor probabilidad</p>
        <p className="text-2xl font-bold text-sky-900">{ETIQUETAS[resultado]}</p>
      </div>

      <ul className="mt-5 space-y-3">
        {ORDEN.map((clave) => {
          const probabilidad = prediccion[CAMPOS_PROBABILIDAD[clave]]
          const porcentaje = (probabilidad * 100).toFixed(1)
          const esGanadora = clave === resultado

          return (
            <li key={clave}>
              <div className="flex items-baseline justify-between text-sm">
                <span className={esGanadora ? 'font-semibold text-slate-900' : 'text-slate-600'}>
                  {ETIQUETAS[clave]}
                </span>
                <span className={esGanadora ? 'font-semibold text-slate-900' : 'text-slate-500'}>
                  {porcentaje}%
                </span>
              </div>
              <div className="mt-1 h-2 w-full overflow-hidden rounded-full bg-slate-100">
                <div
                  className={esGanadora ? 'h-full bg-sky-600' : 'h-full bg-slate-300'}
                  style={{ width: `${porcentaje}%` }}
                />
              </div>
            </li>
          )
        })}
      </ul>

      <p className="mt-5 border-t border-slate-100 pt-4 text-xs text-slate-400">
        Herramienta de apoyo al diagnóstico. No sustituye el juicio médico profesional.
      </p>
    </section>
  )
}