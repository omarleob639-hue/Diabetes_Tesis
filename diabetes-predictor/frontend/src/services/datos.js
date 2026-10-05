import * as api from './api'
import * as mock from './mock'

/**
 * Capa unica de datos.
 *
 * Intenta primero la API real (FastAPI en AWS). Si no responde todavia, cae a
 * los datos de demostracion para que la interfaz siga siendo navegable. Cuando
 * el backend este desplegado no hay que cambiar nada: la deteccion es automatica.
 */

let enDemo = null
let ultimoFallo = null

export function estaEnDemo() {
  return enDemo === true
}

export function detalleFallo() {
  return ultimoFallo
}

async function conRespaldo(llamadaReal, llamadaDemo) {
  try {
    const resultado = await llamadaReal()
    enDemo = false
    ultimoFallo = null
    return resultado
  } catch (fallo) {
    enDemo = true
    ultimoFallo = fallo?.message ?? 'Sin conexión con la API'
    return llamadaDemo()
  }
}

export function predecir(datos) {
  const cuerpo = {
    nombre: datos.nombre?.trim() || 'Paciente sin identificar',
    ...datos,
    antecedentes_familiares: Boolean(datos.antecedentes_familiares),
  }
  return conRespaldo(() => api.crearPrediccion(cuerpo), () => mock.predecir(cuerpo))
}

export function obtenerPacientes() {
  return conRespaldo(api.listarPacientes, mock.listarPacientes)
}

export function obtenerHistorial() {
  return conRespaldo(api.listarPredicciones, mock.listarPredicciones)
}

export function obtenerEstado() {
  return conRespaldo(api.obtenerEstado, () => Promise.resolve({ status: 'demo', model: 'mock' }))
}