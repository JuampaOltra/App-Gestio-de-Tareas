import db
from sqlalchemy import Column, Integer, String, Boolean
from datetime import datetime

class Tarea(db.Base):
    __tablename__ = "tareaOk"
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    hecha = Column(Boolean)
    categoria = Column(String(50))
    fecha = Column(String(datetime))

    def __init__(self, contenido, hecha, categoria, fecha):
        self.contenido = contenido
        self.hecha = hecha
        self.categoria = categoria
        self.fecha = fecha

    def __str__(self):
        return "Tarea {} : {} {} {} {} ".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha)