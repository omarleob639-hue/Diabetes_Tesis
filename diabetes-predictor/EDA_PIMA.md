# EDA — Pima Indians Diabetes Dataset

Fuente: `data/raw/pima/pima.csv` (UCI / Brownlee mirror), sin encabezado, 9 columnas.

## 1. Dimensiones

- Registros: **768**
- Columnas: **9** (8 predictoras + `resultado`)
- Duplicados exactos: **0**
- Nulos reales (NaN): **0**

## 2. Ceros como valores faltantes disfrazados

En Pima, `0` es clínicamente imposible en varias variables y se usa como marcador de ausencia de dato.

| variable           |   nulos_reales |   ceros |   pct_ceros |   media |   mediana |    min |    max |   nulos_si_cero_es_nulo |
|:-------------------|---------------:|--------:|------------:|--------:|----------:|-------:|-------:|------------------------:|
| embarazos          |              0 |     111 |        14.5 |    3.85 |      3    |  0     |  17    |                       0 |
| glucosa            |              0 |       5 |         0.7 |  120.89 |    117    |  0     | 199    |                       5 |
| presion_diastolica |              0 |      35 |         4.6 |   69.11 |     72    |  0     | 122    |                      35 |
| pliegue_cutaneo    |              0 |     227 |        29.6 |   20.54 |     23    |  0     |  99    |                     227 |
| insulina           |              0 |     374 |        48.7 |   79.8  |     30.5  |  0     | 846    |                     374 |
| imc                |              0 |      11 |         1.4 |   31.99 |     32    |  0     |  67.1  |                      11 |
| funcion_pedigree   |              0 |       0 |         0   |    0.47 |      0.37 |  0.078 |   2.42 |                       0 |
| edad               |              0 |       0 |         0   |   33.24 |     29    | 21     |  81    |                       0 |

- Celdas afectadas (5 variables): **652** (17.0%)
- Filas sin ningún `0` imposible: **392** (51.0%)
- `pliegue_cutaneo` e `insulina` se midieron en subgrupos: su `0` no debe imputarse a la media sin decidir el criterio.

## 3. Distribución de clases

- `resultado = 0` (sin diabetes): **500** (65.1%)
- `resultado = 1` (diabetes): **268** (34.9%)
- Razón de desbalance: **1.87:1**
- La columna es **binaria**: no distingue tipo 1 / tipo 2 / gestacional.

## 4. Correlación con el resultado

- `glucosa`: **0.467**
- `imc`: **0.293**
- `edad`: **0.238**
- `embarazos`: **0.222**
- `funcion_pedigree`: **0.174**
- `insulina`: **0.131**
- `pliegue_cutaneo`: **0.075**
- `presion_diastolica`: **0.065**

- Correlación más alta: `glucosa` (0.467).
- Las cinco variables con más `0` imposibles están entre las más correlacionadas: imputar mal altera el modelo.

## 5. Cobertura de las ocho variables del sistema

| Variable | Cobertura en Pima | Detalle |
| --- | --- | --- |
| Edad | directa | columna `edad` (21-81 años) |
| Sexo | constante | cohorte Pima: solo mujeres ≥21 años; sin variabilidad |
| IMC | directa | columna `imc` |
| Glucosa en ayuno | directa | columna `glucosa` (mg/dL) |
| HbA1c | ausente | Pima no incluye hemoglobina glicosilada |
| Presión sistólica | ausente | Pima solo registra presión diastólica |
| Presión diastólica | directa | columna `presion_diastolica` (mmHg) |
| Antecedentes familiares | proxy | `funcion_pedigree` (score continuo, no sí/no) |

- Directas: **4/8** — Edad, IMC, Glucosa en ayuno, Presión diastólica
- Proxy: **1/8** — Antecedentes familiares
- Sin dato usable: **3/8** — Sexo, HbA1c, Presión sistólica

## 6. Decisión de clases

Pima solo aporta dos etiquetas observables:

| Clase del sistema | ¿Pima la aporta? | Por qué |
| --- | --- | --- |
| `tipo_2` | Sí (parcial) | Cohorte adulta ≥21 años, diagnóstico por glucosa; asumida como tipo 2 por literatura |
| `sano` | Sí (parcial) | `resultado = 0` |
| `tipo_1` | No | Sin edad de inicio, sin autoanticuerpos, sin insulina desde el diagnóstico |
| `gestacional` | No | Solo mujeres no embarazadas en el momento de la medición; sin semana de gestación |

**Con Pima solo se puede entrenar un modelo binario (2 clases) o reetiquetar `tipo_2` como proxy de «diabetes» para una demo de 3-4 clases con clases sintéticas.** Eso último es exactamente lo que el plan de datos descarta: fabricar clases completas con IA.

## 7. Siguiente paso

1. Definir el tratamiento de los `0` imposibles (excluir `pliegue_cutaneo`/`insulina` o imputar por mediana).
2. Cubrir `HbA1c`, `presión sistólica` y `tipo_1`/`gestacional` con datasets reales (FDDB Dinamarca, T1DiabetesGranada, Dryad GDM del sur de China).
3. Decidir 2 vs 4 clases según cuántas fuentes reales se obtengan, no por conveniencia de la demo.
