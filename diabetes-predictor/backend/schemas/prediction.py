from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.enums import DiabetesType

_PROBABILIDAD_MAXIMA = 1.0
_TOLERANCIA = 1e-3


class PredictionResponse(BaseModel):
    """Resultado de la red neuronal multiclase para un paciente."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_id: UUID
    resultado: DiabetesType
    probabilidad_tipo1: float = Field(ge=0, le=_PROBABILIDAD_MAXIMA)
    probabilidad_tipo2: float = Field(ge=0, le=_PROBABILIDAD_MAXIMA)
    probabilidad_gestacional: float = Field(ge=0, le=_PROBABILIDAD_MAXIMA)
    probabilidad_sano: float = Field(ge=0, le=_PROBABILIDAD_MAXIMA)
    created_at: datetime

    @model_validator(mode="after")
    def check_probabilidades_normalizadas(self) -> "PredictionResponse":
        total = (
            self.probabilidad_tipo1
            + self.probabilidad_tipo2
            + self.probabilidad_gestacional
            + self.probabilidad_sano
        )
        if abs(total - 1.0) > _TOLERANCIA:
            raise ValueError(f"Las probabilidades deben sumar 1 (sumaron {total:.5f})")
        return self

    @property
    def probabilidades(self) -> dict[DiabetesType, float]:
        return {
            DiabetesType.TIPO_1: self.probabilidad_tipo1,
            DiabetesType.TIPO_2: self.probabilidad_tipo2,
            DiabetesType.GESTACIONAL: self.probabilidad_gestacional,
            DiabetesType.SANO: self.probabilidad_sano,
        }
