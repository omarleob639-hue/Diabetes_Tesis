"""Entrenamiento del baseline real-only con enfoque one-vs-rest (OvR).

Uso:
    backend/.venv/Scripts/python.exe backend/notebooks/06_entrenamiento_ovr.py

Estrategia (la mas defendible: cero datos inventados):
- Un modelo binario por frontera entre clases, cada uno entrenado SOLO con
  datos reales de las dos clases que separa y con las variables que esa fuente
  si mide. Un multiclase sobre las 8 variables exigiria imputar 4 de 8 en
  practicamente todas las filas.
- Frontera 1 `sano` vs `tipo_2`  -> Pima (edad, IMC, glucosa, PAD).
- Frontera 2 `gestacional` vs `embarazada_sana` -> Dryad (glucosa, HbA1c, PAS, PAD).
- Frontera 3 `tipo_1` vs `tipo_2` -> T1DiabetesGranada: PENDIENTE de descarga.

Advertencia clinica (ver FILTRO_DATASETS.md): en la frontera 2 la glucosa en
ayunas y la HbA1c son *criterios de diagnostico* de diabetes gestacional. El
modelo DETECTA diabetes gestacional ya establecida; no predice que va a
aparecer. Queda documentado como limitacion.

Uniones: `glucosa_ayuno` en mg/dL, `hba1c` en %, presion en mmHg.

Artefactos en `backend/model/saved_model/` (fuera de git por `*.joblib`).
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RAIZ = Path(__file__).resolve().parents[2]
UNIFICADO = RAIZ / "data" / "processed" / "dataset_unificado.csv"
MODELOS = RAIZ / "backend" / "model" / "saved_model"

SEED = 42

ARQUITECTURA = (32, 16, 8)
MAX_ITER = 2000
CV_FOLDS = 5

FRONTERAS = [
    {
        "nombre": "sano_vs_tipo2",
        "clases": ("sano", "tipo_2"),
        "fuente": "pima",
        "features": ["edad", "imc", "glucosa_ayuno", "presion_diastolica"],
    },
    {
        "nombre": "gestacional_vs_control",
        "clases": ("gestacional", "embarazada_sana"),
        "fuente": "dryad_gdm",
        "features": ["glucosa_ayuno", "hba1c", "presion_sistolica", "presion_diastolica"],
    },
]


def construir_pipeline() -> Pipeline:
    """El imputador va DENTRO del pipeline: se ajusta en cada fold de la CV,
    nunca sobre el dataset completo (evita fuga de informacion)."""
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "mlp",
                MLPClassifier(
                    hidden_layer_sizes=ARQUITECTURA,
                    activation="relu",
                    solver="adam",
                    alpha=1e-4,
                    max_iter=MAX_ITER,
                    random_state=SEED,
                ),
            ),
        ]
    )


def entrenar_frontera(df: pd.DataFrame, frontera: dict) -> dict:
    sub = df[df["clase"].isin(frontera["clases"])].copy()
    if sub.empty:
        print(f"[aviso] frontera {frontera['nombre']}: sin datos")
        return {}

    X = sub[frontera["features"]].to_numpy(dtype=float)
    y = sub["clase"].to_numpy()

    if np.isnan(X).any():
        print(f"[aviso] {frontera['nombre']}: hay NaN en las features; se imputa la mediana dentro de cada fold")

    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=SEED)
    predicciones = cross_val_predict(
        construir_pipeline(), X, y, cv=cv, method="predict_proba"
    )
    clases_modelo = sorted(frontera["clases"])
    y_pred = np.array(clases_modelo)[predicciones.argmax(axis=1)]

    exactitud_cv = float((y_pred == y).mean())
    print(f"\n=== Frontera {frontera['nombre']} ({frontera['fuente']}) ===")
    print(f"filas: {len(sub)} | clases: {dict(pd.Series(y).value_counts())}")
    print(f"features: {frontera['features']}")
    print(classification_report(y, y_pred, digits=3, zero_division=0))
    print("matriz de confusion:")
    print(confusion_matrix(y, y_pred, labels=clases_modelo))

    modelo_final = construir_pipeline()
    modelo_final.fit(X, y)
    MODELOS.mkdir(parents=True, exist_ok=True)
    ruta = MODELOS / f"ovr_{frontera['nombre']}.joblib"
    joblib.dump(modelo_final, ruta)
    print(f"[ok] modelo guardado en {ruta}")

    return {
        "nombre": frontera["nombre"],
        "n": len(sub),
        "features": frontera["features"],
        "exactitud_cv": exactitud_cv,
        "ruta": str(ruta),
    }


def main() -> None:
    df = pd.read_csv(UNIFICADO)
    print(f"Dataset unificado: {len(df)} filas | clases: {dict(df['clase'].value_counts())}")

    resumenes = []
    for frontera in FRONTERAS:
        resumen = entrenar_frontera(df, frontera)
        if resumen:
            resumenes.append(resumen)

    print("\n=== Resumen OvR (real-only) ===")
    for r in resumenes:
        print(f"{r['nombre']:28s} n={r['n']:5d} exactitud_cv={r['exactitud_cv']:.4f} features={len(r['features'])}")
    print("\nFalta la frontera `tipo_1` vs `tipo_2` (T1DiabetesGranada no descargado).")


if __name__ == "__main__":
    main()