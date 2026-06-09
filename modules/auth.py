import streamlit as st
import pandas as pd
import bcrypt
import os
from config import *

USUARIOS_PATH = "data/usuarios.xlsx"

def cargar_usuarios():
    if os.path.exists(USUARIOS_PATH):
        return pd.read_excel(USUARIOS_PATH, dtype={"cedula": str})
    return pd.DataFrame(columns=[
        "cedula", "nombre", "correo", 
        "clave_hash", "perfil", "activo", "cambiar_clave"
    ])

def guardar_usuarios(df):
    df.to_excel(USUARIOS_PATH, index=False)

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
        # Clave aún no hasheada (primera vez)
        return clave_texto == clave_hash

def login_admin(usuario, clave):
    df = cargar_usuarios()
    fila = df[df["correo"] == usuario]
    if fila.empty:
        return False, None
    fila = fila.iloc[0]
    if fila["perfil"] != "admin" or fila["activo"] != 1:
        return False, None
    if verificar_clave(clave, str(fila["clave_hash"])):
        # Si la clave no está hasheada, la hasheamos ahora
        if not str(fila["clave_hash"]).startswith("$2b$"):
            df.loc[df["correo"] == usuario, "clave_hash"] = hashear_clave(clave)
            guardar_usuarios(df)
        return True, fila.to_dict()
    return False, None

def login_empleado(correo, clave):
    df = cargar_usuarios()
    fila = df[df["correo"] == correo]
    if fila.empty:
        return False, None, False
    fila = fila.iloc[0]
    if fila["perfil"] != "empleado" or fila["activo"] != 1:
        return False, None, False
    if verificar_clave(clave, str(fila["clave_hash"])):
        if not str(fila["clave_hash"]).startswith("$2b$"):
            df.loc[df["correo"] == correo, "clave_hash"] = hashear_clave(clave)
            guardar_usuarios(df)
        debe_cambiar = fila["cambiar_clave"] == 1
        return True, fila.to_dict(), debe_cambiar
    return False, None, False

def cambiar_clave(correo, clave_nueva):
    df = cargar_usuarios()
    df.loc[df["correo"] == correo, "clave_hash"] = hashear_clave(clave_nueva)
    df.loc[df["correo"] == correo, "cambiar_clave"] = 0
    guardar_usuarios(df)