-- Datos de prueba para desarrollo y demostraciones
-- Las probabilidades de cada fila deben sumar 1 (restricción CHECK probabilidades_suman_uno)

INSERT INTO patients (
    id, nombre, edad, sexo, imc, glucosa_ayuno, hba1c,
    presion_sistolica, presion_diastolica, antecedentes_familiares
) VALUES
    ('11111111-1111-4111-8111-111111111111', 'Paciente Uno',   45, 'M', 32.50, 145.00, 7.8, 140, 88, TRUE),
    ('22222222-2222-4222-8222-222222222222', 'Paciente Dos',   18, 'F', 21.00, 180.00, 9.5, 110, 70, FALSE),
    ('33333333-3333-4333-8333-333333333333', 'Paciente Tres',  32, 'F', 29.80, 100.00, 6.4, 118, 74, TRUE),
    ('44444444-4444-4444-8444-444444444444', 'Paciente Cuatro', 28, 'M', 22.40,  85.00, 5.2, 122, 78, FALSE)
ON CONFLICT (id) DO NOTHING;

INSERT INTO predictions (
    patient_id, resultado, probabilidad_tipo1, probabilidad_tipo2,
    probabilidad_gestacional, probabilidad_sano
) VALUES
    ('11111111-1111-4111-8111-111111111111', 'tipo_2',      0.01000, 0.87000, 0.02000, 0.10000),
    ('22222222-2222-4222-8222-222222222222', 'tipo_1',      0.88000, 0.10000, 0.01000, 0.01000),
    ('33333333-3333-4333-8333-333333333333', 'gestacional', 0.02000, 0.11000, 0.81000, 0.06000),
    ('44444444-4444-4444-8444-444444444444', 'sano',        0.01000, 0.06000, 0.02000, 0.91000);