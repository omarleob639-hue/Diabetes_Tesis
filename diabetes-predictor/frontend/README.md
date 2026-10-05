# Frontend — Detección de Diabetes

Interfaz web del sistema de predicción. React 19 + Vite 8 + Tailwind CSS 4.
No contiene lógica de negocio: solo captura datos y muestra el resultado
que devuelve la API.

## Estructura
```
src/
├── components/
│   ├── FormularioPaciente.jsx   Captura de las 8 variables clínicas
│   └── ResultCard.jsx           Resultado con las 4 probabilidades
├── services/
│   └── api.js                   Cliente HTTP de la API
├── App.jsx                      Composición de la vista y manejo de estado
├── main.jsx                     Punto de entrada
└── index.css                    Import de Tailwind
```

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

## Notas
- Los estilos usan únicamente clases de Tailwind; no hay CSS inline.
- El backend debe estar corriendo para que el formulario funcione.
- Sin modelo entrenado, el backend responde 503 salvo que se active
  `MODEL_STUB_ENABLED=true`, que devuelve probabilidades ficticias
  útiles **solo para desarrollo de interfaz**.