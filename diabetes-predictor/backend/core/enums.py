from enum import StrEnum


class DiabetesType(StrEnum):
    """Clases de salida de la red neuronal multiclase."""

    TIPO_1 = "tipo_1"
    TIPO_2 = "tipo_2"
    GESTACIONAL = "gestacional"
    SANO = "sano"


class BiologicalSex(StrEnum):
    F = "F"
    M = "M"
    OTRO = "O"
