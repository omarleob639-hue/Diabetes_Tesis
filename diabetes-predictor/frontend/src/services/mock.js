/**
 * Datos de demostracion mientras la red neuronal no este conectada.
 * Se reemplazan solos cuando el backend responde; ver servicios/datos.js.
 */

const PACIENTES_BASE = [
  { id: 1, nombre: 'María Guadalupe Hernández Ortiz', edad: 52, sexo: 'F', diagnostico: 'Diabetes tipo 2', probabilidad: 0.91 },
  { id: 2, nombre: 'Jorge Alberto Ramírez Lugo', edad: 34, sexo: 'M', diagnostico: 'Sin diabetes', probabilidad: 0.88 },
  { id: 3, nombre: 'Ana Karen Solís Bautista', edad: 29, sexo: 'F', diagnostico: 'Diabetes gestacional', probabilidad: 0.84 },
  { id: 4, nombre: 'Luis Enrique Cortés Mena', edad: 61, sexo: 'M', diagnostico: 'Diabetes tipo 2', probabilidad: 0.93 },
  { id: 5, nombre: 'Sofía Emiliano Reyes', edad: 26, sexo: 'F', diagnostico: 'Sin diabetes', probabilidad: 0.79 },
  { id: 6, nombre: 'Pedro Jakob Núñez Adler', edad: 11, sexo: 'M', diagnostico: 'Diabetes tipo 1', probabilidad: 0.87 },
  { id: 7, nombre: 'Rosa María Trinidad Paz', edad: 44, sexo: 'F', diagnostico: 'Diabetes tipo 2', probabilidad: 0.72 },
  { id: 8, nombre: 'Carlos Daniel Bautista Lugo', edad: 38, sexo: 'M', diagnostico: 'Sin diabetes', probabilidad: 0.69 },
]

const HISTORIAL_BASE = PACIENTES_BASE.slice(0, 7).map((paciente, indice) => ({
  id: 100 - indice,
  patient_id: paciente.id,
  paciente: paciente.nombre,
  fecha: `2026-0${(indice % 9) + 1}-${String(10 + indice).padStart(2, '0')}T09:30:00Z`,
  diagnostico: paciente.diagnostico,
  probabilidad: paciente.probabilidad,
}))

export function listarPacientes() {
  return Promise.resolve(
    PACIENTES_BASE.map((paciente) => ({ ...paciente })),
  )
}

export function listarPredicciones() {
  return Promise.resolve(HISTORIAL_BASE.map((fila) => ({ ...fila })))
}

/** Heuristica simple:Enough to make the form feel responsive while there is no model. */
export function predecir(datos) {
  const glucosa = Number(datos.glucosa_ayuno) || 0
  const hba1c = Number(datos.hba1c) || 0
  const edad = Number(datos.edad) || 0
  const imc = Number(datos.imc) || 0
  const severidad = Math.max(glucosa / 126, hba1c / 6.5, 0)

  const pesos = {
    sano: 1 / (1 + Math.max(0, severidad - 1) * 2),
    tipo_2: (imc > 25 ? 0.9 : 0.3) * (1 + Math.max(0, severidad - 1)),
    gestacional: datos.sexo === 'F' && edad >= 20 && edad <= 45 ? 0.8 * Math.max(0, severidad) : 0.15,
    tipo_1: edad < 20 ? 1.2 * Math.max(0.2, severidad) : 0.1,
  }

  const total = Object.values(pesos).reduce((a, b) => a + b, 0)
  const probabilidades = Object.fromEntries(
    Object.entries(pesos).map(([clave, valor]) => [clave, Number((valor / total).toFixed(4))]),
  )

  const principal = Object.entries(probabilidades).sort((a, b) => b[1] - a[1])[0]

  return Promise.resolve({
    id: Math.floor(Math.random() * 900 + 100),
    created_at: new Date().toISOString(),
    diagnosis: principal[0],
    confidence: probabilidades[principal[0]],
    probabilities: probabilidades,
    mock: true,
  })
}