import { useState } from 'react'

import FormularioPaciente from './components/FormularioPaciente'
import ResultCard from './components/ResultCard'
import { crearPrediccion } from './services/api'

export default function App() {
  const [prediccion, setPrediccion] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function manejarEnvio(datos) {
    setCargando(true)
    setError(null)

    const numericos = ['edad', 'imc', 'glucosa_ayuno', 'presion_sistolica', 'presion_diastolica']

    const cuerpo = Object.fromEntries(
      Object.entries(datos).map(([campo, valor]) => [
        campo,
        numericos.includes(campo) || campo === 'hba1c'
          ? valor === ''
            ? null
            : Number(valor)
          : valor,
      ]),
    )

    try {
      setPrediccion(await crearPrediccion(cuerpo))
    } catch (fallo) {
      setError(fallo.message)
      setPrediccion(null)
    } finally {
      setCargando(false)
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 py-10">
      <div className="mx-auto max-w-3xl px-4">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            Detección de Diabetes
          </h1>
          <p className="mt-2 text-slate-600">
            Identificación del tipo de diabetes con mayor probabilidad en un paciente
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <FormularioPaciente onEnviar={manejarEnvio} cargando={cargando} error={error} />
          <ResultCard prediccion={prediccion} />
        </div>
      </div>
    </main>
  )
}