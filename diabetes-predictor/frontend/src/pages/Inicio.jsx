import { Link } from 'react-router-dom'

import Card from '../components/Card'

const ACCESOS = [
  {
    to: '/nueva-prediccion',
    titulo: 'Nueva predicción',
    texto: 'Captura las ocho variables clínicas de un paciente y obtén el tipo de diabetes más probable.',
    icono: '+',
  },
  {
    to: '/resultados',
    titulo: 'Resultados',
    texto: 'Consulta el diagnóstico, su probabilidad y el desglose de las cuatro clases.',
    icono: '％',
  },
  {
    to: '/pacientes',
    titulo: 'Gestión de pacientes',
    texto: 'Registra, busca y consulta la información de los pacientes atendidos.',
    icono: '☰',
  },
  {
    to: '/historial',
    titulo: 'Historial',
    texto: 'Revisa las predicciones guardadas con fecha, paciente y nivel de confianza.',
    icono: '⏱',
  },
]

const OBJETIVO =
  'Apoyar al profesional de la salud en la identificación del tipo de diabetes mellitus más probable en un paciente, a partir de ocho variables clínicas de acceso rutinario, mediante una red neuronal artificial multiclase.'

const LIMITES = [
  'El resultado es una estimación estadística y no un diagnóstico definitivo.',
  'El modelo no sustituye la valoración clínica, el examen físico ni los análisis de laboratorio.',
  'Las probabilidades dependen de la distribución de la población con la que se entrenó la red.',
]

export default function Inicio() {
  return (
    <div className="space-y-8">
      <section className="rounded-[14px] bg-guinda px-6 py-12 text-white shadow-lg sm:px-10">
        <p className="mb-3 inline-block rounded-full bg-white/12 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white">
          Apoyo al diagnóstico
        </p>
        <h1 className="max-w-3xl text-3xl font-bold text-white sm:text-4xl">
          Sistema de Predicción de Diabetes
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-white/85">
          Plataforma basada en una red neuronal multiclase entrenada con datos clínicos
          de pacientes del municipio de Calpulalpan, Tlaxcala. Estima la probabilidad de
          diabetes tipo 1, tipo 2, gestacional o ausencia de diabetes.
        </p>
        <div className="mt-7 flex flex-wrap gap-3">
          <Link to="/nueva-prediccion" className="btn-base btn-dorado">
            Realizar una predicción
          </Link>
          <Link
            to="/historial"
            className="btn-base border-white/60 text-white hover:bg-white/10"
          >
            Ver historial
          </Link>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {ACCESOS.map((acceso) => (
          <Link
            key={acceso.to}
            to={acceso.to}
            className="rounded-[14px] bg-white p-5 shadow-[0_1px_3px_rgba(31,41,55,0.10)] transition hover:-translate-y-0.5 hover:shadow-[0_8px_24px_rgba(31,41,55,0.12)]"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-guinda/8 font-titulo text-lg font-bold text-guinda">
              {acceso.icono}
            </span>
            <h3 className="mt-4 text-base font-semibold">{acceso.titulo}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-slate-600">{acceso.texto}</p>
          </Link>
        ))}
      </section>

      <Card titulo="Acerca del sistema">
        <div className="space-y-6">
          <div>
            <h3 className="font-titulo text-sm font-semibold uppercase tracking-wide text-guinda-claro">
              Objetivo
            </h3>
            <p className="mt-1.5 text-sm leading-relaxed text-slate-700">{OBJETIVO}</p>
          </div>

          <div>
            <h3 className="font-titulo text-sm font-semibold uppercase tracking-wide text-guinda-claro">
              Variables clínicas
            </h3>
            <ul className="mt-2 flex flex-wrap gap-2">
              {[
                'Edad',
                'Sexo',
                'IMC',
                'Glucosa en ayuno',
                'HbA1c',
                'Presión sistólica',
                'Presión diastólica',
                'Antecedentes familiares',
              ].map((variable) => (
                <li
                  key={variable}
                  className="rounded-full border border-borde bg-fondo px-3 py-1 text-xs font-medium text-texto"
                >
                  {variable}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-titulo text-sm font-semibold uppercase tracking-wide text-guinda-claro">
              Límites
            </h3>
            <ul className="mt-2 list-disc space-y-1.5 pl-5 text-sm text-slate-700">
              {LIMITES.map((limite) => (
                <li key={limite}>{limite}</li>
              ))}
            </ul>
          </div>
        </div>
      </Card>
    </div>
  )
}