---
description: Usar cuando configures o despliegues el backend de FastAPI en AWS Lambda con Dockerfile o Mangum.
---

# AWS Lambda skill

## Configuración
- **Mangum:** Adaptador necesario para ejecutar FastAPI en Lambda.
- **Handler:** El punto de entrada debe estar en `backend/main.py`.
- **Secrets:** Las variables de entorno se gestionan en AWS, nunca en el código.

## Implementación en main.py
```python
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI(title="Diabetes Predictor API")
# ... routers ...

handler = Mangum(app)
```

## Dockerfile para Lambda
```dockerfile
FROM public.ecr.aws/lambda/python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["main.handler"]
```
