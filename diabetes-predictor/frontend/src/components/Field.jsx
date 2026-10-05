const BASE =
  'w-full rounded-lg border bg-white px-3 py-2.5 text-sm text-texto shadow-sm transition placeholder:text-slate-400'

function clases(estado) {
  if (estado === 'error') return `${BASE} border-clase-t1 bg-red-50/40`
  return `${BASE} border-borde hover:border-guinda-claro`
}

/**
 * Campo de formulario con etiqueta siempre visible, ayuda y mensaje de error.
 * El id se genera a partir del nombre para que la etiqueta quede ligada al control.
 */
export default function Field({
  nombre,
  etiqueta,
  ayuda,
  error,
  opciones,
  placeholder,
  ...props
}) {
  const id = `campo-${nombre}`
  const descritoPor = [ayuda && `${id}-ayuda`, error && `${id}-error`]
    .filter(Boolean)
    .join(' ')

  return (
    <div>
      <label
        htmlFor={id}
        className="mb-1.5 block font-titulo text-sm font-semibold text-guinda"
      >
        {etiqueta}
        {props.required === false && (
          <span className="ml-1.5 font-sans text-xs font-normal text-slate-500">
            (opcional)
          </span>
        )}
      </label>

      {ayuda && (
        <p id={`${id}-ayuda`} className="mb-1.5 text-xs text-slate-500">
          {ayuda}
        </p>
      )}

      {opciones ? (
        <select
          id={id}
          name={nombre}
          aria-invalid={Boolean(error)}
          aria-describedby={descritoPor || undefined}
          className={clases(error ? 'error' : 'ok')}
          {...props}
        >
          {opciones.map((opcion) => (
            <option key={opcion.valor} value={opcion.valor}>
              {opcion.texto}
            </option>
          ))}
        </select>
      ) : (
        <input
          id={id}
          name={nombre}
          placeholder={placeholder}
          aria-invalid={Boolean(error)}
          aria-describedby={descritoPor || undefined}
          className={clases(error ? 'error' : 'ok')}
          {...props}
        />
      )}

      {error && (
        <p id={`${id}-error`} role="alert" className="mt-1.5 text-xs font-medium text-clase-t1">
          {error}
        </p>
      )}
    </div>
  )
}