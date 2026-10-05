from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.enums import BiologicalSex, DiabetesType

diabetes_type_enum = sa.Enum(DiabetesType, name="diabetes_type", values_callable=lambda e: [m.value for m in e])
biological_sex_enum = sa.Enum(BiologicalSex, name="biological_sex", values_callable=lambda e: [m.value for m in e])


class Base(DeclarativeBase):
    pass


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(sa.Text, nullable=False)
    edad: Mapped[int] = mapped_column(sa.SmallInteger, nullable=False)
    sexo: Mapped[BiologicalSex] = mapped_column(biological_sex_enum, nullable=False)
    imc: Mapped[float] = mapped_column(sa.Numeric(5, 2), nullable=False)
    glucosa_ayuno: Mapped[float] = mapped_column(sa.Numeric(6, 2), nullable=False)
    hba1c: Mapped[float | None] = mapped_column(sa.Numeric(4, 1))
    presion_sistolica: Mapped[int] = mapped_column(sa.SmallInteger, nullable=False)
    presion_diastolica: Mapped[int] = mapped_column(sa.SmallInteger, nullable=False)
    antecedentes_familiares: Mapped[bool] = mapped_column(sa.Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now()
    )

    predictions: Mapped[list["Prediction"]] = sa.orm.relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    patient_id: Mapped[UUID] = mapped_column(
        sa.Uuid, sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    resultado: Mapped[DiabetesType] = mapped_column(diabetes_type_enum, nullable=False)
    probabilidad_tipo1: Mapped[float] = mapped_column(sa.Numeric(6, 5), nullable=False)
    probabilidad_tipo2: Mapped[float] = mapped_column(sa.Numeric(6, 5), nullable=False)
    probabilidad_gestacional: Mapped[float] = mapped_column(sa.Numeric(6, 5), nullable=False)
    probabilidad_sano: Mapped[float] = mapped_column(sa.Numeric(6, 5), nullable=False)

    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now()
    )

    patient: Mapped["Patient"] = sa.orm.relationship(back_populates="predictions")
