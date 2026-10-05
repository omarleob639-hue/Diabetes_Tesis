-- Migración 001: esquema inicial del sistema de predicción de diabetes
-- Tablas: patients (datos clínicos) y predictions (resultados de la red neuronal)

-- Tipos enumerados para integridad referencial a nivel de base de datos
CREATE TYPE diabetes_type AS ENUM (
    'tipo_1',
    'tipo_2',
    'gestacional',
    'sano'
);

CREATE TYPE biological_sex AS ENUM (
    'F',
    'M',
    'O'
);

-- Función reutilizable para mantener updated_at sin depender de la aplicación
CREATE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Registro de datos clínicos del paciente
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL,
    edad SMALLINT NOT NULL CHECK (edad BETWEEN 0 AND 120),
    sexo biological_sex NOT NULL,
    imc NUMERIC(5, 2) NOT NULL CHECK (imc > 0),
    glucosa_ayuno NUMERIC(6, 2) NOT NULL CHECK (glucosa_ayuno > 0),
    hba1c NUMERIC(4, 1) CHECK (hba1c BETWEEN 3 AND 20),
    presion_sistolica SMALLINT NOT NULL CHECK (presion_sistolica BETWEEN 50 AND 300),
    presion_diastolica SMALLINT NOT NULL CHECK (presion_diastolica BETWEEN 30 AND 200),
    antecedentes_familiares BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Coherencia hemodinámica: la diastólica siempre es menor que la sistólica
    CONSTRAINT presion_coherente CHECK (presion_diastolica < presion_sistolica)
);

-- Resultados y probabilidades de la red neuronal multiclase
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    resultado diabetes_type NOT NULL,
    probabilidad_tipo1 NUMERIC(6, 5) NOT NULL CHECK (probabilidad_tipo1 BETWEEN 0 AND 1),
    probabilidad_tipo2 NUMERIC(6, 5) NOT NULL CHECK (probabilidad_tipo2 BETWEEN 0 AND 1),
    probabilidad_gestacional NUMERIC(6, 5) NOT NULL CHECK (probabilidad_gestacional BETWEEN 0 AND 1),
    probabilidad_sano NUMERIC(6, 5) NOT NULL CHECK (probabilidad_sano BETWEEN 0 AND 1),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Las probabilidades de una softmax suman 1; tolerancia por redondeo a 5 decimales
    CONSTRAINT probabilidades_suman_uno
        CHECK (ABS(
            probabilidad_tipo1 + probabilidad_tipo2
            + probabilidad_gestacional + probabilidad_sano - 1
        ) < 0.001)
);

CREATE INDEX predictions_patient_id_idx ON predictions (patient_id);
CREATE INDEX predictions_created_at_idx ON predictions (created_at DESC);

CREATE TRIGGER patients_set_updated_at
    BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER predictions_set_updated_at
    BEFORE UPDATE ON predictions
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();