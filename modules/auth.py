import streamlit as st
import bcrypt
import pandas as pd
from modules.database import leer_hoja, escribir_hoja, actualizar_celda
from config import *

def cargar_usuarios():
    return leer_hoja("usuarios")

def guardar_usuarios(df):
    escribir_hoja("usuarios", df)

def hashear_clave(clave_texto):
    return bcrypt.hashpw(
        clave_texto.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verificar_clave(clave_texto, clave_hash):
    try:
        return bcrypt.checkpw(
            clave_texto.encode("utf-8"),
            clave_hash.encode("utf-8")
        )
    except Exception:
        return clave_texto == clave_hash

def login_admin(usuario, clave):
    df = cargar_usuarios()
    if df.empty:
        return False, None
    fila = df[df["correo"] == usuario]
    if fila.empty:
        return False, None
    fila = fila.iloc[0]
    if str(fila["perfil"]) != "admin" or str(fila["activo"]) != "1":
        return False, None
    if verificar_clave(clave, str(fila["clave_hash"])):
        if not str(fila["clave_hash"]).startswith("$2b$"):
            nuevo_hash = hashear_clave(clave)
            actualizar_celda("usuarios", "correo", usuario, "clave_hash", nuevo_hash)
        return True, fila.to_dict()
    return False, None

def login_asociado(correo, clave):
    df = cargar_usuarios()
    if df.empty:
        return False, None, False
    fila = df[df["correo"] == correo]
    if fila.empty:
        return False, None, False
    fila = fila.iloc[0]
    if str(fila["perfil"]) != "asociado" or str(fila["activo"]) != "1":
        return False, None, False
    if verificar_clave(clave, str(fila["clave_hash"])):
        if not str(fila["clave_hash"]).startswith("$2b$"):
            nuevo_hash = hashear_clave(clave)
            actualizar_celda("usuarios", "correo", correo, "clave_hash", nuevo_hash)
        debe_cambiar = str(fila["cambiar_clave"]) == "1"
        return True, fila.to_dict(), debe_cambiar
    return False, None, False

def cambiar_clave(correo, clave_nueva):
    nuevo_hash = hashear_clave(clave_nueva)
    actualizar_celda("usuarios", "correo", correo, "clave_hash", nuevo_hash)
    actualizar_celda("usuarios", "correo", correo, "cambiar_clave", "0")