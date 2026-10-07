"""Preprocesamiento del dataset Dryad "GDM southern China" (DOI 10.5061/dryad.rv15dv4j7).

Uso:
    backend/.venv/Scripts/python.exe backend/notebooks/04_preprocesamiento_dryad.py

Decisión (documentada en SOLICITUD_DATASETS.md, "Resultados de la verificación"):
- Aporta las clases `gestacional` (Group=1) y embarazada sana/control (Group=0),
  y las variables del sistema con dato real: glucosa en ayunas (FPG), PAS (SBP),
  PAD (DBP) y HbA1c.
- NO trae `edad` ni `imc` (solo están en el paper, no en el CSV): este dataset no
  puede llenar el contrato de 4 features del modelo de demostración; por eso no se
  define una salida "lista para entrenar", solo la tabla clínica limpia.
- Limpieza aplicada:
  - Se eliminan 3 pacientes (SampleID 292, 636, 1357) que aparecen a la vez como
    Group 1 y Group 0 con los mismos valores clínicos (etiqueta contradictoria).
  - Se deduplican los 4 pacientes restantes con SampleID repetido (se conserva la
    primera fila).
  - Los tipeos sin sentido fisiológico se convierten a NaN: DBP<=30 mmHg,
    HbA1c<=2.5 % y TC==0 (valores tipo "7", "1.0", "1.1").
  - Los NaN restantes se dejan como faltantes (no se imputan: decidir en la
    integración del tetraclásico).

No se sube a git: `data/raw/*` y `data/processed/*` están en `.gitignore`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw" / "dryad_gdm" / "gdm_south_china.csv"
SALIDA = RAIZ / "data" / "processed" / "dryad_gdm_features.csv"

COLUMNA_CLASE = "Group"  # 1=GDM, 0=control

COLUMNAS_CLINICAS = {
    "FPG(mmol/L)": "glucosa_ayuno",
    "HbA1c(%)": "hba1c",
    "SBP(mmHg)": "presion_sistolica",
    "DBP(mmHg)": "presion_diastolica",
    "1hPG(mmol/L)": "_ogtt_1h_no_usar",
    "2hPG(mmol/L)": "_ogtt_2h_no_usar",
    "TG (mmol/L)": "_tg_no_usar",
    "TC(mmol/L)": "_tc_no_usar",
    "HDL-c(mmol/L)": "_hdl_no_usar",
    "LDL-c(mmol/L)": "_ldl_no_usar",
}

CONTRADICTORIOS = [292, 636, 1357]

TIPOS_IMPOSIBLES = {
    "SBP(mmHg)": [],
    "DBP(mmHg)": [("<=30", 30)],
    "FPG(mmol/L)": [],
    "HbA1c(%)": [("<=2.5", 2.5)],
    "TC(mmol/L)": [("==0", 0)],
}


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica dedup y tipeos->NaN hasta obtener la tabla clínica limpia."""
    # 1) Pacientes con etiqueta contradictoria (Group 1 y Group 0)
    antes = len(df)
    df = df[~df["SampleID"].isin(CONTRADICTORIOS)].copy()
    print(f"- Eliminadas filas de pacientes con etiqueta contradictoria: {antes - len(df)}")

    # 2) Deduplicacion: conservar el primer registro por paciente
    antes = len(df)
    df = df.drop_duplicates(subset="SampleID", keep="first").copy()
    print(f"- Filas duplicadas eliminadas: {antes - len(df)}")

    # 3) Tipeos imposibles -> NaN
    imputadas_nan = 0
    for col, reglas in TIPOS_IMPOSIBLES.items():
        for etiqueta, umbral in reglas:
            if etiqueta == "==0":
                mascara = df[col] == umbral
            else:
                mascara = df[col] <= umbral
            imputadas_nan += int(mascara.sum())
            df.loc[mascara, col] = float("nan")

    return df, imputadas_nan


def main() -> None:
    df = pd.read_csv(RAW)
    inicial = len(df)

    df_limpio, tipeos_a_nan = limpiar(df)

    columnas_salida = [c for c, nombre in COLUMNAS_CLINICAS.items() if not nombre.startswith("_")]
    renombre = {c: COLUMNAS_CLINICAS[c] for c in columnas_salida}
    salida = df_limpio[["SampleID", COLUMNA_CLASE] + columnas_salida].rename(columns=renombre)

    salida[COLUMNA_CLASE] = salida[COLUMNA_CLASE].map({1: "gestacional", 0: "embarazada_sana"})

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    salida.to_csv(SALIDA, index=False)

    print(f"\nRegistros cargados: {inicial}")
    print(f"Registros finales: {len(salida)}")
    print(f"Tipeos convertidos a NaN: {tipeos_a_nan}")
    print(f"Distribución clase: {dict(salida[COLUMNA_CLASE].value_counts())}")
    print("\nValores ausentes por columna:")
    print(salida[salida.columns[1:]].isna().sum().to_string())
    print("\nDescripción de la salida:")
    print(salida[salida.columns[1:]].describe().to_string())
    print(f"\n[ok] escrito en {SALIDA}")


if __name__ == "__main__":
    main()