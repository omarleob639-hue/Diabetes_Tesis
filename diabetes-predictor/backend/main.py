import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from routers import health, patients, predictions
from services.model_service import model_service

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if model_service.load():
        logger.info("Modelo cargado; el sistema puede predecir")
    else:
        logger.warning(
            "Modelo no disponible: POST /predictions respondera 503 hasta "
            "entrenar el modelo o activar MODEL_STUB_ENABLED"
        )
    yield


app = FastAPI(
    title="Sistema de Prediccion de Diabetes",
    description="API de deteccion del tipo de diabetes con mayor probabilidad en un paciente.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(patients.router)
app.include_router(predictions.router)
