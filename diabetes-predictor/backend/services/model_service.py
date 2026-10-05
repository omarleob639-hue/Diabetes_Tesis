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
    """Resultado de la red neuronal: clase ganadora y sus 4 probabilidades."""

    resultado: DiabetesType
    probabilidades: dict[DiabetesType, float]


class ModelService:
    """Carga el modelo entrenado y aplica el preprocesamiento.

    El orden de FEATURE_ORDER y la codificación de SEXO_ENCODING son el contrato
    entre el notebook de entrenamiento y esta capa. Si en el notebook se cambia
    el orden de columnas o la codificación del sexo, debe cambiarse aquí también:
    un orden distinto produce predicciones silenciosamente incorrectas.
    """

    FEATURE_ORDER = (
        "edad",
        "sexo",
        "imc",
        "glucosa_ayuno",
        "hba1c",
        "presion_sistolica",
        "presion_diastolica",
        "antecedentes_familiares",
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

    @property
    def is_ready(self) -> bool:
        return self._model is not None or self._stub_enabled

    def load(self) -> bool:
        """Carga el modelo y el escalador. Devuelve True si el sistema puede predecir."""
        if self._stub_enabled:
            return True

        if not self._model_path.exists():
            return False

        try:
            import joblib
            import tensorflow as tf

            self._model = tf.keras.models.load_model(self._model_path)
            scaler_path = self._model_path.parent / "scaler.joblib"
            self._scaler = joblib.load(scaler_path) if scaler_path.exists() else None
        except ImportError:
            return False
        except Exception:  # noqa: BLE001 - cualquier fallo de carga deja el modelo no disponible
            return False

        return True

    def predict(self, patient: PatientCreate) -> PredictionOutcome:
        if self._stub_enabled:
            return self._predict_stub(patient)
        if self._model is None:
            raise ModelNotReadyError(
                "El modelo no está cargado. Entrena el modelo o activa MODEL_STUB_ENABLED."
            )

        features = self._build_feature_vector(patient)
        if self._scaler is not None:
            features = self._scaler.transform([features])

        probabilities = self._model.predict(features)[0]
        mapped = dict(zip(self.CLASS_ORDER, (float(p) for p in probabilities), strict=True))
        return PredictionOutcome(resultado=max(mapped, key=mapped.__getitem__), probabilidades=mapped)

    def _build_feature_vector(self, patient: PatientCreate) -> list[float]:
        return [
            float(patient.edad),
            self.SEXO_ENCODING[patient.sexo],
            float(patient.imc),
            float(patient.glucosa_ayuno),
            float(patient.hba1c) if patient.hba1c is not None else 0.0,
            float(patient.presion_sistolica),
            float(patient.presion_diastolica),
            1.0 if patient.antecedentes_familiares else 0.0,
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
