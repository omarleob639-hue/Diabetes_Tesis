# Filtro de admision de datasets

Regla de decision para evaluar un dataset sin depender de un tercero. Basado en los datasets ya revisados: Pima/NIDDK, gestacional India, prontuario DM1 Brasil, DTD, registro indio 323,145, Dryad GDM sur de China.

## Las 5 preguntas

Responde en orden. Si fallas la 1 o la 2, descarta sin seguir leyendo.

### 1. Tiene alguna medida de glucosa?

Busca `Glucose`, `FBS`, `gtt2`, `OGTT`, `BloodGlucose`.

Si NO hay glucosa, **descarta**. Sin glucosa el modelo solo correlaciona edad, sexo y origen. El prontuario DM1 de Brasil fallo aqui: 7 columnas de "edad" distintas, cero glucosa.

### 2. Tiene la etiqueta por registro?

Debe existir una columna que diga que tipo de diabetes es CADA fila.

Senales de que la etiqueta NO existe:
- Columnas que presuponen el diagnostico: `Weeks_gdm_diag`, `Initial_treatment`, `FT_treatment`.
- Una sola columna binaria "diabetes si/no" sin desglose de tipo.

Si solo tienes "diabetes / no diabetes", tienes un dataset binario, no multiclase.

### 3. Tiene controles sanos de la MISMA poblacion?

El fallo clasico: la clase `sano` viene de Pima (mujeres NO embarazadas) y `gestacional` de mujeres SI embarazadas. El modelo nunca ve una mujer embarazada sana, que es justo el caso que debe clasificar bien.

Si el dataset no tiene grupo control, solo sirve como fuente de una clase positiva.

### 4. La edad se solapa con los demas datasets?

Si una clase es solo ninos y otra solo adultos >35, el modelo aprende "es menor de 30 → tipo 1" sin mirar la glucosa. Da 100% de exactitud y no significa nada.

Chequeo: `df['edad'].describe()` por clase. Si un rango no se solapa con otro, para.

### 5. Interseccion de variables >= 5

Cuenta cuantas columnas sobreviven al cruzar TODOS tus datasets.

Ejemplo real con Pima + gestacional India:

| Variable | Pima | GDM India | Comparable |
|---|---|---|---|
| Edad | `Age` | `Age_at_gdm` | Si |
| IMC | `BMI` | `Prepreg_bmi` | Depende: pregestacional |
| Glucosa | 2h post-SOOG | `fbs` ayunas | **No**: mediciones distintas |
| Anteced. fam. | pedigree 0.0-2.4 | `FH_DM` si/no | **No**: no es lo mismo |
| HbA1c | No | `Hba1c` | Solo en uno |
| Presion | solo diastolica | No | Solo en uno |

Resultado: 3 variables utilizables. Con 3 variables y 4 clases no hay tesis.

Si da menos de 5, el dataset no salva el proyecto.

## Chequeo rapido: 30 segundos

Si solo puedes mirar dos columnas, que sean:

1. La de glucosa.
2. La de la etiqueta.

Si la de etiqueta no existe, ya tienes la respuesta.

## Trampas de fuga de datos

Columnas que parecen predictores pero describen el resultado del diagnostico:

- Tiempos y dosis de tratamiento: `Initial_Total_dose`, `FT_treatment`.
- Semana de diagnostico: `Weeks_gdm_diag`.
- Resultado perinatal y neonatal: `Baby_wt`, `LBW`, `Macrosomy`, `Preterm`, `Death`, `Sex_baby`, `Gestational_age`, `Mode_delivery`.
- Complicaciones: `Neonatal_complications`, `Hypoglycemia`, `Maternal_complications`.
- Variables derivadas del objetivo: `Age_cat`, `Bmi_cat`, `Week_gdm_diag_cat`.

Si metes cualquiera de estas, predices una consecuencia del diagnostico, no el diagnostico. La exactitud sube a 99% y el modelo es basura.

## Confusiones de nombres

- `Sex_baby` es sexo del bebe, no de la madre. `sexo` en el formulario es la paciente.
- `Insulin` en Pima es insulina serica a 2h, no el tratamiento.
- `BloodPressure` en Pima es SOLO la diastolica. No hay sistolica.
- `DiabetesPedigreeFunction` es score continuo 0.0-2.4, no antecedente si/no.
- `Hba1c` y glucosa en ayunas son criterios de diagnostico de DMG: sirven para DETECTAR, no para PREDECIR que aparecera.

## Nota sobre Pima

768 mujeres Pima de Arizona, todas mayores de 21. Binario DM2/sano.

- `Glucose` es glucosa plasmatica 2 h despues de SOOG, no en ayunas.
- `Outcome`: 0 = no diabetes (500), 1 = diabetes (268). **Esta proporcion se invierte con frecuencia en la literatura.**
- Ceros que son faltantes: `Insulin` 374, `SkinThickness` 227, `BloodPressure` 35, `BMI` 11, `Glucose` 5.
- No tiene `sexo`, ni `HbA1c`, ni presion sistolica.
- Pima 2016 (`class_0`/`class_1`) es otra version: :-1, ternarios y 0 en `Glucose`, `BloodPressure`, `BMI`, `Age`, `Pregnancies`. Distinto dataset, no lo mezcles con el de 768.

## Lo ya descartado, con motivo

| Dataset | Motivo |
|---|---|
| DM1 prontuario (Brasil, portugues) | Sin glucosa, sin HbA1c, sin presion, sin IMC adulto. Pediactrico. |
| DM1 publicos con CGM (DiaData, OhioT1DM, REPLACE-BG, WISDM, ShanghaiT1DM) | Time-series de monitorizacion continua en personas YA diagnosticadas. No son cribado. Sin grupo control. |
| GDM Dryad sur de China | No descartado: ver "Evaluacion Dryad GDM" abajo. |
| DTD (4 tipos, 99.98%) | Mezcla 4 fuentes, fuga por edad, conteos inconsistentes. |
| MIDO GDM (1709, CIME) | Sin grupo control. |
| Registro indio 323,145 pacientes | Unica base con los 4 tipos. Portal privado de pago, no CSV. |

## Evaluacion Dryad GDM (sur de China) — 2026-10-07

Dataset abierto (DOI 10.5061/dryad.rv15dv4j7): 538 GDM + 626 embarazadas sanas, con FPG, HbA1c, SBP, DBP, lípidos y genotipos. Descargado, verificado y limpiado (`backend/notebooks/04_preprocesamiento_dryad.py`; ver `SOLICITUD_DATASETS.md`).

| Pregunta del filtro | Resultado |
|---|---|
| 1. ¿Tiene glucosa? | **Sí** — FPG, 1hPG y 2hPG (mmol/L) |
| 2. ¿Etiqueta por registro? | **Sí** — `Group` 1=GDM, 0=control |
| 3. ¿Controles sanos de la misma poblacion? | **Sí** — 626 embarazadas sin GDM: justo el control que Pima no tiene para `gestacional` |
| 4. ¿Edad solapada? | **No evaluable** — el CSV no trae edad (solo el paper); tampoco IMC |
| 5. Variables utilizables | 4 variables del sistema (FPG, HbA1c, SBP, DBP) — falta `edad`/`imc` |

**Veredicto:** fuente parcial válida para la clase `gestacional` (+ control embarazada sana). **No** puede llenar el contrato de 4 features (edad/imc ausentes). Decisión de rol en el tetraclásico: pendiente.

Nota de calidad: 3 pacientes aparecían etiquetados a la vez como GDM y control con los mismos valores (eliminados); había DBP=7-8 mmHg, HbA1c=1.0-1.1 % y TC=0 (tipeos a NaN).

## Sobre T1DiabetesGranada

No está "descartado" en sí: es un **registro de CGM de pacientes YA diagnosticados de DM1** (736), lo que lo hace inadecuado como cribado o como control — pero sí **sirve como fuente de la clase `tipo_1`** (edad, sexo, glucosa, HbA1c; sin presión arterial). El 7-oct se envió la solicitud de acceso a la Secretaría del ICAR (UGR). Pendiente: cuando llegue el ZIP, re-evaluar si conviene frente a FDDB.

## Sobre el articulo de 97% de exactitud

PMC9955149 reporta 97% clasificando normal/T1D/T2D/gestacional. Su metodo:

> "the datasets for gestational diabetes were extracted from type 1 and type 2 datasets"

Fabrico el dataset gestacional derivandolo de pacientes de tipo 1 y 2. Es circular, y por eso el numero es tan alto. El mismo articulo describe Pima al reves (500 positivas / 268 negativas).

Se cita como antecedente, pero no sus resultados.