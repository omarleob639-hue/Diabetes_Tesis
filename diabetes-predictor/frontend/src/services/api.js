const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    throw new Error(await leerDetalleError(response))
  }

  return response.status === 204 ? null : response.json()
}

async function leerDetalleError(response) {
  try {
    const cuerpo = await response.json()
    if (Array.isArray(cuerpo.detail)) {
      return cuerpo.detail.map((e) => e.msg).join('; ')
    }
    return cuerpo.detail ?? `Error ${response.status}`
  } catch {
    return `Error ${response.status}`
  }
}

export function crearPrediccion(datosClinicos) {
  return request('/predictions', {
    method: 'POST',
    body: JSON.stringify(datosClinicos),
  })
}

export function listarPredicciones(patientId) {
  const query = patientId ? `?patient_id=${patientId}` : ''
  return request(`/predictions${query}`)
}

export function listarPacientes() {
  return request('/patients')
}

export function obtenerEstado() {
  return request('/health')
}