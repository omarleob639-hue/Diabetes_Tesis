# Solicitud de datasets

Guía para obtener los datasets reales que faltan para el modelo multiclase. Estado y procedimiento de cada fuente.

## Resumen

| Fuente | Clase que aporta | ¿Requiere permiso? | Dificultad | Estado |
|---|---|---|---|---|
| GDM sur de China (Dryad) | `gestacional` + controles sanas | No (acceso abierto; descarga manual) | Baja | ✅ Descargado, verificado y limpio (`data/processed/dryad_gdm_features.csv`) — falta decidir su rol en el modelo |
| T1DiabetesGranada (Zenodo) | `tipo_1` | Sí (permiso manual) | Baja | ⏳ Solicitud enviada — esperando aprobación, luego baja el ZIP |
| FDDB Dinamarca (SDCO) | `tipo_1`, `tipo_2` (las 8 variables) | Sí (proceso institucional) | Alta | ⏳ No contactado (opcional — proceso pesado) |

---

## 1. GDM sur de China (Dryad) — descarga abierta

- **Enlace del dataset:** https://datadryad.org/dataset/doi:10.5061/dryad.rv15dv4j7
- **DOI:** 10.5061/dryad.rv15dv4j7
- **Autoría:** Liang, Qiulian; Sun, Yan; Li, Ming et al. (2024). Publicado el 07-dic-2024.
- **Contenido:** 538 GDM (`Group=1`) + 626 embarazadas sanas (`Group=0`). Datos clínicos: SBP (mmHg), DBP (mmHg), FPG (mmol/L), 1hPG (mmol/L), 2hPG (mmol/L), HbA1c (%), TG, TC, HDL-c, LDL-c (mmol/L) + 5 polimorfismos genéticos.
- **Requiere permiso:** No. Cualquiera lo puede descargar.
- **Cómo descargarlo (manual, el navegador es obligatorio):**
  - Dryad bloquea scripts (protección Anubis); por eso no se puede bajar con `Invoke-WebRequest`. Se descarga a mano:
    1. Abrir en el navegador: `https://datadryad.org/downloads/file_stream/3698481` (CSV, 113 KB).
    2. Abrir en el navegador: `https://datadryad.org/downloads/file_stream/3698487` (README).
    3. Guardar el CSV en `data/raw/dryad_gdm/gdm_south_china.csv`.
- **Advertencias:**
  - **No trae edad ni IMC** (solo aparecen en el paper, no en el CSV depositado). Aporta la clase `gestacional` con controles y las variables que faltaban (presión arterial y HbA1c), pero `edad` e `imc` seguirán sin dato en esa clase.
  - Todo el grupo es femenino (coherente con `gestacional`). No tiene `antecedentes_familiares`.
- **Pasos siguientes:** descargar el CSV, avisar y correr la verificación (EDA) igual que con Pima y Mendeley (revisar nulos, unidades, grupos y cobertura de las 8 variables).

---

## 2. T1DiabetesGranada (Zenodo) — permiso manual

- **Enlace del registro:** https://zenodo.org/records/10050944
- **DOI:** 10.5281/zenodo.10050944
- **Documento de referencia:** Nature Scientific Data — https://www.nature.com/articles/s41597-023-02737-4
- **Contenido:** 736 pacientes con diabetes tipo 1 de Granada; variables clínicas y bioquímicas (edad, sexo, año de nacimiento, parámetros bioquímicos y monitorización continua de glucosa).
- **Requisito:** acceso restringido; hay que aceptar el Data Usage Agreement y enviar solicitud con nombre, email e institución. La solicitud la procesa la **Secretaría del Departamento de Ingeniería del Computador, Automática y Robótica (ICAR)** de la Universidad de Granada.
- **Pasos (vía oficial):**
  1. Crear/iniciar sesión en `zenodo.org`.
  2. Abrir el registro `10.5281/zenodo.10050944` y pulsar el botón **"Request access"** (es el flujo oficial del propio Zenodo).
  3. En el formulario: nombre completo, email, institución y justificación del uso de los datos.
  4. Alternativa por correo: **`icarsecretaria@ugr.es`** (Secretaría del ICAR). Nota: el correo usa direcciones `@ugr.es`; comprobar que la dirección origen acepte respuesta.
- **Plantilla de solicitud (alternativa por correo a `icarsecretaria@ugr.es`):**

  ```
  Asunto: Request access to T1DiabetesGranada dataset (DOI 10.5281/zenodo.10050944)

  Nombre: [NOMBRE]
  Email: [EMAIL]
  Institución: [INSTITUCIÓN]

  Solicito acceso al dataset T1DiabetesGranada para un proyecto de titulación sobre
  evaluación de riesgo de diabetes basado en variables clínicas y bioquímicas.
  Los datos se usarán exclusivamente con fines académicos, se almacenarán de forma
  local y no se compartirán públicamente.

  Justificación del uso: [DESCRIBIR — p. ej. predecir riesgo de diabetes tipo 1 a
  partir de variables como edad, IMC, glucosa, HbA1c y presión arterial].
  ```

- **Dato importante:** trae 736 DM1 reales pero **sin presión arterial**: en el filtro de las 8 variables del sistema cubre 5-6/8. Sirve para la clase `tipo_1`, pero sufrirá la misma carencia de `PAS`/`PAD`/`antecedentes_familiares` que el resto de fuentes.

---

## 3. FDDB Dinamarca (SDCO) — proceso institucional

- **Referencia:** Funen Diabetes Database (FDDB), gestionada por Steno Diabetes Center Odense (SDCO).
- **Documento de referencia:** estudio BMJ Open que usa FDDB.
- **Plataforma:** SDCO projektdatabase — https://sdco.dk/forskning/projektdatabase
- **Contacto:** `ouh.sdco@rsyd.dk`
- **Contenido (según estudios publicados):** ~3,691 DM1 + ~19,085 DM2 con las 8 variables del sistema (incluye presión arterial y HbA1c). Es la única fuente con cobertura completa.
- **Requiere permiso:** Sí, y es un proceso pesado:
  1. Escritura de un protocolo/justificación de 3-4 páginas.
  2. Registro del proyecto ante la institución responsable de los datos en Dinamarca.
  3. Solicitud formal ante Danmarks Statistik y Sundhedsdatastyrelsen.
- **Recomendación:** para una tesis de licenciatura sin afiliación danesa es poco realista. Útil solo como plan C o si se consigue un colaborador en Dinamarca.

---

## Resultados de la verificación del Dryad GDM (2026-10-07)

Archivo: `data/raw/dryad_gdm/gdm_south_china.csv` (113 KB, 1164 filas × 34 columnas).

**Bien:**
- 538 GDM (`Group=1`) + 626 embarazadas sanas (`Group=0`) — coincide con el abstract.
- Columnas usables para el sistema: FPG (mmol/L), SBP (mmHg), DBP (mmHg), HbA1c (%); las demás (TG/TC/HDL/LDL) no se usan.
- Solo 3-5 NaN por variable clínica; el grupo GDM no tiene ningún NaN.

**Problemas detectados:**
1. **7 pacientes duplicados**; en 3 casos (SampleID 292, 636 y 1357) el mismo paciente aparece como GDM Y como control con los mismos valores clínicos (etiquetas contradictorias) → eliminar esas filas ambiguas y deduplicar.
2. **Tipeos imposibles:** DBP=7 y 8 mmHg, HbA1c=1.0-1.1%, TC=0 → tratar como ausentes o imputar.
3. **No trae edad ni IMC** → la clase `gestacional` no puede llenar `edad`/`imc` del contrato del modelo (4 features). Aporta presión, HbA1c y glucosa reales para esa clase, pero **no resuelve el modelo tetraclásico por sí solo** (pendiente: decidir si se usa como fuente parcial o se descarta).

**Listo (limpieza aplicada el 2026-10-07, `backend/notebooks/04_preprocesamiento_dryad.py`):**
- Eliminados los 3 pacientes con etiqueta contradictoria (292, 636, 1357) y 4 filas duplicadas → 1154 registros finales (534 `gestacional` + 620 `embarazada_sana`).
- 6 tipeos imposibles convertidos a NaN (DBP 7/8, HbA1c 1.0-1.1 %, TC=0).
- Salida limpia: `data/processed/dryad_gdm_features.csv` → columnas `SampleID`, `clase` (`gestacional`/`embarazada_sana`), `glucosa_ayuno` (mmol/L), `hba1c` (%), `presion_sistolica` y `presion_diastolica` (mmHg). Los NaN restantes quedan como faltantes (sin imputar).
- **Sigue sin edad ni IMC** → no puede llenar el contrato de 4 features del modelo de demostración. **Pendiente:** decidir si entra como fuente `gestacional` parcial en el tetraclásico.

## Mapa de cobertura (8 variables del sistema)

| Variable | Pima (binario) | Dryad GDM | T1DiabetesGranada | FDDB |
|---|---|---|---|---|
| edad | ✅ | ❌ (solo en el paper) | ✅ | ✅ |
| sexo | ✅ (constante F) | ✅ (constante F) | ✅ | ✅ |
| imc | ✅ | ❌ (solo en el paper) | ❓ | ✅ |
| glucosa_ayuno | ✅ | ✅ (FPG) | ❓ | ✅ |
| hba1c | ❌ | ✅ | ✅ | ✅ |
| PAS | ❌ | ✅ (SBP) | ❌ | ✅ |
| PAD | ✅ | ✅ (DBP) | ❌ | ✅ |
| antecedentes_familiares | ❌ | ❌ | ❌ | ❌ |

- Ninguna fuente entrega `antecedentes_familiares`; sigue siendo un campo del cuestionario del sistema sin dataset público que la cubra.
- Dryad (abierta) es la única fuente accesible hoy y la única que añade presión arterial + HbA1c para la clase `gestacional`.