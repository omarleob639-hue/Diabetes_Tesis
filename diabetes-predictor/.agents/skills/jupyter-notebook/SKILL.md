---
description: Usar cuando trabajes en los notebooks de Jupyter para exploración, preprocesamiento o entrenamiento del modelo.
---

# Jupyter notebook skill

## Estructura Sugerida
1. `01_exploracion.ipynb`: Análisis de datos clínicos de Calpulalpan.
2. `02_preprocesamiento.ipynb`: Limpieza y normalización.
3. `03_entrenamiento.ipynb`: Entrenamiento de la RNA multiclase.
4. `04_evaluacion.ipynb`: Validación y métricas finales.

## Reglas de Trabajo
- **Documentación:** Cada celda de código debe estar precedida por una celda Markdown explicativa.
- **Persistencia:** Guardar el `scaler` y el `encoder` en la misma sesión donde se entrena el modelo exitoso.
- **Librerías:** Pandas, Numpy, Matplotlib, Seaborn, Scikit-learn, TensorFlow.
- **Exportación:** Al finalizar el entrenamiento, copiar automáticamente el modelo a `backend/model/saved_model/`.
