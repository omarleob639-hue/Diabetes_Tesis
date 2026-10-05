# PrediDiabetes — Sistema de Predicción de Diabetes

Tesis de licenciatura sobre detección de diabetes mediante redes neuronales
artificiales. Sistema multiclase que identifica el tipo de diabetes con mayor
probabilidad en un paciente (tipo 1, tipo 2, gestacional o sano).

> **Estado:** la interfaz está publicada en Vercel, pero **el modelo no está
> entrenado**. El sistema opera con datos de demostración y lo declara en
> pantalla. El bloqueo actual es la fuente de datos, no el código.

## Documentos

| Documento | Contenido |
|---|---|
| [`tesis/`](tesis/) | Manuscrito en LaTeX (Capítulos 1–3 redactados) |
| [`tesis_diabetes_resumen.md`](tesis_diabetes_resumen.md) | Resumen de los capítulos 1–3 y lista de pendientes |
| [`diabetes-predictor/ENTREGABLES_FINALES.md`](diabetes-predictor/ENTREGABLES_FINALES.md) | **Contexto técnico completo**: arquitectura, API, rutas, paleta, pendientes y datasets descartados |
| [`diabetes-predictor/FILTRO_DATASETS.md`](diabetes-predictor/FILTRO_DATASETS.md) | Criterios de selección y evaluación de datasets candidatos |
| [`protocolo2.0-Omar León Montiel.docx`](protocolo2.0-Omar%20León%20Montiel.docx) | Protocolo de investigación |

## Estructura

```
tesis/                     Manuscrito LaTeX, bibliografía e imágenes
diabetes-predictor/        Código del sistema
├── backend/               FastAPI, SQLAlchemy, Pydantic, tests
├── database/              Migraciones SQL y datos de prueba
├── data/                  Datasets (ignorados por git)
└── frontend/              React 19 + Vite + Tailwind v4 + React Router
    └── src/
        ├── pages/         Inicio, NuevaPrediccion, Resultados, Pacientes, Historial
        ├── components/    Header, Card, Field, ProbabilityBar
        ├── services/      api.js (real), mock.js (demo), datos.js (fallback)
        ├── constants/     clinico.js
        └── context/       Estado compartido de predicción
```

## Interfaz

Cinco rutas enrutadas con React Router:

| Ruta | Vista |
|---|---|
| `/` | Portada del proyecto |
| `/nueva-prediccion` | Formulario de las 8 variables clínicas |
| `/resultados` | Clase más probable y probabilidades por clase |
| `/pacientes` | Listado con búsqueda |
| `/historial` | Historial con filtros |

## Puesta en marcha rápida

```bash
# Backend
cd diabetes-predictor/backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
copy .env.example .env     # llenar credenciales de Supabase
.venv/Scripts/uvicorn main:app --reload

# Frontend (Node 22)
cd diabetes-predictor/frontend
npm install
npm run dev
```

El frontend funciona sin backend: si la API no responde, cae a datos de
demostración y lo avisa en pantalla. La variable que lee es
`VITE_API_BASE_URL` (ver `frontend/.env.example`).

## Estado

| Componente | Estado |
|---|---|
| Esquema SQL, migraciones y seeds | Implementado, sin aplicar a Supabase |
| API FastAPI (9 endpoints, 10 pruebas) | ✅ pasa |
| Interfaz React con 5 rutas | ✅ publicada en Vercel |
| Modelo de red neuronal | 🔴 Sin entrenar — bloqueado por datos |
| Despliegue del backend | 🟡 Pendiente de decisión (Lambda vs App Runner) |

El entrenamiento está pendiente de definir la fuente de los datos. Sin un
dataset real de diabetes tipo 1, la clasificación tetraclásica no es
defendible: los candidatos revisados solo aportan clases sanas, tipo 2 o
gestacionales. El detalle está en `FILTRO_DATASETS.md`.

Ver la sección "Lo que falta" de `ENTREGABLES_FINALES.md` para el desglose
completo.