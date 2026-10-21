"""Dataset unificado de las 8 variables clínicas del sistema.

Uso:
    backend/.venv/Scripts/python.exe backend/notebooks/05_dataset_unificado.py

Une las fuentes ya limpias en una sola tabla con el contrato del sistema
(8 variables), el identificador de clase, la procedencia y una marca de origen
(por ahora todo `real`; las filas sintéticas se agregarán después con
`06_completo_sintetico.py`).

Fuentes incluidas hoy:
- Pima (`data/processed/pima_features.csv`): `sano` (500) y `tipo_2` (268).
  Aporta edad, IMC, glucosa en ayuno (mg/dL) y presión diastólica.
- Dryad GDM (`data/processed/dryad_gdm_features.csv`): `gestacional` (534) y
  `embarazada_sana` (620). Aporta glucosa (mmol/L -> mg/dL), HbA1c, presión
  sistólica y diastólica.
- T1DiabetesGranada: **pendiente de descarga** (acceso aprobado, falta bajar
  el ZIP). Dejará la clase `tipo_1` con edad, sexo, glucosa y HbA1c.

Decisiones documentadas:
- `embarazada_sana` se mantiene como clase de control SEPARADA de `sano`:
  Pima son mujeres no embarazadas y Dryad son embarazadas sin GDM. Fusionarlas
  reintroduciría el confounding que apunta FILTRO_DATASETS.md.
- Las unidades se normalizan a las del sistema: glucosa en mg/dL, HbA1c en %,
  presión en mmHg, IMC en kg/m2.
- Los datos que una fuente no trae se dejan vacios (NaN): no se imputan ni se
  inventan aqui. El completamiento se documenta aparte.
- `antecedentes_familiares` no existe en ninguna fuente: queda vacia en todo
  el dataset (columna a resolver con la recolecta clinica o con sintesis).

No se sube a git: `data/processed/*` esta en `.gitignore`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PIMA = RAIZ / "data" / "processed" / "pima_features.csv"
DRYAD = RAIZ / "data" / "processed" / "dryad_gdm_features.csv"
T1D_RAW = RAIZ / "data" / "raw" / "t1diabetes_granada"
SALIDA = RAIZ / "data" / "processed" / "dataset_unificado.csv"

VARIABLES = [
    "edad",
    "sexo",
    "imc",
    "glucosa_ayuno",
    "hba1c",
    "presion_sistolica",
    "presion_diastolica",
    "antecedentes_familiares",
]

MMOL_L_A_MG_DL = 18.0182

CLASES_SISTEMA = ["tipo_1", "tipo_2", "gestacional", "sano"]


def marco_vacio() -> pd.DataFrame:
    df = pd.DataFrame(columns=["id"] + VARIABLES + ["clase", "origen", "fuente"])
    return df


def de_pima() -> pd.DataFrame:
    df = pd.read_csv(PIMA)
    salida = marco_vacio()
    salida["id"] = [f"pima_{i:04d}" for i in range(len(df))]
    salida["edad"] = df["edad"]
    salida["sexo"] = "F"  # Pima Indian Diabetes Database: solo mujeres
    salida["imc"] = df["imc"]
    salida["glucosa_ayuno"] = df["glucosa_ayuno"]  # ya en mg/dL
    salida["presion_diastolica"] = df["presion_diastolica"]
    salida["clase"] = df["resultado"].map({0: "sano", 1: "tipo_2"})
    salida["origen"] = "real"
    salida["fuente"] = "pima"
    return salida


def de_dryad() -> pd.DataFrame:
    df = pd.read_csv(DRYAD)
    salida = marco_vacio()
    salida["id"] = [f"dryad_{sid}" for sid in df["SampleID"].astype(str)]
    salida["sexo"] = "F"  # grupo de embarazos
    salida["glucosa_ayuno"] = df["glucosa_ayuno"] * MMOL_L_A_MG_DL  # mmol/L -> mg/dL
    salida["hba1c"] = df["hba1c"]
    salida["presion_sistolica"] = df["presion_sistolica"]
    salida["presion_diastolica"] = df["presion_diastolica"]
    salida["clase"] = df["clase"]
    salida["origen"] = "real"
    salida["fuente"] = "dryad_gdm"
    return salida


def de_t1diabetes_granada() -> pd.DataFrame:
    """Clase `tipo_1`. Falta el ZIP (acceso aprobado, descarga pendiente)."""
    if not T1D_RAW.exists():
        print("[aviso] T1DiabetesGranada no esta descargado: la clase `tipo_1` queda fuera.")
        print("        Bajar el ZIP desde Zenodo con la cuenta aprobada y extraerlo en:")
        print(f"        {T1D_RAW}")
        return marco_vacio()
    print("[aviso] T1DiabetesGranada presente: falta implementar su lectura (unidades HbA1c/glucosa).")
    return marco_vacio()


def cobertura(df: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for clase, grupo in df.groupby("clase"):
        fila = {"clase": clase, "n": len(grupo)}
        for var in VARIABLES:
            disponibles = grupo[var].notna().sum()
            fila[var] = f"{int(disponibles)}/{len(grupo)}"
        filas.append(fila)
    return pd.DataFrame(filas)


def main() -> None:
    pima = de_pima()
    dryad = de_dryad()
    t1d = de_t1diabetes_granada()
    df = pd.concat([pima, dryad, t1d], ignore_index=True)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA, index=False)

    print(f"\nFilas por clase: {dict(df['clase'].value_counts())}")
    print(f"Filas por fuente: {dict(df['fuente'].value_counts())}")
    print(f"Total filas: {len(df)}")
    print("\nCobertura por clase (dato disponible / total):")
    print(cobertura(df).to_string(index=False))
    print("\nCobertura global por variable:")
    global_ = {var: f"{int(df[var].notna().sum())}/{len(df)}" for var in VARIABLES}
    for var, cov in global_.items():
        print(f"  {var:24s} {cov}")
    print(f"\n[ok] escrito en {SALIDA}")


if __name__ == "__main__":
    main()