import { Link } from 'react-router-dom'

import Card from '../components/Card'
import ProbabilityBar from '../components/ProbabilityBar'
import { AVISO_CLINICO, CLASES, ORDEN_CLASES } from '../constants/clinico'
import { usePrediccion } from '../context/prediccion'

function fechaLegible(iso) {
  if (!iso) return '—'
  const fecha = new Date(iso)
  if (Number.isNaN(fecha.getTime())) return '—'
  return fecha.toLocaleString('es-MX', { dateStyle: 'long', timeStyle: 'short' })
}

export default function Resultados() {
  const { prediccion } = usePrediccion()

  if (!prediccion) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold sm:text-3xl">Resultados</h1>
        <Card>
          <div className="py-10 text-center">
            <p className="text-base font-medium text-texto">
              Aún no hay una predicción que mostrar.
            </p>
            <p className="mx-auto mt-2 max-w-md text-sm text-slate-600">
              Captura las variables clínicas de un paciente para generar el resultado.
            </p>
            <Link to="/nueva-prediccion" className="btn-base btn-dorado mt-6 inline-flex">
              Realizar una predicción
            </Link>
          </div>
        </Card>
      </div>
    )
  }

  const principal = CLASES[prediccion.diagnosis] ?? {
    etiqueta: prediccion.diagnosis,
    color: '#1f2937',
  }
  const probabilidades = prediccion.probabilities ?? {}

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold sm:text-3xl">Resultados</h1>
        <p className="mt-1.5 text-sm text-slate-600">
          Estimación del tipo de diabetes más probable y desglose de las cuatro clases.
        </p>
      </div>

      <Card conFranja>
        {prediccion.mock && (
          <p className="mb-5 rounded-lg border border-dorado bg-[#fdf8ef] px-4 py-3 text-sm font-medium text-[#6b5218]">
            Datos de demostración: la red neuronal aún no está conectada al backend.
          </p>
        )}

        <div className="flex flex-wrap items-baseline justify-between gap-4">
          <div>
            <p className="font-titulo text-xs font-semibold uppercase tracking-wider text-slate-500">
              Diagnóstico más probable
            </p>
            <p className="mt-1 font-titulo text-3xl font-bold" style={{ color: principal.color }}>
              {principal.etiqueta}
            </p>
          </div>
          <div className="rounded-xl bg-fondo px-5 py-3 text-right">
            <p className="font-titulo text-xs font-semibold uppercase tracking-wider text-slate-500">
              Probabilidad
            </p>
            <p
              className="font-titulo text-3xl font-bold tabular-nums"
              style={{ color: principal.color }}
            >
              {(Number(prediccion.confidence) * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        <div className="mt-8 space-y-4">
          {ORDEN_CLASES.map((clave) => (
            <ProbabilityBar
              key={clave}
              etiqueta={CLASES[clave].etiqueta}
              color={CLASES[clave].color}
              probabilidad={(Number(probabilidades[clave]) || 0) * 100}
            />
          ))}
        </div>

        <dl className="mt-8 grid gap-4 border-t border-borde pt-5 sm:grid-cols-2">
          <div>
            <dt className="font-titulo text-xs font-semibold uppercase tracking-wider text-slate-500">
              Identificador de la predicción
            </dt>
            <dd className="mt-1 font-mono text-sm text-texto">#{prediccion.id}</dd>
          </div>
          <div>
            <dt className="font-titulo text-xs font-semibold uppercase tracking-wider text-slate-500">
              Fecha y hora
            </dt>
            <dd className="mt-1 text-sm text-texto">{fechaLegible(prediccion.created_at)}</dd>
          </div>
        </dl>

        <div className="mt-7 flex flex-col gap-3 border-t border-borde pt-5 sm:flex-row">
          <Link to="/nueva-prediccion" className="btn-base btn-dorado">
            Nueva predicción
          </Link>
          <Link to="/historial" className="btn-base btn-contorno">
            Ver historial
          </Link>
        </div>
      </Card>

      <p className="rounded-[14px] border-l-4 border-guinda-claro bg-white px-5 py-4 text-sm leading-relaxed text-slate-700 shadow-sm">
        {AVISO_CLINICO}
      </p>
    </div>
  )
}