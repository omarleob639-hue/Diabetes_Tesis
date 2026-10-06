# Sistema de Predicción de Diabetes — Contexto del Proyecto

> **Actualizado:** 5 de octubre de 2026 · commit `cee87d2` desplegado en Vercel

## ¿Qué es?
Sistema web para la detección temprana de diabetes mellitus desarrollado
como tesis de licenciatura. Predice de manera integrada el tipo de diabetes
con mayor probabilidad en un paciente: tipo 1, tipo 2, gestacional o sano,
utilizando una red neuronal artificial multiclase.

**Estado crítico:** la interfaz está publicada, pero la red neuronal **no está
entrenada**. El sistema opera con datos de demostración y lo declara en
pantalla. Ninguna predicción mostrada es un resultado real del modelo.

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
│   ├── notebooks/              Experiments (bloqueado)
│   └── model/saved_model/      Modelo entrenado (bloqueado)
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
4. Modelo ML (Jupyter → TensorFlow + Scikit-learn) — **bloqueado**
5. Integración del modelo en `model_service.py` — **bloqueado**
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
| `gestacional` | **No** | sin semana de gestación, sin controles embarazadas sanas |

Con Pima **solo hay 2 etiquetas observables**. La vía triclásica
(`sano` / `prediabetes` / `diabetes`) es la defendible con lo que hay hoy:
`prediabetes` se puede derivar de umbrales reales sobre `glucosa` e `imc`,
no hace falta inventar filas. La tetraclásica **exige DM1 real + GDM real
con controles**, que siguen sin fuente descargada. La decisión final se toma
al cerrar los candidatos de FDDB/Dryad, no por conveniencia de la demo.

### Paso 4 — Preprocesamiento
- Imputar ceros inválidos con la mediana por columna.
- Estandarizar con `StandardScaler`.
- **Split por sujeto, nunca por fila** (ver nota de leakage abajo).

### Paso 5 — Entrenar y evaluar
- Red neuronal en TensorFlow / Keras.
- Split estratificado 70/15/15.
- Validación cruzada k-fold.
- Métricas: exactitud, sensibilidad, especificidad, F1 por clase,
  matriz de confusión multiclase, tasa de falsos positivos.

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

Shanghai contiene únicamente `Date`, `CGM (mg/dl)`, `CBG (mg/dl)`,
`Blood Ketone`, `Dietary intake`, `Insulin dose`, `CSII basal/bolus`.
No hay edad, sexo, IMC, HbA1c, presión ni antecedentes familiares: es
monitorización continua, no cribado.

### Candidatos revisados el 6 de octubre
| Candidato | Cobertura | Estatus |
|---|---|---|
| T1DiabetesGranada (Zenodo) | 736 DM1, edad, sexo, glucosa, HbA1c. **Sin presión arterial** | Requiere permiso manual |
| FDDB Dinamarca | **Las 8 variables**; 3,691 DM1 + 19,085 DM2 | Solicitud formal a Odense Univ. |
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

### 3. Modelo ML — bloqueado por datos
**Este es el cuello de botella real.** El filtro de candidatos está en
`FILTRO_DATASETS.md`. Resumen de lo revisado:

| Candidato | Problema |
|---|---|
| Pima Indians | Aporta `sano` (500) y `tipo_2` (268); no DM1 ni gestacional |
| GDM India (Cho et al.) | **Solo casos GDM.** Sin controles, sin sensores, mezcla DM1/DM2 |
| Shanghai T1DM/T2DM (figshare) | **Descargado y descartado.** Solo CGM e insulina; 7 de 8 variables ausentes |
| T1DiabetesGranada | El más cercano a DM1. Requiere permiso manual; **no descargado** |
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
- El modelo no está entrenado: hoy el sistema **no predice**, simula.
- Los datos son de pacientes del municipio de Calpulalpan, Tlaxcala
  *(afirmación de la tesis, **sin respaldar todavía**: los datasets usados
  hasta hoy son Pima/UCI y fuentes públicas de terceros)*
- Muestra mínima de 1000 registros
- El sistema es herramienta de apoyo al diagnóstico, no reemplaza al médico
- Periodo de datos: 2020–2026
- No se recolectan datos manualmente, se usan bases existentes