# Sistema de Predicción de Diabetes — Contexto del Proyecto

> **Actualizado:** 6 de octubre de 2026 · EDA + modelo binario integrado + demo local probada

## ¿Qué es?
Sistema web para la detección temprana de diabetes mellitus desarrollado
como tesis de licenciatura. Predice de manera integrada el tipo de diabetes
con mayor probabilidad en un paciente: tipo 1, tipo 2, gestacional o sano,
utilizando una red neuronal artificial multiclase.

**Estado actual:** la red neuronal multiclase **aún no está entrenada** (el
tetraclásico requiere DM1 y GDM reales con las 8 variables, sin fuente pública
descargada). Se entrenó e integró un **modelo binario de demostración** con
Pima (`sano`/`tipo_2`, 4 variables, exactitud CV 0.763). La UI sigue
funcionando en modo demostración y lo declara en pantalla.

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
| Interfaz | React 19 + Vite | 5 vistas enrutadas con React Router |
| Enrutado | react-router-dom | Navegación cliente, 5 rutas |
| Estilos | Tailwind CSS v4 | Tokens de diseño vía `@theme`, sin CSS inline |
| Hosting frontend | Vercel | **Desplegado** en el proyecto `Universidad` |
| API | FastAPI + Pydantic v2 | Endpoints REST para predicción y pacientes |
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

## Rutas de la interfaz
| Ruta | Vista | Propósito |
|---|---|---|
| `/` | `Inicio` | Portada del proyecto y Presentación institucional |
| `/nueva-prediccion` | `NuevaPrediccion` | Formulario de las 8 variables clínicas |
| `/resultados` | `Resultados` | Clase más probable y desglose de probabilidades |
| `/pacientes` | `Pacientes` | Listado con búsqueda |
| `/historial` | `Historial` | Historial con filtros |

`vercel.json` declara `rewrites` con `/(.*) -> /index.html`. Sin esto,
recargar `/historial` devolvería 404 porque React Router vive en cliente.

---

## Identidad visual
Paleta de carácter institucional, definida como tokens en `index.css`:

| Token | Hex | Uso |
|---|---|---|
| Guinda | `#611232` / `#9D2449` | Encabezado, acentos, franja |
| Dorado | `#A57F2C` / `#B38E5D` | Botones primarios |
| Verde | `#235B4E` | Estado saudável, confirmación |
| Fondo | `#F1F4F8` | Superficies |
| Texto | `#1F2937` | Texto principal |

Tipografías: `Montserrat` para títulos y cifras, `Noto Sans` para cuerpo.

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
7. React muestra el resultado en `pages/Resultados.jsx`

### Fallback automático a modo demostración
`services/datos.js` es la única capa que consume datos. Intenta primero la
API real y, si falla, degrada al mock **declarándolo en pantalla**:

```
pages/* -> services/datos.js -> services/api.js  (VITE_API_BASE_URL)
                              -> services/mock.js (demo, sin backend)
```

Consecuencia práctica: cuando el backend esté desplegado, **no hay que tocar
ningún componente**. La detección es automática.

Variables de entorno del frontend (Vite solo expone prefijos `VITE_`):
| Variable | Valor local | Nota |
|---|---|---|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Única variable soportada |

`VITE_API_URL` **no funciona**: `api.js` lee `VITE_API_BASE_URL`. Estas
variables son públicas por diseño; nunca deben contener secretos.

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
│   ├── notebooks/              EDA/preproc/entrenamiento (Pima demo) ✅
│   └── model/saved_model/      Artefactos .joblib binario demo (gitignored)
├── database/
│   ├── migrations/             SQL versionado (001_esquema_inicial.sql)
│   └── seeds/                  Datos de prueba
├── data/
│   ├── raw/                    Dataset original (bloqueado)
│   └── processed/              Dataset limpio (bloqueado)
└── frontend/
    ├── src/
    │   ├── components/         Header, Card, Field, ProbabilityBar
    │   ├── pages/              Inicio, NuevaPrediccion, Resultados,
    │   │                       Pacientes, Historial
    │   ├── services/           api.js, mock.js, datos.js (capa única)
    │   ├── constants/          clinico.js (paleta, clases, variables)
    │   ├── context/            prediccion.js, ProveedorPrediccion.jsx
    │   ├── App.jsx             Rutas
    │   └── main.jsx            BrowserRouter
    ├── vercel.json             Build Vite + rewrites SPA
    └── .env.example            Documenta VITE_API_BASE_URL
```

Los componentes antiguos `FormularioPaciente.jsx` y `ResultCard.jsx` se
eliminaron al migrar a vistas enrutadas con contexto compartido.

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
- En Tailwind v4, `@utility` **no** acepta pseudo-selectores:
  se escribe `&:hover` dentro del bloque, nunca `@utility x:hover`
- Node 22 declarado en `package.json`; Vercel usa esa versión
- Los cambios de tesis viven fuera de los commits del sistema

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
1. Base de datos (PostgreSQL + Supabase) — **hecho**
2. Backend (FastAPI + contratos) — **hecho**
3. Frontend (React + Tailwind + React Router) — **hecho y desplegado**
4. Modelo ML (Jupyter → TensorFlow + Scikit-learn) — **parcial: binario demo (Pima) hecho, tetraclásico bloqueado**
5. Integración del modelo en `model_service.py` — **hecho para el binario**
6. Despliegue del backend (AWS Lambda) — **pendiente**
7. Evaluación y comparación estadística — **bloqueado**

---

## Estado actual
Implementado y verificado:
- Esquema SQL con integridad referencial, CHECK de rangos clínicos y de
  suma de probabilidades, índices y triggers de `updated_at`.
- API con 9 endpoints, validación Pydantic y 10 pruebas de humo que pasan.
- Interfaz React con Tailwind que compila y pasa el linter.
- Las 5 rutas responden 200 y los 17 módulos del grafo de imports compilan.
- Build en 505 ms; bundle de 285 kB (89 kB gzip).
- Desplegado en Vercel, proyecto `Universidad`.
- **Demo local verificada de punta a punta** (6 oct): backend FastAPI con el
  modelo binario real + frontend en dev. Casos comprobados: diabético →
  `tipo_2` (p=0.993), sano → `sano` (p=0.992), frontera (glucosa 120, IMC 28)
  → `tipo_2` (p=0.598).

### Probar la demo localmente (modelo binario real)
```powershell
# 1. Backend (usa SQLite local; modelos ya creados en test.db)
cd diabetes-predictor/backend
$env:DATABASE_URL='sqlite:///./test.db'; $env:MODEL_STUB_ENABLED='false'
.venv\Scripts\python.exe -c "from db.base import engine; from db.models import Base; Base.metadata.create_all(bind=engine)"
.venv\Scripts\uvicorn main:app --host 127.0.0.1 --port 8000

# 2. Frontend (otro terminal)
cd diabetes-predictor/frontend
npm run dev
# Abrir http://127.0.0.1:5173/
```
Nota dev: `sqlite:///./test.db` es SOLO para la demo local; en producción se
aplican las migraciones SQL a Supabase (PostgreSQL).

---

## Plan de trabajo — sesión del 6 de octubre

Decidido hoy: **descargar Pima y arrancar el EDA + entrenamiento.** El resto
queda en lista; estos son los pasos.

### Paso 1 — Descargar Pima ✅ hecho (6 oct)
- Pima Indians Diabetes, 768 registros, 8 variables. UCI / Kaggle.
- Destino: `data/raw/pima/pima.csv` (23.3 KB, sin encabezado, 9 columnas).
- MD5 `85e73c52eccb545102f43b2db03533f6`, espejo de Brownlee, 768 filas.
- `data/raw/*` está en `.gitignore`: **el CSV no viaja a git.**

### Paso 2 — EDA ✅ hecho (6 oct)
Script reproducible: `backend/notebooks/01_exploracion_pima.py`
Informe completo: `EDA_PIMA.md`. Resumen:

- **Ceros disfrazados: 652 celdas (17.0 %)** en 5 variables —
  `insulina` 374 (48.7 %), `pliegue_cutaneo` 227 (29.6 %),
  `presion_diastolica` 35, `imc` 11, `glucosa` 5.
  Solo **392 filas (51 %)** están limpias de todo `0` imposible.
- Nulos reales (NaN): 0. Duplicados: 0.
- Clases: `sano` 500 (65.1 %), `diabetes` 268 (34.9 %), desbalance 1.87:1.
- Correlación con el desenlace: `glucosa` 0.467 > `imc` 0.293 >
  `edad` 0.238 > `embarazos` 0.222 > `funcion_pedigree` 0.174 >
  `insulina` 0.131 > `pliegue_cutaneo` 0.075 >
  `presion_diastolica` 0.065.
- **Cobertura de las 8 variables del sistema: 4 directas** (edad, IMC,
  glucosa en ayuno, presión diastólica) + 1 proxy (`funcion_pedigree`
  por antecedentes familiares) + 3 sin dato usable (sexo constante=F,
  **HbA1c ausente**, **presión sistólica ausente**).
- **Sin gráficos dentro del repo:** son datos de terceros.

### Paso 3 — Decidir 3 vs 4 clases ⏳ pendiente, con números
Lo que Pima aporta y lo que no:

| Clase | ¿Pima? | Por qué |
|---|---|---|
| `tipo_2` | Sí, parcial | adultas ≥21 años, dx por glucosa; asumida tipo 2 por literatura |
| `sano` | Sí, parcial | `resultado = 0` |
| `tipo_1` | **No** | sin edad de inicio, sin autoanticuerpos, sin insulina desde el dx |
| `gestacional` | **No** (Pima) | sin semana de gestación; el control quedaba sin fuente |

Con Pima **solo hay 2 etiquetas observables**. La vía triclásica
(`sano` / `prediabetes` / `diabetes`) es la defendible con lo que hay hoy:
`prediabetes` se puede derivar de umbrales reales sobre `glucosa` e `imc`,
no hace falta inventar filas. La tetraclásica **exige DM1 real + GDM real
con controles**. En el 7-oct se cerró parte del hueco: el **Dryad GDM del sur
de China** aporta 534 `gestacional` + 620 embarazadas sanas (con HbA1c y
presión), y la solicitud de **T1DiabetesGranada** (DM1) está **enviada**. La
decisión final se toma al cerrar esos candidatos, no por conveniencia de la demo.

### Paso 4 — Preprocesamiento ✅ hecho para el binario demo
- Imputar ceros inválidos con la mediana **por grupo** en `02_preprocesamiento_pima.py`.
- Estandarizar con `StandardScaler`.
- **Split por sujeto, nunca por fila** (ver nota de leakage abajo).

### Paso 5 — Entrenar y evaluar ✅ hecho para el binario demo (Pima)
- Red neuronal **MLP de scikit-learn** (sin ruedas de TF para Py 3.13): `03_entrenamiento_pima.py`.
- Validación cruzada estratificada 5-fold (0.763 ± 0.025).
- Métricas por clase, matriz de confusión y sanidad impresas en consola.
- **Pendiente para el tetraclásico:** TensorFlow/Keras, split 70/15/15, F1 ≥ 0.80.

### Paso 6 — Exportar a ONNX
Reduce tamaño y cold start frente a TensorFlow crudo. Necesario si el
backend va a AWS Lambda.

### Paso 7 — Integrar y publicar
- Cargar el modelo en `services/model_service.py`.
- Quitar el banner de "datos de demostración".
- Desplegar el backend y apuntar `VITE_API_BASE_URL` a la URL real.

### Datos ya descargados
| Ubicación | Contenido | Veredicto |
|---|---|---|
| `data/raw/pima/pima.csv` | Pima, 768 filas, binario | **Base de la demo**: `sano` 500 / `tipo_2` 268 |
| `data/raw/diabetes_datasets.zip` | Shanghai T1DM + T2DM, CC BY 4.0 | **No sirve**: 7 de 8 variables ausentes |
| `data/raw/figshare_shanghai/` | Descomprimido, 16 + 109 archivos | Solo CGM e insulina |
| `%USERPROFILE%\Downloads\Master_data_GDM.xlsx` | GDM Mendeley, 813 filas | **Descartado**: sin presión arterial, sin controles (809/813 tratados) y **valores alterados entre hojas** (`fbs` 113→89, `Hba1c` 6.5→5.9, `gtt2` 329→199) |
| `data/raw/dryad_gdm/gdm_south_china.csv` | GDM sur de China, 1164 filas | **Usado (parcial)**: tras limpieza quedan 534 `gestacional` + 620 `embarazada_sana` con HbA1c y presión → `data/processed/dryad_gdm_features.csv`. **Sin edad/IMC** |

Limpieza del Dryad: `backend/notebooks/04_preprocesamiento_dryad.py`
(elimina 3 pacientes con etiqueta contradictoria y 4 filas duplicadas;
6 tipeos imposibles pasan a NaN). Ver `SOLICITUD_DATASETS.md`.

Shanghai contiene únicamente `Date`, `CGM (mg/dl)`, `CBG (mg/dl)`,
`Blood Ketone`, `Dietary intake`, `Insulin dose`, `CSII basal/bolus`.
No hay edad, sexo, IMC, HbA1c, presión ni antecedentes familiares: es
monitorización continua, no cribado.

### Candidatos revisados el 6 de octubre
| Candidato | Cobertura | Estatus |
|---|---|---|
| T1DiabetesGranada (Zenodo) | 736 DM1, edad, sexo, glucosa, HbA1c. **Sin presión arterial** | ✅ Solicitud enviada (7-oct) a la Secretaría del ICAR |
| GDM sur de China (Dryad) | 538 GDM + 626 embarazadas sanas; SBP, DBP, FPG, HbA1c e lípidos. **Sin edad/IMC** | ✅ Descargado, verificado y limpio (7-oct) |
| FDDB Dinamarca | **Las 8 variables**; 3,691 DM1 + 19,085 DM2 | Solicitud formal a Odense Univ. (no contactado — ver `SOLICITUD_DATASETS.md`) |
| Bimodal Shanghai 2026 | 5,922 pacientes, 190 atributos, antecedentes familiares | Solo diabéticos, sin sanos |

Conclusión: **no existe dataset público descargable con las 8 variables +
DM1 + DM2 + sano + gestacional.** La DM1 se diagnostica en la infancia con
criterios clínicos que rara vez se publican tabulados.

### Nota crítica: data leakage
Los datasets longitudinales traen **varias filas por paciente**
(`1002_0`, `1002_1`, `1002_2` son el mismo sujeto). Un split por fila mete
al mismo paciente en train y test y la exactitud sube artificialmente.
**Siempre agrupar por paciente.**

### Nota ética
Los datos de terceros son registros clínicos identificables; los nombres de
archivo son IDs internos de hospital. Reglas:
- Todo el análisis ocurre **en la máquina local**.
- **Nunca** subirlos a GitHub, Vercel ni servicios externos de IA.
- En la tesis: solo el link de la fuente, cero filas de pacientes.
- Citar la licencia. Shanghai es CC BY 4.0.

---

## Lo que falta
### 1. Frontend — listo, sin bloqueos
Copy corregido: `Inicio` ya **no afirma** que el modelo fue entrenado con
datos de Calpulalpan (commit `171c126`). Ahora declara que es una versión de
demostración con datos de referencia. Queda pendiente revisar
`tesis/Capitulo1.tex`, `Capitulo2.tex` y `tesis_diabetes_resumen.md`, que
repiten la misma afirmación.

### 2. Backend — bloqueado en Vercel
`VITE_API_BASE_URL=http://localhost:8000` no existe desde Vercel, por eso
aparece *Failed to fetch*. Mientras tanto el sistema cae al mock.

Opciones para el backend, sin decisión tomada:
| Opción | A favor | En contra |
|---|---|---|
| AWS Lambda + Lambda Web Adapter | Barato si casi no hay tráfico | Cold starts (~2-4 s con ONNX) |
| AWS App Runner / ECS | Sin cold starts, contenedor nativo | Costo por Always-On |
| Mantener local | Costo cero | No es público |

Recomendación previa: **exportar el modelo a ONNX y servirlo en Lambda**.
Reduce el tamaño y el arranque respecto a TensorFlow crudo.

### 3. Modelo ML — demo binaria lista, tetraclásico bloqueado por datos
**Modelo binario de demostración (Pima) — entrenado e integrado (6 oct).**
Pipeline reproducible en `backend/notebooks/`:
`01_exploracion_pima.py` → `02_preprocesamiento_pima.py` →
`03_entrenamiento_pima.py`.

- **Features (4):** `edad`, `imc`, `glucosa_ayuno`, `presion_diastolica`.
  Pima no registra `hba1c`, `presión sistólica` ni variabilidad de `sexo`;
  el formulario las recibe pero el modelo de demostración no las usa
  (documentado en docstring de `model_service.py` y en `EDA_PIMA.md`).
- **Imputación:** 51 `0` imposibles (glucosa 5, imc 11, PAD 35) imputados
  con la **mediana por grupo** (outcome), no la global.
- **Modelo:** MLP de scikit-learn `(32,16,8)`, escalado con `StandardScaler`,
  todos ajustados dentro de cada fold (sin leakage).
- **Validación:** 5 folds estratificados.
  - Exactitud media: **0.763 ± 0.025**
  - F1: `sano` 0.82 (prec 0.82 / rec 0.82) — `tipo_2` 0.66 (prec 0.66 / rec 0.66)
  - Matriz de confusión agregada: `[[410 90] [92 176]]`
  - Sanidad: glucosa alta + IMC alto → `tipo_2` (p=0.98); perfil sano → `sano`
    (p=0.997); frontera (glucosa 118, IMC 27) → `sano` por poco (p=0.55).
- **Por qué sklearn y no TensorFlow:** no hay ruedas oficiales de TF para
  Python 3.13 en Windows (nota en `requirements.txt`). El MLP cumple la
  condición de "red neuronal" de la tesis; el tetraclásico en Keras `.h5` se
  servirá cuando existan los datos (la capa de carga ya lo soporta).
- **Honestidad del demo:** la salida es binaria. `tipo_1` y `gestacional` se
  devuelven en **0.0**: el modelo NO las predice y no se fabrican.
  Artefactos `.joblib` fuera de git (`*.joblib` en `.gitignore`).

**El cuello de botella real sigue aquí para las 4 clases.** El filtro de
candidatos está en `FILTRO_DATASETS.md`. Resumen de lo revisado:

| Candidato | Problema |
|---|---|
| Pima Indians | Aporta `sano` (500) y `tipo_2` (268); no DM1 ni gestacional |
| GDM India (Cho et al.) | **Solo casos GDM.** Sin controles, sin sensores, mezcla DM1/DM2 |
| Shanghai T1DM/T2DM (figshare) | **Descargado y descartado.** Solo CGM e insulina; 7 de 8 variables ausentes |
| T1DiabetesGranada | El más cercano a DM1 (736). **Solicitud enviada (7-oct)**; pendiente de acceso |
| GDM sur de China (Dryad) | **Descargado y limpio (7-oct)**: `gestacional` (534) + `embarazada_sana` (620); HbA1c, SBP, DBP, FPG. Falta `edad`/`imc` |
| FDDB Dinamarca | Tiene las 8 variables y 3,691 DM1; solicitud formal, no descarga |
| Prontuario Brasil (DM1/2) | Acceso restringido, mezcla DM1 y DM2 |
| PMC9954149 | **No usar**: sus clases GDM fueron fabricadas |

Reglas acordadas:
- **Nunca fabricar una clase completa con IA.** Se puede sintetizar una
  clase minoritaria para balancear, pero debe documentarse.
- Sin DM1 real, la clasificación tetraclásica **no es defendible**. Una
  opción metodológica más sólida sería triclásica (`sano`/`prediabetes`/
  `diabetes`) mientras no exista DM1.
- Mezclar datasets crea *confounding* de población y de fuente de medición.
  Solo 3 variables son comparables entre Pima y el set gestacional.

### 4. Base de datos — sin validar en producción
Migraciones escritas pero **nunca aplicadas** a Supabase: no hay Docker ni
`psql` en el entorno.

### 5. CI — no verificado
El workflow existe en `.github/workflows/test.yml` pero **no se ha corrido**:
`gh` no está instalado. Antes del commit se verificó localmente (10 pruebas
backend, Ruff, lint y build frontend).

### 6. Housekeeping
Hay una **copia obsoleta del proyecto** en
`Desktop\omar\omar\Titulación\diabetes-predictor\frontend` (scaffold de
agosto, Tailwind 3, sin `vercel.json`). No contiene nada del diseño actual.
No borrar sin revisar antes: podría tener trabajo propio.

Detalle: el `.gitignore` excluye `data/`, así que ni el ZIP de Shanghai ni
`pima.csv` **están en git**. Correcto desde el punto de vista ético, pero
significa que no están en GitHub: si se pierde el disco, hay que volver a
bajarlos de la fuente (el EDA sí está versionado:
`backend/notebooks/01_exploracion_pima.py`).

---

## Limitaciones
- **Modelo tetraclásico sin entrenar**: las clases `tipo_1` y `gestacional`
  no tienen fuente con las 8 variables; el modelo actual es binario de
  demostración (`sano`/`tipo_2`, 4 variables, exactitud CV 0.763) y devuelve
  0.0 en las dos clases que no puede predecir. Avance del 7-oct: el **Dryad
  GDM** cubre `gestacional` + controles embarazadas con HbA1c y presión
  (pero sin `edad`/`imc`), y la solicitud de **T1DiabetesGranada** (DM1)
  está enviada a la Secretaría del ICAR.
- El modelo de demostración **ignora** `sexo`, `hba1c`, `presión sistólica` y
  `antecedentes familiares`: Pima no los registra.
- Los datos son de pacientes del municipio de Calpulalpan, Tlaxcala
  *(afirmación de la tesis, **sin respaldar todavía**: los datasets usados
  hasta hoy son Pima/UCI y fuentes públicas de terceros)*
- Muestra mínima de 1000 registros
- El sistema es herramienta de apoyo al diagnóstico, no reemplaza al médico
- Periodo de datos: 2020–2026
- No se recolectan datos manualmente, se usan bases existentes