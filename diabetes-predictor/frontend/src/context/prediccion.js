import { createContext, useContext } from 'react'

export const ContextoPrediccion = createContext(null)

export function usePrediccion() {
  const contexto = useContext(ContextoPrediccion)
  if (!contexto) {
    throw new Error('usePrediccion debe usarse dentro de ProveedorPrediccion')
  }
  return contexto
}