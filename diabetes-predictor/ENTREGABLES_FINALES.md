# Sistema de Predicción de Diabetes — Contexto del Proyecto

## ¿Qué es?
Sistema web para la detección temprana de diabetes mellitus desarrollado
como tesis de licenciatura. Predice de manera integrada el tipo de diabetes
con mayor probabilidad en un paciente: tipo 1, tipo 2, gestacional o sano,
utilizando una red neuronal artificial multiclase.

---

## Objetivo
Demostrar que un modelo integral basado en redes neuronales que detecta
los tipos de diabetes simultáneamente es estadísticamente más preciso
que modelos individuales independientes, con una exactitud >= 85%.

---

## Hipótesis
Existen diferencias estadísticamente significativas en exactitud y tasa
de falsos positivos entre el modelo integral y los modelos individuales,
siendo el modelo integral superior (nivel de significancia: 0.05).

---

## Variables clínicas de entrada
| Variable | Campo en la API | Tipo |
|---|---|---|
| Edad | `edad` | Numérica |
| Sexo | `sexo` | Categórica (`F`, `M`, `O`) |
| Índice de masa corporal (IMC) | `imc` | Numérica |
| Glucosa en ayuno | `glucosa_ayuno` | Numérica |
| Hemoglobina glicosilada (HbA1c) | `hba1c` | Numérica (opcional) |
| Presión arterial sistólica | `presion_sistolica` | Numérica |
| Presión arterial diastólica | `presion_diastolica` | Numérica |
| Antecedentes familiares de diabetes | `antecedentes_familiares` | Booleana |

## Clases de salida
- `tipo_1` — Diabetes tipo 1
- `tipo_2` — Diabetes tipo 2
- `gestacional` — Diabetes gestacional
- `sano` — Sin diabetes

---

## Stack tecnológico
| Capa | Tecnología | Rol |
|---|---|---|
| Interfaz | React 19 + Vite | Formulario de entrada y visualización de resultados |
| Estilos | Tailwind CSS v4 | Utilidades CSS, sin estilos inline |
| Hosting frontend | Vercel | Deploy automático desde GitHub |
| API | FastAPI + Pydantic v2 | Endpoints REST para predicción y gestión de pacientes |
| Driver PostgreSQL | psycopg 3 | Acceso a la base de datos |
| ORM | SQLAlchemy 2.0 | Mapeo de las tablas `patients` y `predictions` |
| Serverless | AWS Lambda | Pendiente de decisión (ver abajo) |
| Modelo ML | TensorFlow | Red neuronal multiclase (bloqueado) |
| Preprocesamiento | Scikit-learn | Normalización y codificación (bloqueado) |
| Base de datos | PostgreSQL | Almacenamiento de pacientes y predicciones |
| BaaS | Supabase | Autenticación, API REST y panel de administración |
| Experimentación | Jupyter Notebook | Exploración, entrenamiento y evaluación (bloqueado) |
| Versiones | GitHub | Control de versiones y CI/CD |

---

## Arquitectura
```
[React en Vercel] --HTTP/REST--> [FastAPI] --> [Modelo TensorFlow]
                                          |            |
                                          +--> [PostgreSQL / Supabase]
```

El frontend es puramente presentacional: no contiene lógica de negocio y
solo consume la API por HTTP. El servicio de predicción vive en
`services/model_service.py`, que centraliza la carga del modelo, el
preprocesamiento y el orden de las variables.

---

## Flujo del sistema
1. El médico ingresa los datos clínicos del paciente en el formulario web
2. React envía los datos a `POST /predictions` de FastAPI
3. FastAPI valida los datos con Pydantic y llama a `services/model_service.py`
4. El servicio aplica el preprocesamiento (escalador + codificación)
5. La red neuronal genera probabilidades para las 4 clases
6. FastAPI persiste paciente y predicción en una sola transacción y devuelve
   el tipo con mayor probabilidad junto con las 4 probabilidades
7. React muestra el resultado en `components/ResultCard.jsx`

---

## API
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Estado del servicio y de la base de datos |
| `GET` | `/patients` | Listar pacientes |
| `POST` | `/patients` | Registrar paciente |
| `GET` | `/patients/{patient_id}` | Consultar paciente |
| `PATCH` | `/patients/{patient_id}` | Actualizar paciente |
| `DELETE` | `/patients/{patient_id}` | Eliminar paciente |
| `GET` | `/predictions` | Listar predicciones (filtrable por `patient_id`) |
| `POST` | `/predictions` | Crear predicción a partir de datos clínicos |
| `GET` | `/predictions/{prediction_id}` | Consultar predicción |

Documentación interactiva: `http://localhost:8000/docs`

---

## Estructura del repositorio
```
diabetes-predictor/
├── backend/
│   ├── main.py                 Aplicación FastAPI
│   ├── core/                   Configuración y enums compartidos
│   ├── db/                     Modelos SQLAlchemy y sesión
│   ├── schemas/                Contratos Pydantic de entrada y salida
│   ├── routers/                Endpoints HTTP
│   ├── services/               Lógica de predicción
│   ├── tests/                  Pruebas de humo
│   ├── notebooks/              Experiments (bloqueado)
│   └── model/saved_model/      Modelo entrenado (bloqueado)
├── database/
│   ├── migrations/             SQL versionado (001_esquema_inicial.sql)
│   └── seeds/                  Datos de prueba
├── data/
│   ├── raw/                    Dataset original (bloqueado)
│   └── processed/              Dataset limpio (bloqueado)
└── frontend/
    ├── src/components/         FormularioPaciente, ResultCard
    ├── src/services/           Cliente HTTP de la API
    └── src/App.jsx             Composición de la vista
```

---

## Métricas de evaluación
- Exactitud global >= 85%
- Sensibilidad y especificidad por clase
- F1-score y matriz de confusión multiclase
- Tasa de falsos positivos (base de la hipótesis)
- Validación cruzada
- Prueba estadística frente a modelos individuales por tipo

---

## Reglas de desarrollo
- Python 3.11 en el backend (`3.12` es el máximo soportado por TensorFlow)
- React 19 + Vite en el frontend
- Comentarios del código en español
- Nombres de variables, funciones y archivos en inglés
- Variables de entorno nunca hardcodeadas, siempre desde `.env`
- Tablas y columnas SQL en `snake_case`
- Toda tabla tiene: `id UUID`, `created_at`, `updated_at`
- Estilos con Tailwind, nunca CSS inline
- Endpoints REST: sustantivos en plural, sin verbos
- Migraciones nunca se editan después de aplicadas; se agrega una nueva

---

## Puesta en marcha

```bash
# Backend
cd diabetes-predictor/backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
copy .env.example .env   # y llenar las credenciales de Supabase
.venv/Scripts/uvicorn main:app --reload

# Frontend
cd diabetes-predictor/frontend
npm install
npm run dev
```

---

## Orden de desarrollo
1. Base de datos (PostgreSQL + Supabase) — hecho
2. Backend (FastAPI + contratos) — hecho
3. Frontend (React + Tailwind) — hecho
4. Modelo ML (Jupyter → TensorFlow + Scikit-learn) — **bloqueado**
5. Integración del modelo en `model_service.py` — **bloqueado**
6. Despliegue (Vercel + AWS Lambda) — bloqueado por decisión de arquitectura
7. Evaluación y comparación estadística — bloqueado

---

## Estado actual
Implementado y verificado:
- Esquema SQL con integridad referencial, CHECK de rangos clínicos y de
  suma de probabilidades, índices y triggers de `updated_at`.
- API con 9 endpoints, validación Pydantic y 10 pruebas de humo que pasan.
- Interfaz React con Tailwind que compila y pasa el linter.

Pendiente de decisión del asesor (bloquea el resto):
- Fuente de los datos de entrenamiento.
- Ubicación del modelo: AWS Lambda o dentro del backend.

---

## Limitaciones
- Los datos son de pacientes del municipio de Calpulalpan, Tlaxcala
- Muestra mínima de 1000 registros
- El sistema es herramienta de apoyo al diagnóstico, no reemplaza al médico
- Periodo de datos: 2020–2026
- No se recolectan datos manualmente, se usan bases existentes