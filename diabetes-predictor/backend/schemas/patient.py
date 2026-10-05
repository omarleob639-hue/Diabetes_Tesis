from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.enums import BiologicalSex


class PatientCreate(BaseModel):
    """Datos clínicos que captura el personal médico."""

    nombre: str = Field(min_length=1, max_length=120)
    edad: int = Field(ge=0, le=120)
    sexo: BiologicalSex
    imc: float = Field(gt=0, le=100)
    glucosa_ayuno: float = Field(gt=0, le=1000)
    hba1c: float | None = Field(default=None, ge=3, le=20)
    presion_sistolica: int = Field(ge=50, le=300)
    presion_diastolica: int = Field(ge=30, le=200)
    antecedentes_familiares: bool

    @model_validator(mode="after")
    def check_presion_coherente(self) -> "PatientCreate":
        if self.presion_diastolica >= self.presion_sistolica:
            raise ValueError(
                "La presión diastólica debe ser menor que la sistólica "
                f"(recibido: {self.presion_diastolica}/{self.presion_sistolica})"
            )
        return self


class PatientUpdate(BaseModel):
    """Actualización parcial; los campos omitidos conservan su valor."""

    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    edad: int | None = Field(default=None, ge=0, le=120)
    sexo: BiologicalSex | None = None
    imc: float | None = Field(default=None, gt=0, le=100)
    glucosa_ayuno: float | None = Field(default=None, gt=0, le=1000)
    hba1c: float | None = Field(default=None, ge=3, le=20)
    presion_sistolica: int | None = Field(default=None, ge=50, le=300)
    presion_diastolica: int | None = Field(default=None, ge=30, le=200)
    antecedentes_familiares: bool | None = None


class PatientResponse(PatientCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
