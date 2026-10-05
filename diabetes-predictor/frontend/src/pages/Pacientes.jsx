import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import Card from '../components/Card'
import { obtenerPacientes } from '../services/datos'

const SEXO = { F: 'Femenino', M: 'Masculino', O: 'Otro' }

export default function Pacientes() {
  const [pacientes, setPacientes] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    let vigente = true
    obtenerPacientes()
      .then((filas) => vigente && setPacientes(filas))
      .finally(() => vigente && setCargando(false))
    return () => {
      vigente = false
    }
  }, [])

  const filtrados = useMemo(() => {
    const termino = busqueda.trim().toLowerCase()
    if (!termino) return pacientes
    return pacientes.filter((paciente) =>
      `${paciente.nombre} ${paciente.diagnostico}`.toLowerCase().includes(termino),
    )
  }, [pacientes, busqueda])

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold sm:text-3xl">Pacientes</h1>
          <p className="mt-1.5 text-sm text-slate-600">
            Consulta de pacientes registrados en el sistema.
          </p>
        </div>
        <Link to="/nueva-prediccion" className="btn-base btn-dorado">
          Dar de alta con predicción
        </Link>
      </div>

      <Card>
        <div className="mb-5">
          <label
            htmlFor="busqueda-pacientes"
            className="mb-1.5 block font-titulo text-sm font-semibold text-guinda"
          >
            Buscar paciente
          </label>
          <input
            id="busqueda-pacientes"
            type="search"
            placeholder="Nombre o diagnóstico"
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="w-full rounded-lg border border-borde bg-white px-3 py-2.5 text-sm shadow-sm transition placeholder:text-slate-400 hover:border-guinda-claro sm:max-w-sm"
          />
        </div>

        {cargando ? (
          <p className="py-8 text-center text-sm text-slate-500">Cargando pacientes…</p>
        ) : filtrados.length === 0 ? (
          <p className="py-8 text-center text-sm text-slate-500">
            No se encontraron pacientes con ese criterio.
          </p>
        ) : (
          <div className="-mx-5 overflow-x-auto sm:mx-0">
            <table className="w-full min-w-[42rem] border-collapse text-sm">
              <thead>
                <tr className="border-b border-borde text-left">
                  {['ID', 'Nombre', 'Edad', 'Sexo', 'Último diagnóstico', 'Prob.'].map(
                    (columna) => (
                      <th
                        key={columna}
                        scope="col"
                        className="px-3 py-3 font-titulo text-xs font-semibold uppercase tracking-wider text-guinda"
                      >
                        {columna}
                      </th>
                    ),
                  )}
                </tr>
              </thead>
              <tbody>
                {filtrados.map((paciente) => (
                  <tr key={paciente.id} className="border-b border-slate-100 last:border-0">
                    <td className="px-3 py-3 font-mono text-slate-500">{paciente.id}</td>
                    <td className="px-3 py-3 font-medium text-texto">{paciente.nombre}</td>
                    <td className="px-3 py-3 tabular-nums">{paciente.edad}</td>
                    <td className="px-3 py-3">{SEXO[paciente.sexo] ?? paciente.sexo}</td>
                    <td className="px-3 py-3">{paciente.diagnostico}</td>
                    <td className="px-3 py-3 tabular-nums">
                      {(Number(paciente.probabilidad) * 100).toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}