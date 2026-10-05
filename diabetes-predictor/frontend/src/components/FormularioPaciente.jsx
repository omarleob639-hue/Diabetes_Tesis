import { useState } from 'react'

const CAMPOS_NUMERICOS = {
  edad: { min: 0, max: 120, paso: 1, required: true },
  imc: { min: 1, max: 100, paso: 0.1, required: true },
  glucosa_ayuno: { min: 20, max: 600, paso: 0.01, required: true },
  hba1c: { min: 3, max: 20, paso: 0.1, required: false },
  presion_sistolica: { min: 50, max: 300, paso: 1, required: true },
  presion_diastolica: { min: 30, max: 200, paso: 1, required: true },
}

const ESTADO_INICIAL = {
  nombre: '',
  edad: '',
  sexo: '',
  imc: '',
  glucosa_ayuno: '',
  hba1c: '',
  presion_sistolica: '',
  presion_diastolica: '',
  antecedentes_familiares: false,
}

const CLASES_INPUT =
  'w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500'

export default function FormularioPaciente({ onEnviar, cargando, error }) {
  const [datos, setDatos] = useState(ESTADO_INICIAL)

  function actualizar(campo, valor) {
    setDatos((previos) => ({ ...previos, [campo]: valor }))
  }

  function manejarEnvio(evento) {
    evento.preventDefault()
    onEnviar(datos)
  }

  return (
    <form
      onSubmit={manejarEnvio}
      className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
    >
      <h2 className="mb-4 text-lg font-semibold text-slate-900">Datos del paciente</h2>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">Nombre</span>
          <input
            type="text"
            required
            maxLength={120}
            value={datos.nombre}
            onChange={(e) => actualizar('nombre', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">Edad</span>
          <input
            type="number"
            required
            {...CAMPOS_NUMERICOS.edad}
            value={datos.edad}
            onChange={(e) => actualizar('edad', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">Sexo</span>
          <select
            required
            value={datos.sexo}
            onChange={(e) => actualizar('sexo', e.target.value)}
            className={CLASES_INPUT}
          >
            <option value="">Seleccione</option>
            <option value="F">Femenino</option>
            <option value="M">Masculino</option>
            <option value="O">Otro</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">IMC (kg/m²)</span>
          <input
            type="number"
            required
            {...CAMPOS_NUMERICOS.imc}
            value={datos.imc}
            onChange={(e) => actualizar('imc', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">Glucosa en ayuno (mg/dL)</span>
          <input
            type="number"
            step="0.01"
            required
            min={CAMPOS_NUMERICOS.glucosa_ayuno.min}
            max={CAMPOS_NUMERICOS.glucosa_ayuno.max}
            value={datos.glucosa_ayuno}
            onChange={(e) => actualizar('glucosa_ayuno', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">
            HbA1c (%) <span className="font-normal text-slate-400">opcional</span>
          </span>
          <input
            type="number"
            {...CAMPOS_NUMERICOS.hba1c}
            value={datos.hba1c}
            onChange={(e) => actualizar('hba1c', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">Presión sistólica (mmHg)</span>
          <input
            type="number"
            required
            {...CAMPOS_NUMERICOS.presion_sistolica}
            value={datos.presion_sistolica}
            onChange={(e) => actualizar('presion_sistolica', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium text-slate-700">Presión diastólica (mmHg)</span>
          <input
            type="number"
            required
            {...CAMPOS_NUMERICOS.presion_diastolica}
            value={datos.presion_diastolica}
            onChange={(e) => actualizar('presion_diastolica', e.target.value)}
            className={CLASES_INPUT}
          />
        </label>
      </div>

      <label className="mt-4 flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={datos.antecedentes_familiares}
          onChange={(e) => actualizar('antecedentes_familiares', e.target.checked)}
          className="size-4 rounded border-slate-300 text-sky-600 focus:ring-sky-500"
        />
        <span className="font-medium text-slate-700">Antecedentes familiares de diabetes</span>
      </label>

      {error && (
        <p role="alert" className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={cargando}
        className="mt-6 w-full rounded-lg bg-sky-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {cargando ? 'Analizando…' : 'Analizar paciente'}
      </button>
    </form>
  )
}