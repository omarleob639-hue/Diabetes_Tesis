import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enums import DiabetesType
from db.base import get_db
from db.models import Patient, Prediction
from schemas.patient import PatientCreate
from schemas.prediction import PredictionResponse
from services.model_service import ModelNotReadyError, model_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("", response_model=list[PredictionResponse])
def list_predictions(
    patient_id: UUID | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> list[Prediction]:
    consulta = select(Prediction)
    if patient_id is not None:
        consulta = consulta.where(Prediction.patient_id == patient_id)

    return list(db.scalars(consulta.offset(skip).limit(limit)))


@router.post("", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction(data: PatientCreate, db: Session = Depends(get_db)) -> Prediction:
    try:
        outcome = model_service.predict(data)
    except ModelNotReadyError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Fallo la prediccion")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al ejecutar la prediccion",
        ) from exc

    # Paciente y prediccion se escriben en una sola transaccion
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.flush()

    probabilidades = outcome.probabilidades
    prediction = Prediction(
        patient_id=patient.id,
        resultado=outcome.resultado,
        probabilidad_tipo1=probabilidades[DiabetesType.TIPO_1],
        probabilidad_tipo2=probabilidades[DiabetesType.TIPO_2],
        probabilidad_gestacional=probabilidades[DiabetesType.GESTACIONAL],
        probabilidad_sano=probabilidades[DiabetesType.SANO],
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: UUID, db: Session = Depends(get_db)) -> Prediction:
    prediction = db.get(Prediction, prediction_id)
    if prediction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediccion no encontrada")
    return prediction
