import { Route, Routes } from 'react-router-dom'

import Header from './components/Header'
import { ProveedorPrediccion } from './context/ProveedorPrediccion'
import Historial from './pages/Historial'
import Inicio from './pages/Inicio'
import NuevaPrediccion from './pages/NuevaPrediccion'
import Pacientes from './pages/Pacientes'
import Resultados from './pages/Resultados'

export default function App() {
  return (
    <ProveedorPrediccion>
      <div className="flex min-h-screen flex-col bg-fondo">
        <Header />

        <main className="mx-auto w-full max-w-6xl flex-1 px-4 pb-14 pt-32 sm:px-6 lg:pt-24">
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/nueva-prediccion" element={<NuevaPrediccion />} />
            <Route path="/resultados" element={<Resultados />} />
            <Route path="/pacientes" element={<Pacientes />} />
            <Route path="/historial" element={<Historial />} />
            <Route path="*" element={<Inicio />} />
          </Routes>
        </main>

        <footer className="border-t border-borde bg-white">
          <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-6 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between sm:px-6">
            <p>
              <span className="font-titulo font-semibold text-guinda">PrediDiabetes</span> ·
              Sistema de apoyo al diagnóstico
            </p>
            <p className="text-xs">
              Proyecto de tesis · Universidad · Contacto para uso clínico autorizado
            </p>
          </div>
        </footer>
      </div>
    </ProveedorPrediccion>
  )
}