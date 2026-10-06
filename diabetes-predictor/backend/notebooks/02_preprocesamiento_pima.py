"""Preprocesamiento del dataset Pima para el modelo binario de demostración.

Uso:
    backend/.venv/Scripts/python.exe backend/notebooks/02_preprocesamiento_pima.py

Decisión (documentada en EDA_PIMA.md):
- Se conservan 4 variables del contrato del sistema con dato directo en Pima:
  `edad`, `imc`, `glucosa_ayuno` y `presion_diastolica`.
- `insulina` y `pliegue_cutaneo` se descartan (no son variables del sistema y su
  `0` es un subgrupo sin medición, 48.7 % y 29.6 % de ceros).
- `funcion_pedigree` se descarta porque no es `antecedentes_familiares` (bool).
- En Pima no existen `hba1c`, `presion_sistolica` ni variabilidad de `sexo`;
  el backend las recibe del formulario pero el modelo de demostración no las usa.
- Los `0` clínicamente imposibles en `glucosa`, `imc` y `presion_diastolica` se
  imputan con la mediana del grupo (outcome), no la global, para no sesgar la
  distribución por clase.

No se sube ninguna fila a git: `data/processed/*` está en `.gitignore`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw" / "pima" / "pima.csv"
SALIDA = RAIZ / "data" / "processed" / "pima_features.csv"

COLUMNAS_RAW = [
    "embarazos",
    "glucosa",
    "presion_diastolica",
    "pliegue_cutaneo",
    "insulina",
    "imc",
    "funcion_pedigree",
    "edad",
    "resultado",
]

CERO_IMPOSIBLE = ["glucosa_ayuno", "presion_diastolica", "imc"]

FEATURES_CONTRATO = ["edad", "imc", "glucosa_ayuno", "presion_diastolica"]


def cargar() -> pd.DataFrame:
    df = pd.read_csv(RAW, header=None, names=COLUMNAS_RAW)
    df = df.rename(columns={"glucosa": "glucosa_ayuno"})
    return df


def imputar_por_grupo(df: pd.DataFrame) -> pd.DataFrame:
    imputadas = 0
    for col in CERO_IMPOSIBLE:
        df[col] = df[col].astype(float)
        mascara = df[col] == 0
        n = int(mascara.sum())
        if n == 0:
            continue
        mediana_grupo = df.loc[~mascara & (df[col] != 0)].groupby("resultado")[col].median()
        df.loc[mascara, col] = df.loc[mascara, "resultado"].map(mediana_grupo)
        imputadas += n
    return df, imputadas


def main() -> None:
    df = cargar()
    inicial = len(df)
    df, imputadas = imputar_por_grupo(df)
    salida = df[FEATURES_CONTRATO + ["resultado"]].copy()

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    salida.to_csv(SALIDA, index=False)

    print(f"Registros cargados: {inicial}")
    print(f"Ceros imputados con mediana de grupo: {imputadas}")
    print(f"Columnas: {list(salida.columns)}")
    print(f"Distribución resultado: {dict(salida['resultado'].value_counts())}")
    print("\nDescripción de la salida:")
    print(salida[FEATURES_CONTRATO].describe().to_string())
    print(f"\n[ok] escrito en {SALIDA}")


if __name__ == "__main__":
    main()