# Frontend — PrediDiabetes

Interfaz web del sistema de predicción. React 19 + Vite 8 + Tailwind CSS 4 +
React Router 7. No contiene lógica de negocio ni lógica clínica: captura datos,
consume la capa de servicios y presenta el resultado.

## Estructura
```
src/
├── pages/
│   ├── Inicio.jsx               Portada y presentación institucional
│   ├── NuevaPrediccion.jsx      Formulario de las 8 variables clínicas
│   ├── Resultados.jsx           Clase principal y probabilidades por clase
│   ├── Pacientes.jsx            Listado con búsqueda
│   └── Historial.jsx            Historial con filtros
├── components/
│   ├── Header.jsx               Encabezado fijo con navegación
│   ├── Card.jsx                 Superficie de tarjeta reutilizable
│   ├── Field.jsx                Campo de formulario accesible
│   └── ProbabilityBar.jsx       Barra de probabilidad por clase
├── services/
│   ├── datos.js                 Capa única: API con fallback a demo
│   ├── api.js                   Cliente HTTP (VITE_API_BASE_URL)
│   └── mock.js                  Datos y predicción de demostración
├── constants/clinico.js         Clases, variables, paleta y aviso clínico
├── context/                     prediccion.js + ProveedorPrediccion.jsx
├── App.jsx                      Definición de rutas
├── main.jsx                     BrowserRouter
└── index.css                    Tokens de diseño (@theme)
```

## Rutas
| Ruta | Vista |
|---|---|
| `/` | `Inicio` |
| `/nueva-prediccion` | `NuevaPrediccion` |
| `/resultados` | `Resultados` |
| `/pacientes` | `Pacientes` |
| `/historial` | `Historial` |

`vercel.json` declara `rewrites` de `/(.*)` a `/index.html`. Es obligatorio:
sin eso, cargar `/historial` directamente devolvería 404 porque el enrutado
ocurre en el cliente.

## Comandos
```bash
npm install
npm run dev       # servidor de desarrollo en http://localhost:5173
npm run build     # build de producción en dist/
npm run lint      # oxlint
npm run preview   # previsualiza el build de producción
```

## Configuración
La URL de la API se define con la variable de entorno `VITE_API_BASE_URL`.
Si no se define, usa `http://localhost:8000`.

Para apuntar a una API desplegada:
```bash
# .env.local
VITE_API_BASE_URL=https://tu-api.onrender.com
```

## Modo demostración
`services/datos.js` intenta la API real y, si falla, degrada a `mock.js`
**declarándolo en pantalla** ("Datos de demostración"). La interfaz es
plenamente navegable sin backend desplegado.

Cuando el backend esté disponible no hay que tocar ningún componente: la
detección es automática.

## Notas
- Los estilos usan únicamente clases de Tailwind; no hay CSS inline.
- Las variables `VITE_*` son **públicas** por diseño de Vite. No poner
  secretos en ellas.
- El nombre de la variable es `VITE_API_BASE_URL`. `VITE_API_URL` se ignora.
- Node 22 (`engines` en `package.json`); Vercel usa esa versión.
- En Tailwind v4, `@utility` no acepta pseudo-selectores: escribir `&:hover`
  dentro del bloque, nunca `@utility x:hover`.
- Sin modelo entrenado, el backend responde 503 salvo que se active
  `MODEL_STUB_ENABLED=true`, que devuelve probabilidades ficticias
  útiles **solo para desarrollo de interfaz**.