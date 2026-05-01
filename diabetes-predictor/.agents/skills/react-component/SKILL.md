---
description: Usar cuando crees o modifiques componentes o páginas en React. Aplica para JSX, estilos con Tailwind y llamadas a la API.
---

# React component skill

## Convenciones
- **Ubicación:** Componentes en `src/components/`, Páginas en `src/pages/`.
- **Estilos:** Solo Tailwind CSS. Prohibido CSS inline.
- **Nombres:** `PascalCase` para componentes, `camelCase` para funciones/variables.
- **API:** Centralizar llamadas en `src/services/api.js`.

## Conexión con Backend
```javascript
const API_URL = import.meta.env.VITE_API_URL

export const predict = async (patientData) => {
  const response = await fetch(`${API_URL}/predictions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patientData)
  })
  if (!response.ok) throw new Error('Error en la API');
  return response.json()
}
```

## Formulario Clínico
Asegurar que se incluyan todas las variables: edad, sexo, imc, glucosa_ayuno, hba1c, presion_sistolica, presion_diastolica, antecedentes_familiares.
