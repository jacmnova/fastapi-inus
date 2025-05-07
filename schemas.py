from pydantic import BaseModel, validator
from typing import List, Optional, Union


class UsuarioLogCreate(BaseModel):
    usuario: str

class ItemPedidoCreate(BaseModel):
    cant: str
    codigo: str
    descprov: str
    descrip: str
    dprice: str
    dpriced: str
    encar: int
    existen: str
    img: str
    lote: str
    nomprv: str
    oferta: Optional[str] = None
    oprecio: str
    opreciod: str
    vence: str

class PedidoCreate(BaseModel):
    ubicacion: str
    items: List[ItemPedidoCreate]

class PedidoVendedorCreate(BaseModel):
    usuario: str
    nombre: str
    proveed: str
    nomprv: str
    codigo_cliente: str
    nombre_cliente: str
    Pedido: List[ItemPedidoCreate]


class ItemFormatoPedidoCreate(BaseModel):
    barras: Union[str, int]
    bssiniva: Union[str, float]
    cant: Union[str, int]
    cod_cli: Union[str, int]
    codigoa: Union[str, int]
    dconiva: Union[str, float]
    descprov: Union[str, float]
    descrip: str
    descu: Union[str, int]
    dsiniva: Union[str, float]
    escala: Union[str, float]
    existen: Union[str, float]
    id_pedido: Union[str, int]
    img: str
    iva: Union[str, float]
    ivabs: Union[str, float]
    ivad: Union[str, float]
    lote: str
    oprecio: Union[str, float]
    preciod: Union[str, float]
    preciosiniva: Union[str, float]
    segmento: Optional[Union[str, int]] = "0"
    tasa: Union[str, float]
    tivabs: Union[str, float]
    tivad: Union[str, float]
    totalbs: Union[str, float]
    totald: Union[str, float]
    vence: str

    @validator('*', pre=True)
    def convertir_a_str(cls, v):
        return str(v) if v is not None else ""

class PedidoVendedorFormatoNuevo(BaseModel):
    usuario: str
    nombre: str
    proveed: str
    nomprv: str
    codigo_cliente: str
    nombre_cliente: str
    Pedido: List[ItemFormatoPedidoCreate]
    diasCredito: str
    montoFactura: str