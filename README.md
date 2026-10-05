# Diabetes_Tesis

Tesis de licenciatura sobre detección de diabetes mediante redes neuronales
artificiales. Sistema multiclase que identifica el tipo de diabetes con mayor
probabilidad en un paciente (tipo 1, tipo 2, gestacional o sano).

## Documentos

| Documento | Contenido |
|---|---|
| [`tesis/`](tesis/) | Manuscrito en LaTeX (Capítulos 1–3 redactados) |
| [`tesis_diabetes_resumen.md`](tesis_diabetes_resumen.md) | Resumen de los capítulos 1–3 y lista de pendientes |
| [`diabetes-predictor/ENTREGABLES_FINALES.md`](diabetes-predictor/ENTREGABLES_FINALES.md) | Contexto técnico del proyecto, API y estado actual |
| [`protocolo2.0-Omar León Montiel.docx`](protocolo2.0-Omar%20León%20Montiel.docx) | Protocolo de investigación |

## Estructura

```
tesis/                     Manuscrito LaTeX, bibliografía e imágenes
diabetes-predictor/        Código del sistema
├── backend/               FastAPI, modelos, tests
├── database/              Migraciones SQL y datos de prueba
├── data/                  Datasets (ignorados por git)
└── frontend/              React + Vite + Tailwind
```

## Puesta en marcha rápida

```bash
# Backend
cd diabetes-predictor/backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
copy .env.example .env
.venv/Scripts/uvicorn main:app --reload

# Frontend
cd diabetes-predictor/frontend
npm install
npm run dev
```

## Estado

El esquema de base de datos, la API y la interfaz web están implementados y
verificados. El entrenamiento del modelo está pendiente de definir la fuente
de los datos. Ver la sección "Estado actual" de `ENTREGABLES_FINALES.md`.