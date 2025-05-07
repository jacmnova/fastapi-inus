from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.responses import JSONResponse
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

conf = ConnectionConfig(
    MAIL_USERNAME = "portalProveedoresInsuaminca@gmail.com",
    MAIL_PASSWORD = "Insuaminca1q2w3e",
    MAIL_FROM = "portalProveedoresInsuaminca@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False
)

# Permitir origenes (ajusta según tus necesidades)
origins = [
    "http://localhost:3000",  # por ejemplo, si usas React
    "http://127.0.0.1:3000",
    "http://localhost",
    "*",  # ⚠️ solo en desarrollo, no en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # puede usar ["*"] para todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"API": "INSUAMINCA"}

@app.post("/log_usuario/")
def log_usuario(log: schemas.UsuarioLogCreate, db: Session = Depends(get_db)):
    db_log = models.UsuarioLog(usuario=log.usuario)
    db.add(db_log)
    db.commit()
    return {"mensaje": "Usuario registrado", "usuario": log.usuario}

@app.post("/pedidos/")
def crear_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    total_cantidad = sum(int(item.cant) for item in pedido.items)
    descuento = 0.0  # Podrías calcularlo si es necesario

    nuevo_pedido = models.Pedido(
        cantidad=total_cantidad,
        descuento=descuento,
        ubicacion=pedido.ubicacion
    )
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)

    for item in pedido.items:
        db_item = models.ItemPedido(**item.dict(), pedido_id=nuevo_pedido.id)
        db.add(db_item)

    db.commit()
    return {
        "mensaje": "Pedido creado correctamente",
        "pedido_id": nuevo_pedido.id,
        "total_unidades": total_cantidad
    }


@app.post("/pedidos_vendedor/")
def crear_pedido_vendedor(pedido: schemas.PedidoVendedorFormatoNuevo, db: Session = Depends(get_db)):
    # Calcular total de unidades
    total_unidades = sum(int(item.cant) for item in pedido.Pedido)

    # Calcular total en dólares
    total_dolares = sum(float(item.totald.replace(",", "")) for item in pedido.Pedido)

    # Extraer tasa desde el primer item (si todos tienen la misma)
    tasa_dia = float(pedido.Pedido[0].tasa.replace(",", "")) if pedido.Pedido else 0.0

    db_pedido = models.Pedidos(
        usuario=pedido.usuario,
        nombre=pedido.nombre,
        proveed=pedido.proveed,
        nomprv=pedido.nomprv,
        codigo_cliente=pedido.codigo_cliente,
        nombre_cliente=pedido.nombre_cliente,
        Pedido=[item.dict() for item in pedido.Pedido],
        unidades=total_unidades,
        valor_dolar=total_dolares,
        tasa_dia=tasa_dia,
        diasCredito=pedido.diasCredito,
        montoFactura=pedido.montoFactura,
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return {
        "mensaje": "Pedido creado correctamente",
        "pedido_id": db_pedido.id,
        "unidades": total_unidades,
        "valor_dolar": total_dolares,
        "tasa_dia": tasa_dia
    }


@app.put("/pedidos_vendedor/{pedido_id}/estado")
def actualizar_estado(pedido_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedido_id).first()
    if not pedido:
        return {"error": "Pedido no encontrado"}
    pedido.estado = nuevo_estado
    db.commit()
    return {"mensaje": f"Estado actualizado a '{nuevo_estado}'", "pedido_id": pedido_id}

@app.get("/pedidos_vendedor/usuario/{usuario}")
def pedidos_por_usuario(usuario: str, db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedidos).filter(models.Pedidos.usuario == usuario).all()
    return pedidos

@app.get("/pedidos_vendedor/proveedor/{proveed}")
def pedidos_por_proveedor(proveed: str, db: Session = Depends(get_db)):
    pedidos = db.query(models.Pedidos).filter(models.Pedidos.proveed == proveed).all()
    return pedidos

# @app.get("/envio_email/confimar_pedidos/{email}/{idPedido}")
# async def envio_email(email: str, idPedido: int, db: Session = Depends(get_db)):
#     pedido = db.query(models.Pedidos).filter(models.Pedidos.id == idPedido).first()
#     if not pedido:
#         return JSONResponse(status_code=404, content={"error": "Pedido no encontrado"})

#     # Formatear el contenido del correo electrónico
#     items_pedido = ""
#     if pedido.Pedido:
#         for item in pedido.Pedido:
#             items_pedido += f"""
#                 - Código: {item.get('codigoa', 'N/A')}
#                   Descripción: {item.get('descrip', 'N/A')}
#                   Cantidad: {item.get('cant', 'N/A')}
#                   Precio Unitario $: {item.get('preciod', 'N/A')}
#                   Total $: {item.get('totald', 'N/A')}
#             """
#     else:
#         items_pedido = "No hay items en este pedido."

#     body = f"""
#     Hola, {pedido.nombre_cliente}!

#     Gracias por tu pedido con número de referencia: {pedido.id}.

#     Detalles del pedido:
#     Proveedor: {pedido.nomprv}
#     Fecha y Hora: {pedido.fecha} {pedido.hora.strftime('%H:%M:%S')}
#     Total de Unidades: {pedido.unidades}
#     Valor Total en Dólares: ${pedido.valor_dolar:.2f}
#     Tasa del Día: {pedido.tasa_dia:.2f} Bs/$

#     Productos:
#     {items_pedido}

#     ¡Gracias por tu compra!
#     """

#     message = MessageSchema(
#         subject=f"Confirmación de Pedido #{pedido.id}",
#         recipients=[email],
#         body=body,
#         subtype="plain"  # Puedes usar "html" si quieres formato HTML
#     )

#     fm = FastMail(conf)
#     try:
#         await fm.send_message(message)
#         return {"mensaje": f"Correo de confirmación enviado a {email}", "pedido_id": pedido.id}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": f"Error al enviar el correo: {str(e)}"})
