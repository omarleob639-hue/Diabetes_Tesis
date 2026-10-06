"""Entrenamiento y evaluación del modelo binario de demostración (Pima).

Uso:
    backend/.venv/Scripts/python.exe backend/notebooks/03_entrenamiento_pima.py

Contrato con services/model_service.py:
- 4 features escaladas con StandardScaler: edad, imc, glucosa_ayuno,
  presion_diastolica (mismo orden que FEATURE_ORDER).
- MLPClassifier (red neuronal) de sklearn: esta demostración evita TensorFlow
  porque no hay ruedas oficiales para Python 3.13 (backend/requirements.txt).
- Salida binaria: índice 1 = diabetes (tipo_2), índice 0 = sano. El servicio
  mapea a las clases del sistema dejando tipo_1 y gestacional en 0.0.
- Métricas con 5 folds estratificados (estrategia de la tesis), escalador
  ajustado dentro de cada fold para evitar leakage.

Los artefactos (.joblib) quedan fuera de git (`*.joblib` en .gitignore).
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "data" / "processed" / "pima_features.csv"
MODELO = RAIZ / "backend" / "model" / "saved_model" / "diabetes_model.joblib"
ESCALADOR = RAIZ / "backend" / "model" / "saved_model" / "scaler.joblib"

FEATURES = ["edad", "imc", "glucosa_ayuno", "presion_diastolica"]
ETIQUETAS = {0: "sano", 1: "tipo_2"}
FOLDS = 5
RANDOM_STATE = 42


def pipeline() -> make_pipeline:
    return make_pipeline(
        StandardScaler(),
        MLPClassifier(
            hidden_layer_sizes=(32, 16, 8),
            activation="relu",
            solver="adam",
            alpha=1e-3,
            max_iter=1200,
            random_state=RANDOM_STATE,
        ),
    )


def validacion_cruzada(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    kfold = StratifiedKFold(n_splits=FOLDS, shuffle=True, random_state=RANDOM_STATE)
    y_verdaderos: list[np.ndarray] = []
    y_predichos: list[np.ndarray] = []
    exactitudes: list[float] = []

    for fold, (train_idx, test_idx) in enumerate(kfold.split(X, y), start=1):
        modelo = pipeline()
        modelo.fit(X[train_idx], y[train_idx])
        y_pred = modelo.predict(X[test_idx])
        y_verdaderos.append(y[test_idx])
        y_predichos.append(y_pred)
        exactitudes.append(float(modelo.score(X[test_idx], y[test_idx])))
        print(f"fold {fold}: exactitud={exactitudes[-1]:.4f}")

    y_t = np.concatenate(y_verdaderos)
    y_p = np.concatenate(y_predichos)
    print(f"\nExactitud media CV: {np.mean(exactitudes):.4f} ± {np.std(exactitudes):.4f}")
    print("\nClassification report (CV agregada):")
    print(classification_report(y_t, y_p, target_names=list(ETIQUETAS.values())))
    print("Matriz de confusión (CV agregada):")
    print(confusion_matrix(y_t, y_p))

    return y_t, y_p


def main() -> None:
    df = pd.read_csv(ENTRADA)
    X = df[FEATURES].to_numpy()
    y = df["resultado"].to_numpy()

    validacion_cruzada(X, y)

    modelo_final = pipeline().fit(X, y)
    MODELO.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo_final.named_steps["mlpclassifier"], MODELO)
    joblib.dump(modelo_final.named_steps["standardscaler"], ESCALADOR)
    print(f"\n[ok] modelo guardado en {MODELO}")
    print(f"[ok] escalador guardado en {ESCALADOR}")

    ejemplo = pd.DataFrame(
        [
            {"edad": 50, "imc": 31.0, "glucosa_ayuno": 168.0, "presion_diastolica": 82.0},
            {"edad": 25, "imc": 24.0, "glucosa_ayuno": 92.0, "presion_diastolica": 68.0},
        ]
    )
    probas = modelo_final.predict_proba(ejemplo)
    for fila, (proba, pred) in enumerate(zip(probas, modelo_final.predict(ejemplo), strict=True)):
        print(f"ejemplo {fila + 1}: {ETIQUETAS[int(pred)]} "
              f"(p_sano={proba[0]:.3f}, p_tipo_2={proba[1]:.3f})")


if __name__ == "__main__":
    main()