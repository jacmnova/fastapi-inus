import json
from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey, Text
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class UsuarioLog(Base):
    __tablename__ = "usuario_logs"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, index=True)
    fecha = Column(Date, default=datetime.now().date)
    hora = Column(Time, default=datetime.now().time)

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer)  # cantidad total de productos
    descuento = Column(Float)   # descuento aplicado (si aplica)
    ubicacion = Column(String)

    items = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "items_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))

    cant = Column(String)
    codigo = Column(String)
    descprov = Column(String)
    descrip = Column(String)
    dprice = Column(String)
    dpriced = Column(String)
    encar = Column(Integer)
    existen = Column(String)
    img = Column(String)
    lote = Column(String)
    nomprv = Column(String)
    oferta = Column(String, nullable=True)
    oprecio = Column(String)
    opreciod = Column(String)
    vence = Column(String)

    pedido = relationship("Pedido", back_populates="items")

class JSONEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class Pedidos(Base):
    __tablename__ = "pedidos_vendedor"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String)
    nombre = Column(String)
    proveed = Column(String)
    nomprv =  Column(String)
    codigo_cliente =  Column(String)
    nombre_cliente =  Column(String)
    Pedido = Column(JSONEncodedDict)
    diasCredito =  Column(String)
    montoFactura = Column(String)

    fecha = Column(Date, default=datetime.now().date)
    hora = Column(Time, default=datetime.now().time)
    estado = Column(String, default="Enviada")

    unidades = Column(Integer, default=0)
    valor_dolar = Column(Float, default=0.0)
    tasa_dia = Column(Float, default=0.0)