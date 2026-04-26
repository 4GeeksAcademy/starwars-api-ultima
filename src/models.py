from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
   

    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email
        }


class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_personaje: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    edad: Mapped[int] = mapped_column(nullable=False)
    genero: Mapped[str] = mapped_column(String(120), nullable=False)

    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_personaje": self.nombre_personaje,
            "edad": self.edad,
            "genero": self.genero,
        }


class Planetas(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_planetas: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    habitantes: Mapped[int] = mapped_column(nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(120), nullable=False)

    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_planetas": self.nombre_planetas,
            "habitantes": self.habitantes,
            "ubicacion": self.ubicacion,
        }


class Vehiculos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_vehiculos: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    modelo: Mapped[str] = mapped_column(String(120), nullable=False)
    pasajeros: Mapped[int] = mapped_column(nullable=False)

    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="vehiculo")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_vehiculos": self.nombre_vehiculos,
            "modelo": self.modelo,
            "pasajeros": self.pasajeros
        }


class Favoritos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    id_personajes: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=True)
    id_vehiculos: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=True)
    id_planetas: Mapped[int] = mapped_column(ForeignKey("planetas.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favoritos")
    personaje: Mapped["Personaje"] = relationship("Personaje", back_populates="favoritos")
    vehiculo: Mapped["Vehiculos"] = relationship("Vehiculos", back_populates="favoritos")
    planeta: Mapped["Planetas"] = relationship("Planetas", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "id_personajes": self.id_personajes,
            "id_vehiculos": self.id_vehiculos,
            "id_planetas": self.id_planetas,
            "personaje": self.personaje.serialize() if self.personaje else None,
            "vehiculo": self.vehiculo.serialize() if self.vehiculo else None,
            "planeta": self.planeta.serialize() if self.planeta else None
        }

    def __repr__(self):
        return f'<Favorito {self.id}>'