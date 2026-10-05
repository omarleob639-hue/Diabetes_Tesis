import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import Card from '../components/Card'
import Field from '../components/Field'
import { VARIABLES } from '../constants/clinico'
import { usePrediccion } from '../context/prediccion'

const ESTADO_INICIAL = {
  nombre: '',
  edad: '',
  sexo: '',
  imc: '',
  glucosa_ayuno: '',
  hba1c: '',
  presion_sistolica: '',
  presion_diastolica: '',
  antecedentes_familiares: 'false',
}

const OPCIONES_SEXO = [
  { valor: '', texto: 'Seleccione…' },
  { valor: 'F', texto: 'Femenino' },
  { valor: 'M', texto: 'Masculino' },
  { valor: 'O', texto: 'Otro' },
]

const OPCIONES_ANTECEDENTES = [
  { valor: 'false', texto: 'No' },
  { valor: 'true', texto: 'Sí' },
]

function validar(datos) {
  const errores = {}

  for (const variable of VARIABLES) {
    const bruto = datos[variable.nombre]
    if (variable.requerido === false) continue
    if (bruto === '') {
      errores[variable.nombre] = `${variable.etiqueta} es obligatoria.`
      continue
    }
    const valor = Number(bruto)
    if (Number.isNaN(valor)) {
      errores[variable.nombre] = `${variable.etiqueta} debe ser numérico.`
    } else if (valor < variable.min || valor > variable.max) {
      errores[variable.nombre] =
        `${variable.etiqueta} debe estar entre ${variable.min} y ${variable.max} ${variable.unidad}.`
    }
  }

  if (!datos.sexo) errores.sexo = 'Seleccione el sexo.'
  if (datos.antecedentes_familiares === '') {
    errores.antecedentes_familiares = 'Indique si existen antecedentes familiares.'
  }

  return errores
}

export default function NuevaPrediccion() {
  const [datos, setDatos] = useState(ESTADO_INICIAL)
  const [errores, setErrores] = useState({})
  const navegar = useNavigate()
  const { generar, cargando, error } = usePrediccion()

  function actualizar(campo, valor) {
    setDatos((previos) => ({ ...previos, [campo]: valor }))
    setErrores((previos) => ({ ...previos, [campo]: undefined }))
  }

  function limpiar() {
    setDatos(ESTADO_INICIAL)
    setErrores({})
  }

  async function manejarEnvio(evento) {
    evento.preventDefault()
    const encontrados = validar(datos)
    setErrores(encontrados)
    if (Object.keys(encontrados).length > 0) return

    const resultado = await generar({
      ...datos,
      antecedentes_familiares: datos.antecedentes_familiares === 'true',
    })
    if (resultado) navegar('/resultados')
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold sm:text-3xl">Nueva predicción</h1>
        <p className="mt-1.5 text-sm text-slate-600">
          Registra las ocho variables clínicas. Los campos opcionales pueden quedar vacíos.
        </p>
      </div>

      <Card>
        <form onSubmit={manejarEnvio} noValidate>
          <div className="grid gap-x-6 gap-y-5 sm:grid-cols-2">
            <Field
              nombre="nombre"
              etiqueta="Nombre del paciente"
              ayuda="Opcional. Si se omite se registra como paciente sin identificar."
              placeholder="Nombre(s) y apellido(s)"
              maxLength={120}
              value={datos.nombre}
              onChange={(e) => actualizar('nombre', e.target.value)}
            />

            {VARIABLES.map((variable) => (
              <Field
                key={variable.nombre}
                nombre={variable.nombre}
                etiqueta={`${variable.etiqueta} (${variable.unidad})`}
                placeholder={variable.placeholder}
                error={errores[variable.nombre]}
                type="number"
                inputMode="decimal"
                step="any"
                min={variable.min}
                max={variable.max}
                required={variable.requerido !== false}
                value={datos[variable.nombre]}
                onChange={(e) => actualizar(variable.nombre, e.target.value)}
              />
            ))}

            <Field
              nombre="sexo"
              etiqueta="Sexo"
              opciones={OPCIONES_SEXO}
              error={errores.sexo}
              required
              value={datos.sexo}
              onChange={(e) => actualizar('sexo', e.target.value)}
            />

            <Field
              nombre="antecedentes_familiares"
              etiqueta="Antecedentes familiares de diabetes"
              opciones={OPCIONES_ANTECEDENTES}
              error={errores.antecedentes_familiares}
              required
              value={datos.antecedentes_familiares}
              onChange={(e) => actualizar('antecedentes_familiares', e.target.value)}
            />
          </div>

          {error && (
            <p
              role="alert"
              className="mt-5 rounded-lg border border-clase-t1 bg-red-50 px-4 py-3 text-sm font-medium text-clase-t1"
            >
              {error}
            </p>
          )}

          <div className="mt-7 flex flex-col-reverse gap-3 border-t border-borde pt-5 sm:flex-row sm:justify-end">
            <button type="button" onClick={limpiar} className="btn-base btn-contorno">
              Limpiar
            </button>
            <button
              type="submit"
              disabled={cargando}
              className="btn-base btn-dorado disabled:cursor-not-allowed disabled:opacity-60"
            >
              {cargando ? 'Analizando…' : 'Generar predicción'}
            </button>
          </div>
        </form>
      </Card>
    </div>
  )
}