---
description: Usar cuando necesites crear o modificar endpoints en FastAPI. Aplica para routers, schemas Pydantic y servicios del backend.
---

# FastAPI endpoint skill

## Convenciones
- **Ubicación:** Routers en `backend/routers/`, Schemas en `backend/schemas/`, Servicios en `backend/services/`.
- **REST:** Sustantivos en plural, minúsculas, sin verbos (ej: `/patients`).
- **Validación:** Usar Pydantic v2 para toda entrada y salida.
- **Lógica:** La lógica de negocio vive en `services/`, los routers solo coordinan.
- **Errores:** Usar siempre `HTTPException` con códigos de estado correctos.

## Estructura Maestra
```python
@router.post("/predictions", response_model=PredictionResponse)
async def create_prediction(data: PatientInput, db: Session = Depends(get_db)):
    try:
        # Validación extra o procesamiento previo
        result = model_service.predict(data)
        return result
    except Exception as e:
        # Log del error y respuesta clara
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")
```

## Variables Clínicas
- edad, sexo, imc, glucosa_ayuno, hba1c, presion_sistolica, presion_diastolica, antecedentes_familiares.
- Clases de salida: `tipo_1`, `tipo_2`, `gestacional`, `sano`.
