---
description: Usar cuando configures pipelines de CI/CD en GitHub Actions para deploy automático del frontend a Vercel o backend a AWS Lambda.
---

# GitHub Actions skill

## Workflows Principales
- `.github/workflows/deploy-frontend.yml`: Despliegue en Vercel.
- `.github/workflows/deploy-backend.yml`: Despliegue en AWS Lambda.
- `.github/workflows/test.yml`: Ejecución de tests en cada Pull Request.

## Reglas de Ejecución
- Solo se activan con `push` a la rama `main`.
- **Filtros de Ruta:** Usar `paths` para evitar despliegues innecesarios:
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'  # Solo si cambia el frontend
```

## Seguridad
- Usar **GitHub Secrets** para: `AWS_ACCESS_KEY`, `VERCEL_TOKEN`, `SUPABASE_KEY`.
- Nunca imprimir secretos en los logs de los workflows.
