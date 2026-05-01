---
description: Usar cuando crees o modifiques tablas, migraciones o consultas en PostgreSQL con Supabase.
---

# Supabase migration skill

## Convenciones de Base de Datos
- **Migraciones:** Guardar en `database/migrations/` con prefijo `001_`, `002_`, etc.
- **Nombres:** `snake_case` para tablas y columnas.
- **Columnas Base:** Todas las tablas deben tener `id` (UUID), `created_at` y `updated_at`.
- **Inmutabilidad:** No editar migraciones ya ejecutadas, siempre crear una nueva.

## Tablas del Sistema
- `patients`: Historial y datos clínicos.
- `predictions`: Resultados y probabilidades de la red neuronal.

```sql
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES patients(id),
  resultado VARCHAR(20) NOT NULL,
  probabilidad_tipo1 FLOAT,
  probabilidad_tipo2 FLOAT,
  probabilidad_gestacional FLOAT,
  probabilidad_sano FLOAT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```
