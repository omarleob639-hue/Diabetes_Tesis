---
description: Usar cuando trabajes con el modelo de TensorFlow, entrenamiento, preprocesamiento, evaluación o exportación del modelo de diabetes.
---

# TensorFlow model skill

## Estructura de Archivos
- **Modelo:** `backend/model/saved_model/diabetes_model.h5`
- **Scaler:** `backend/model/saved_model/scaler.pkl`
- **Encoder:** `backend/model/saved_model/label_encoder.pkl`

## Reglas de Entrenamiento (Métricas Tesis)
- **Validación Cruzada:** Siempre usar 5 folds (`KFold`).
- **Objetivo:** Exactitud >= 85% y F1-score por clase >= 0.80.
- **Evaluación Obligatoria:** Generar siempre Matriz de Confusión y `classification_report`.

## Flujo de Producción
1. El preprocesamiento (escalado y codificación) debe ser **idéntico** al de entrenamiento.
2. `model_service.py` carga los archivos `.h5` y `.pkl` al iniciar la aplicación para evitar latencia.

```python
from sklearn.metrics import classification_report, confusion_matrix
# Ejecutar siempre al evaluar
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```
