from fastapi import APIRouter
from sqlalchemy import text

from db.base import SessionLocal

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        estado_bd = "ok"
    except Exception:  # noqa: BLE001 - un chequeo de salud no debe propagar errores de conexion
        estado_bd = "sin_conexion"

    return {"estado": "ok", "base_datos": estado_bd}
