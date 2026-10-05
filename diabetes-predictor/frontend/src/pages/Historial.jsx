import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import Card from '../components/Card'
import { obtenerHistorial } from '../services/datos'

function fechaLegible(iso) {
  if (!iso) return '—'
  const fecha = new Date(iso)
  if (Number.isNaN(fecha.getTime())) return '—'
  return fecha.toLocaleDateString('es-MX', { dateStyle: 'medium' })
}

function color(diagnostico) {
  if (diagnostico === 'sano') return 'text-clase-sano'
  if (diagnostico === 'tipo_1') return 'text-clase-t1'
  if (diagnostico === 'tipo_2') return 'text-clase-t2'
  return 'text-clase-gest'
}

export default function Historial() {
  const [historial, setHistorial] = useState([])
  const [filtro, setFiltro] = useState('todos')
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    let vigente = true
    obtenerHistorial()
      .then((filas) => vigente && setHistorial(filas))
      .finally(() => vigente && setCargando(false))
    return () => {
      vigente = false
    }
  }, [])

  const diagnosticos = useMemo(
    () => [...new Set(historial.map((fila) => fila.diagnostico))].filter(Boolean),
    [historial],
  )

  const filtrados = useMemo(
    () => (filtro === 'todos' ? historial : historial.filter((f) => f.diagnostico === filtro)),
    [historial, filtro],
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold sm:text-3xl">Historial</h1>
        <p className="mt-1.5 text-sm text-slate-600">
          Predicciones guardadas con fecha, paciente, diagnóstico y probabilidad.
        </p>
      </div>

      <Card>
        <div className="mb-5 flex flex-wrap items-end gap-4">
          <div className="min-w-[14rem]">
            <label
              htmlFor="filtro-historial"
              className="mb-1.5 block font-titulo text-sm font-semibold text-guinda"
            >
              Filtrar por diagnóstico
            </label>
            <select
              id="filtro-historial"
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="w-full rounded-lg border border-borde bg-white px-3 py-2.5 text-sm shadow-sm transition hover:border-guinda-claro"
            >
              <option value="todos">Todos</option>
              {diagnosticos.map((diagnostico) => (
                <option key={diagnostico} value={diagnostico}>
                  {diagnostico}
                </option>
              ))}
            </select>
          </div>
          <p className="ml-auto self-center text-sm text-slate-500">
            {filtrados.length}{' '}
            {filtrados.length === 1 ? 'predicción' : 'predicciones'}
          </p>
        </div>

        {cargando ? (
          <p className="py-8 text-center text-sm text-slate-500">Cargando historial…</p>
        ) : filtrados.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">
            No hay predicciones registradas con ese filtro.
          </p>
        ) : (
          <div className="-mx-5 overflow-x-auto sm:mx-0">
            <table className="w-full min-w-[42rem] border-collapse text-sm">
              <thead>
                <tr className="border-b border-borde text-left">
                  {['ID', 'Fecha', 'Paciente', 'Diagnóstico', 'Prob.'].map((columna) => (
                    <th
                      key={columna}
                      scope="col"
                      className="px-3 py-3 font-titulo text-xs font-semibold uppercase tracking-wider text-guinda"
                    >
                      {columna}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtrados.map((fila) => (
                  <tr key={fila.id} className="border-b border-slate-100 last:border-0">
                    <td className="px-3 py-3 font-mono text-slate-500">#{fila.id}</td>
                    <td className="px-3 py-3 whitespace-nowrap text-slate-600">
                      {fechaLegible(fila.fecha)}
                    </td>
                    <td className="px-3 py-3 font-medium text-texto">{fila.paciente}</td>
                    <td className={`px-3 py-3 font-medium ${color(fila.diagnostico)}`}>
                      {fila.diagnostico}
                    </td>
                    <td className="px-3 py-3 tabular-nums">
                      {(Number(fila.probabilidad) * 100).toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <div className="text-center">
        <Link to="/nueva-prediccion" className="btn-base btn-dorado inline-flex">
          Generar una nueva predicción
        </Link>
      </div>
    </div>
  )
}