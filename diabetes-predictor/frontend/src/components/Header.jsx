import { NavLink } from 'react-router-dom'

const ENLACES = [
  { to: '/', label: 'Inicio', exacto: true },
  { to: '/nueva-prediccion', label: 'Nueva predicción' },
  { to: '/resultados', label: 'Resultados' },
  { to: '/pacientes', label: 'Pacientes' },
  { to: '/historial', label: 'Historial' },
]

function Franja({ className = '' }) {
  return (
    <div className={`franja ${className}`} aria-hidden="true">
      <div className="flex-1 bg-[#006847]" />
      <div className="flex-1 bg-white" />
      <div className="flex-1 bg-[#ce1126]" />
    </div>
  )
}

function Marca() {
  return (
    <svg
      viewBox="0 0 24 24"
      className="h-9 w-9 shrink-0"
      fill="none"
      stroke="var(--color-dorado-claro)"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M3 12h4l2-5 3 10 2.5-7 1.5 2H21" />
    </svg>
  )
}

export default function Header() {
  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <Franja />
      <div className="bg-guinda">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <NavLink to="/" className="flex items-center gap-3">
            <Marca />
            <span className="leading-tight">
              <span className="block font-titulo text-lg font-bold text-white">
                PrediDiabetes
              </span>
              <span className="block text-xs text-white/80">
                Predicción clínica de diabetes mellitus
              </span>
            </span>
          </NavLink>

          <nav aria-label="Navegación principal" className="-mx-1 overflow-x-auto">
            <ul className="flex items-center gap-1 whitespace-nowrap px-1 pb-1 lg:pb-0">
              {ENLACES.map((enlace) => (
                <li key={enlace.to}>
                  <NavLink
                    to={enlace.to}
                    end={enlace.exacto}
                    className={({ isActive }) =>
                      [
                        'block rounded-lg px-3 py-2 text-sm font-semibold transition',
                        isActive
                          ? 'bg-guinda-medio text-white shadow-inner'
                          : 'text-white/85 hover:bg-guinda-medio hover:text-white',
                      ].join(' ')
                    }
                  >
                    {enlace.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </header>
  )
}

export { Franja }