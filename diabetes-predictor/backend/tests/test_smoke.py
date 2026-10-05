"""Pruebas de humo: verifican el contrato de la API sin requerir base de datos real."""

import os

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("MODEL_STUB_ENABLED", "true")

from fastapi.testclient import TestClient

from db.base import engine
from db.models import Base
from main import app

DATOS_VALIDOS = {
    "nombre": "Paciente Prueba",
    "edad": 45,
    "sexo": "M",
    "imc": 32.5,
    "glucosa_ayuno": 145.0,
    "hba1c": 7.8,
    "presion_sistolica": 140,
    "presion_diastolica": 88,
    "antecedentes_familiares": True,
}


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)


def test_health(client):
    assert client.get("/health").status_code == 200


@pytest.mark.parametrize(
    ("nombre_caso", "ajustes", "esperado"),
    [
        ("adulto_con_glucosa_alta", {"edad": 45, "sexo": "M"}, "tipo_2"),
        ("joven_delgado", {"edad": 18, "sexo": "F", "imc": 21.0, "glucosa_ayuno": 180.0}, "tipo_1"),
        (
            "mujer_en_edad_fertil",
            {"edad": 32, "sexo": "F", "imc": 29.8, "glucosa_ayuno": 90.0, "hba1c": None},
            "gestacional",
        ),
        (
            "adulto_sano",
            {"edad": 50, "sexo": "M", "imc": 22.4, "glucosa_ayuno": 85.0, "hba1c": 5.2},
            "sano",
        ),
    ],
)
def test_prediccion_clase_esperada(client, nombre_caso, ajustes, esperado):
    cuerpo = {**DATOS_VALIDOS, **ajustes}
    respuesta = client.post("/predictions", json=cuerpo)

    assert respuesta.status_code == 201, nombre_caso
    assert respuesta.json()["resultado"] == esperado, nombre_caso


def test_probabilidades_suman_uno(client):
    respuesta = client.post("/predictions", json=DATOS_VALIDOS)
    cuerpo = respuesta.json()

    total = (
        cuerpo["probabilidad_tipo1"]
        + cuerpo["probabilidad_tipo2"]
        + cuerpo["probabilidad_gestacional"]
        + cuerpo["probabilidad_sano"]
    )
    assert abs(total - 1.0) < 1e-3


def test_presion_incoherente_rechazada(client):
    respuesta = client.post(
        "/predictions",
        json={**DATOS_VALIDOS, "presion_sistolica": 120, "presion_diastolica": 130},
    )
    assert respuesta.status_code == 422


def test_sexo_invalido_rechazado(client):
    assert client.post("/predictions", json={**DATOS_VALIDOS, "sexo": "X"}).status_code == 422


def test_hba1c_opcional(client):
    cuerpo = {**DATOS_VALIDOS, "hba1c": None}
    assert client.post("/predictions", json=cuerpo).status_code == 201


def test_paciente_inexistente_404(client):
    respuesta = client.get("/patients/00000000-0000-4000-8000-000000000000")
    assert respuesta.status_code == 404
