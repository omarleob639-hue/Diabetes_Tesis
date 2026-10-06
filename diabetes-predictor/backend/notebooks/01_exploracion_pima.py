"""Exploración del dataset Pima Indians Diabetes.

Uso:
    backend/.venv/Scripts/python.exe backend/notebooks/01_exploracion_pima.py

Lee data/raw/pima/pima.csv (sin encabezado), detecta nulos disfrazados como 0,
resume distribución de clases y correlaciones, y reporta la cobertura de las
ocho variables clínicas del sistema.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "data" / "raw" / "pima" / "pima.csv"
INFORME = RAIZ / "EDA_PIMA.md"

COLUMNAS = [
    "embarazos",
    "glucosa",
    "presion_diastolica",
    "pliegue_cutaneo",
    "insulina",
    "imc",
    "funcion_pedigree",
    "edad",
    "resultado",
]

CERO_COMO_NULO = [
    "glucosa",
    "presion_diastolica",
    "pliegue_cutaneo",
    "insulina",
    "imc",
]

COBERTURA = {
    "Edad": ("directa", "columna `edad` (21-81 años)"),
    "Sexo": ("constante", "cohorte Pima: solo mujeres ≥21 años; sin variabilidad"),
    "IMC": ("directa", "columna `imc`"),
    "Glucosa en ayuno": ("directa", "columna `glucosa` (mg/dL)"),
    "HbA1c": ("ausente", "Pima no incluye hemoglobina glicosilada"),
    "Presión sistólica": ("ausente", "Pima solo registra presión diastólica"),
    "Presión diastólica": ("directa", "columna `presion_diastolica` (mmHg)"),
    "Antecedentes familiares": ("proxy", "`funcion_pedigree` (score continuo, no sí/no)"),
}


def cargar() -> pd.DataFrame:
    return pd.read_csv(RUTA, header=None, names=COLUMNAS)


def ceros_imposibles(df: pd.DataFrame, columna: str) -> int:
    return int((df[columna] == 0).sum())


def resumen_nulos(df: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for col in COLUMNAS[:-1]:
        ceros = ceros_imposibles(df, col)
        filas.append(
            {
                "variable": col,
                "nulos_reales": int(df[col].isna().sum()),
                "ceros": ceros,
                "pct_ceros": round(100 * ceros / len(df), 1),
                "media": round(float(df[col].mean()), 2),
                "mediana": round(float(df[col].median()), 2),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "nulos_si_cero_es_nulo": ceros if col in CERO_COMO_NULO else 0,
            }
        )
    return pd.DataFrame(filas)


def construir_informe(df: pd.DataFrame) -> str:
    n = len(df)
    nulos = resumen_nulos(df)
    positivos = int((df["resultado"] == 1).sum())
    negativos = int((df["resultado"] == 0).sum())
    nulos_totales = int(nulos["nulos_si_cero_es_nulo"].sum())
    filas_limpias = int((df[CERO_COMO_NULO] != 0).all(axis=1).sum())

    correlacion = df.corr(numeric_only=True)["resultado"].drop("resultado")
    correlacion = correlacion.reindex(correlacion.abs().sort_values(ascending=False).index)

    directas = [v for v, (tipo, _) in COBERTURA.items() if tipo == "directa"]
    proxies = [v for v, (tipo, _) in COBERTURA.items() if tipo == "proxy"]
    faltantes = [v for v, (tipo, _) in COBERTURA.items() if tipo != "directa" and tipo != "proxy"]

    lineas: list[str] = []
    lineas.append("# EDA — Pima Indians Diabetes Dataset\n")
    lineas.append(
        f"Fuente: `{RUTA.relative_to(RAIZ).as_posix()}` (UCI / Brownlee mirror), sin encabezado, 9 columnas.\n"
    )

    lineas.append("## 1. Dimensiones\n")
    lineas.append(f"- Registros: **{n}**")
    lineas.append(f"- Columnas: **{len(COLUMNAS)}** (8 predictoras + `resultado`)")
    lineas.append(f"- Duplicados exactos: **{int(df.duplicated().sum())}**")
    lineas.append(f"- Nulos reales (NaN): **{int(df.isna().sum().sum())}**\n")

    lineas.append("## 2. Ceros como valores faltantes disfrazados\n")
    lineas.append(
        "En Pima, `0` es clínicamente imposible en varias variables y se usa como marcador de ausencia de dato.\n"
    )
    lineas.append(nulos.to_markdown(index=False))
    lineas.append("")
    pct_afectadas = round(100 * nulos_totales / (n * len(CERO_COMO_NULO)), 1)
    lineas.append(f"- Celdas afectadas (5 variables): **{nulos_totales}** ({pct_afectadas}%)")
    lineas.append(f"- Filas sin ningún `0` imposible: **{filas_limpias}** ({round(100 * filas_limpias / n, 1)}%)")
    lineas.append(
        "- `pliegue_cutaneo` e `insulina` se midieron en subgrupos: su `0` no debe "
        "imputarse a la media sin decidir el criterio.\n"
    )

    lineas.append("## 3. Distribución de clases\n")
    lineas.append(f"- `resultado = 0` (sin diabetes): **{negativos}** ({round(100 * negativos / n, 1)}%)")
    lineas.append(f"- `resultado = 1` (diabetes): **{positivos}** ({round(100 * positivos / n, 1)}%)")
    lineas.append(f"- Razón de desbalance: **{round(negativos / positivos, 2)}:1**")
    lineas.append("- La columna es **binaria**: no distingue tipo 1 / tipo 2 / gestacional.\n")

    lineas.append("## 4. Correlación con el resultado\n")
    for var, valor in correlacion.items():
        lineas.append(f"- `{var}`: **{round(float(valor), 3)}**")
    lineas.append("")
    lineas.append(f"- Correlación más alta: `{correlacion.index[0]}` ({round(float(correlacion.iloc[0]), 3)}).")
    lineas.append(
        "- Las cinco variables con más `0` imposibles están entre las más "
        "correlacionadas: imputar mal altera el modelo.\n"
    )

    lineas.append("## 5. Cobertura de las ocho variables del sistema\n")
    lineas.append("| Variable | Cobertura en Pima | Detalle |")
    lineas.append("| --- | --- | --- |")
    for variable, (tipo, detalle) in COBERTURA.items():
        lineas.append(f"| {variable} | {tipo} | {detalle} |")
    lineas.append("")
    lineas.append(f"- Directas: **{len(directas)}/8** — {', '.join(directas)}")
    lineas.append(f"- Proxy: **{len(proxies)}/8** — {', '.join(proxies)}")
    lineas.append(f"- Sin dato usable: **{len(faltantes)}/8** — {', '.join(faltantes)}\n")

    lineas.append("## 6. Decisión de clases\n")
    lineas.append("Pima solo aporta dos etiquetas observables:")
    lineas.append("")
    lineas.append("| Clase del sistema | ¿Pima la aporta? | Por qué |")
    lineas.append("| --- | --- | --- |")
    lineas.append(
        "| `tipo_2` | Sí (parcial) | Cohorte adulta ≥21 años, diagnóstico por glucosa; "
        "asumida como tipo 2 por literatura |"
    )
    lineas.append("| `sano` | Sí (parcial) | `resultado = 0` |")
    lineas.append("| `tipo_1` | No | Sin edad de inicio, sin autoanticuerpos, sin insulina desde el diagnóstico |")
    lineas.append(
        "| `gestacional` | No | Solo mujeres no embarazadas en el momento de la medición; sin semana de gestación |"
    )
    lineas.append("")
    lineas.append(
        "**Con Pima solo se puede entrenar un modelo binario (2 clases) o "
        "reetiquetar `tipo_2` como proxy de «diabetes» para una demo de 3-4 clases "
        "con clases sintéticas.** Eso último es exactamente lo que el plan de datos "
        "descarta: fabricar clases completas con IA.\n"
    )

    lineas.append("## 7. Siguiente paso\n")
    lineas.append(
        "1. Definir el tratamiento de los `0` imposibles (excluir `pliegue_cutaneo`/`insulina` o imputar por mediana)."
    )
    lineas.append(
        "2. Cubrir `HbA1c`, `presión sistólica` y `tipo_1`/`gestacional` con "
        "datasets reales (FDDB Dinamarca, T1DiabetesGranada, Dryad GDM del sur de China)."
    )
    lineas.append(
        "3. Decidir 2 vs 4 clases según cuántas fuentes reales se obtengan, no por conveniencia de la demo.\n"
    )

    return "\n".join(lineas)


def main() -> None:
    df = cargar()
    informe = construir_informe(df)
    INFORME.write_text(informe, encoding="utf-8")
    print(informe)
    print(f"\n[ok] informe escrito en {INFORME}")


if __name__ == "__main__":
    main()
