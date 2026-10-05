export const CLASES = {
  tipo_1: { etiqueta: 'Diabetes tipo 1', corto: 'Tipo 1', color: '#b3261e' },
  tipo_2: { etiqueta: 'Diabetes tipo 2', corto: 'Tipo 2', color: '#a57f2c' },
  gestacional: { etiqueta: 'Diabetes gestacional', corto: 'Gestacional', color: '#9d2449' },
  sano: { etiqueta: 'Sin diabetes', corto: 'Sin diabetes', color: '#235b4e' },
}

export const ORDEN_CLASES = ['tipo_1', 'tipo_2', 'gestacional', 'sano']

export const VARIABLES = [
  {
    nombre: 'edad',
    etiqueta: 'Edad',
    unidad: 'años',
    placeholder: '45',
    min: 1,
    max: 120,
  },
  {
    nombre: 'imc',
    etiqueta: 'IMC',
    unidad: 'kg/m²',
    placeholder: '27.5',
    min: 10,
    max: 70,
  },
  {
    nombre: 'glucosa_ayuno',
    etiqueta: 'Glucosa en ayuno',
    unidad: 'mg/dL',
    placeholder: '110',
    min: 40,
    max: 600,
  },
  {
    nombre: 'hba1c',
    etiqueta: 'HbA1c',
    unidad: '%',
    placeholder: '5.8',
    min: 3,
    max: 20,
    requerido: false,
  },
  {
    nombre: 'presion_sistolica',
    etiqueta: 'Presión sistólica',
    unidad: 'mmHg',
    placeholder: '120',
    min: 70,
    max: 250,
  },
  {
    nombre: 'presion_diastolica',
    etiqueta: 'Presión diastólica',
    unidad: 'mmHg',
    placeholder: '80',
    min: 40,
    max: 150,
  },
]

export const AVISO_CLINICO =
  'Este sistema es una herramienta de apoyo al diagnóstico. No reemplaza el criterio de un profesional de la salud.'