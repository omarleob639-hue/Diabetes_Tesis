from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from core.config import get_settings
from core.enums import BiologicalSex, DiabetesType
from schemas.patient import PatientCreate


class ModelNotReadyError(RuntimeError):
    """Se lanza al pedir una predicción sin un modelo cargado."""


@dataclass(frozen=True, slots=True)
class PredictionOutcome:
    """Resultado del modelo: clase ganadora y sus 4 probabilidades."""

    resultado: DiabetesType
    probabilidades: dict[DiabetesType, float]


class ModelService:
    """Carga el modelo entrenado y aplica el preprocesamiento.

    El orden de FEATURE_ORDER es el contrato entre el script de entrenamiento
    (backend/notebooks/03_entrenamiento_pima.py) y esta capa. Si el script
    cambia el orden de columnas, debe cambiarse aquí también: un orden distinto
    produce predicciones silenciosamente incorrectas.

    Estado actual — modelo binario de demostración (Pima):
    - 4 features con dato directo en Pima: `edad`, `imc`, `glucosa_ayuno` y
      `presion_diastolica`. `sexo`, `hba1c`, `presion_sistolica` y
      `antecedentes_familiares` se reciben del formulario pero el modelo de
      demostración no los usa (Pima no los registra; ver EDA_PIMA.md).
    - Clasificador MLP de scikit-learn guardado como `diabetes_model.joblib`
      con escalador `scaler.joblib`. TensorFlow no tiene ruedas oficiales para
      Python 3.13; si el día de mañana se entrena el modelo tetraclásico en
      Keras (`.h5`), esta capa lo detecta y lo sirve igual.
    - La salida es binaria: índice 1 = diabetes (tipo_2), índice 0 = sano.
      `tipo_1` y `gestacional` se devuelven en 0.0: el modelo NO puede
      predecirlas con los datos actuales y no debe fabricarse.
    """

    FEATURE_ORDER = (
        "edad",
        "imc",
        "glucosa_ayuno",
        "presion_diastolica",
    )

    CLASS_ORDER = (
        DiabetesType.TIPO_1,
        DiabetesType.TIPO_2,
        DiabetesType.GESTACIONAL,
        DiabetesType.SANO,
    )

    SEXO_ENCODING: ClassVar[dict[BiologicalSex, float]] = {
        BiologicalSex.F: 0.0,
        BiologicalSex.M: 1.0,
        BiologicalSex.OTRO: 2.0,
    }

    def __init__(self, model_path: Path, stub_enabled: bool = False) -> None:
        self._model_path = model_path
        self._stub_enabled = stub_enabled
        self._model = None
        self._scaler = None
        self._is_binary = False

    @property
    def is_ready(self) -> bool:
        return self._model is not None or self._stub_enabled

    def load(self) -> bool:
        """Carga el modelo y el escalador. Devuelve True si el sistema puede predecir."""
        if self._stub_enabled:
            return True

        if not self._model_path.exists():
            return False

        scaler_path = self._model_path / "scaler.joblib"

        try:
            import joblib

            binary_path = self._model_path / "diabetes_model.joblib"
            if binary_path.exists():
                self._model = joblib.load(binary_path)
                self._scaler = joblib.load(scaler_path) if scaler_path.exists() else None
                self._is_binary = True
                return True

            import tensorflow as tf

            self._model = tf.keras.models.load_model(self._model_path)
            self._scaler = joblib.load(scaler_path) if scaler_path.exists() else None
            return True
        except ImportError:
            return False
        except Exception:  # noqa: BLE001 - cualquier fallo de carga deja el modelo no disponible
            return False

    def predict(self, patient: PatientCreate) -> PredictionOutcome:
        if self._stub_enabled:
            return self._predict_stub(patient)
        if self._model is None:
            raise ModelNotReadyError(
                "El modelo no está cargado. Entrena el modelo o activa MODEL_STUB_ENABLED."
            )

        if self._is_binary:
            return self._predict_binario(patient)

        features = self._build_feature_vector(patient)
        if self._scaler is not None:
            features = self._scaler.transform([features])

        probabilities = self._model.predict(features)[0]
        mapped = dict(zip(self.CLASS_ORDER, (float(p) for p in probabilities), strict=True))
        return PredictionOutcome(resultado=max(mapped, key=mapped.__getitem__), probabilidades=mapped)

    def _predict_binario(self, patient: PatientCreate) -> PredictionOutcome:
        features = self._build_feature_vector(patient)
        if self._scaler is not None:
            features = self._scaler.transform([features])

        proba = self._model.predict_proba(features)[0]
        p_sano = float(proba[0])
        p_tipo_2 = float(proba[1])
        probabilidades = {
            DiabetesType.TIPO_1: 0.0,
            DiabetesType.TIPO_2: p_tipo_2,
            DiabetesType.GESTACIONAL: 0.0,
            DiabetesType.SANO: p_sano,
        }
        resultado = (
            DiabetesType.TIPO_2 if p_tipo_2 >= p_sano else DiabetesType.SANO
        )
        return PredictionOutcome(resultado=resultado, probabilidades=probabilidades)

    def _build_feature_vector(self, patient: PatientCreate) -> list[float]:
        return [
            float(patient.edad),
            float(patient.imc),
            float(patient.glucosa_ayuno),
            float(patient.presion_diastolica),
        ]

    def _predict_stub(self, patient: PatientCreate) -> PredictionOutcome:
        """Predicción ficticia y determinista para desarrollo de interfaz.

        NO es un modelo clínico. Se activa únicamente con MODEL_STUB_ENABLED=true.
        """
        if patient.edad < 30 and patient.imc < 25:
            resultado = DiabetesType.TIPO_1
        elif patient.sexo is BiologicalSex.F and 25 <= patient.edad <= 45:
            resultado = DiabetesType.GESTACIONAL
        elif (patient.hba1c or 0) >= 6.5 or patient.glucosa_ayuno >= 126:
            resultado = DiabetesType.TIPO_2
        else:
            resultado = DiabetesType.SANO

        base = 0.97 if resultado is DiabetesType.SANO else 0.85
        remaining = (1.0 - base) / 3
        probabilidades = {clase: base if clase is resultado else remaining for clase in self.CLASS_ORDER}
        return PredictionOutcome(resultado=resultado, probabilidades=probabilidades)


_settings = get_settings()
model_service = ModelService(
    model_path=Path(__file__).resolve().parent.parent / _settings.model_path,
    stub_enabled=_settings.model_stub_enabled,
)
