import { useMemo, useState } from 'react'

import { predecir } from '../services/datos'
import { ContextoPrediccion } from './prediccion'

export function ProveedorPrediccion({ children }) {
  const [prediccion, setPrediccion] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function generar(datos) {
    setCargando(true)
    setError(null)
    try {
      const resultado = await predecir(datos)
      setPrediccion(resultado)
      return resultado
    } catch (fallo) {
      setError(fallo.message)
      return null
    } finally {
      setCargando(false)
    }
  }

  const valor = useMemo(
    () => ({
      prediccion,
      cargando,
      error,
      generar,
      limpiar: () => setPrediccion(null),
    }),
    [prediccion, cargando, error],
  )

  return <ContextoPrediccion.Provider value={valor}>{children}</ContextoPrediccion.Provider>
}