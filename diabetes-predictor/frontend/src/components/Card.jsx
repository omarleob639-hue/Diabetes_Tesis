import { Franja } from './Header'

export default function Card({
  titulo,
  descripcion,
  conFranja = false,
  className = '',
  children,
  ...props
}) {
  return (
    <section
      className={`overflow-hidden rounded-[14px] bg-white shadow-[0_1px_3px_rgba(31,41,55,0.10),0_8px_24px_rgba(31,41,55,0.06)] ${className}`}
      {...props}
    >
      {conFranja && <Franja />}
      {(titulo || descripcion) && (
        <div className="border-b border-borde px-5 py-4 sm:px-6">
          {titulo && <h2 className="text-lg font-semibold">{titulo}</h2>}
          {descripcion && <p className="mt-1 text-sm text-slate-600">{descripcion}</p>}
        </div>
      )}
      <div className="px-5 py-5 sm:px-6">{children}</div>
    </section>
  )
}