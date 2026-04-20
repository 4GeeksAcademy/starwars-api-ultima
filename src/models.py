from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favoritos_id: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="user_id")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,  
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_personaje: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    edad: Mapped[int] = mapped_column( nullable=False)
    genero: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="id_personajes")


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
    habitantes: Mapped[int] = mapped_column( nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="id_planetas")


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
    modelo: Mapped[int] = mapped_column( nullable=False)
    pasajeros: Mapped[int] = mapped_column( unique=True, nullable=False)
    favoritos: Mapped[List["Favoritos"]] = relationship("Favoritos", back_populates="id_vehiculos")


    def serialize(self):
        return {
            "id": self.id,
            "nombre_vehiculos": self.nombre_vehiculos,
            "modelo": self.modelo,
            "pasajeros": self.pasajeros
        }
class Favoritos(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        id_personajes: Mapped[int] = mapped_column(db.ForeignKey("personaje.id"),nullable=True)
        id_vehiculos: Mapped[int] = mapped_column(db.ForeignKey("vehiculos.id"),nullable=True)
        id_planetas: Mapped[int] = mapped_column(db.ForeignKey("planetas.id"),nullable=True)
        user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"),nullable=False)

        def serialize(self):
            return {
            "id": self.id,
            "id_personajes": self.id_personajes,
            "id_vehiculos": self.id_vehiculos,
            "id_planetas": self.id_planetas,
            "user_id": self.user_id
        }                                           
    