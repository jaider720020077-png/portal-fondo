import streamlit as st
import os
import pandas as pd
from datetime import datetime
from modules.auth import (
    cargar_usuarios, guardar_usuarios,
    hashear_clave
)
from config import *

SALDOS_PATH = "data/saldos.xlsx"
ACCESOS_PATH = "data/accesos.xlsx"

# ── Registro de acceso ───────────────────────────────────────
def registrar_acceso(correo, nombre, perfil):
    try:
        if os.path.exists(ACCESOS_PATH):
            df = pd.read_excel(ACCESOS_PATH)
        else:
            df = pd.DataFrame(columns=["fecha", "hora", "correo", "nombre", "perfil"])
        nueva_fila = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M:%S"),
            "correo": correo,
            "nombre": nombre,
            "perfil": perfil
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(ACCESOS_PATH, index=False)
    except Exception:
        pass

# ── Panel principal ──────────────────────────────────────────
def panel_admin():
    st.markdown(f"### 👑 Panel de Administrador — {NOMBRE_CORTO}")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Usuarios",
        "📂 Carga de datos",
        "📋 Registro de accesos",
        "⚙️ Configuración"
    ])

    with tab1:
        seccion_usuarios()
    with tab2:
        seccion_carga_datos()
    with tab3:
        seccion_accesos()
    with tab4:
        seccion_configuracion()


# ── Sección: Usuarios ────────────────────────────────────────
def seccion_usuarios():
    st.markdown("#### Gestión de usuarios")

    subtab1, subtab2, subtab3 = st.tabs([
        "📋 Lista de usuarios",
        "➕ Crear usuario",
        "📥 Carga masiva"
    ])

    with subtab1:
        lista_usuarios()
    with subtab2:
        crear_usuario_individual()
    with subtab3:
        carga_masiva_usuarios()


def lista_usuarios():
    df = cargar_usuarios()
    empleados = df[df["perfil"] == "empleado"].copy()

    if empleados.empty:
        st.info("No hay empleados registrados todavía.")
        return

    st.markdown(f"**{len(empleados)} empleados registrados**")

    for _, fila in empleados.iterrows():
        with st.expander(f"{'🟢' if fila['activo'] == 1 else '🔴'} {fila['nombre']} — {fila['correo']}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                estado = "Activo" if fila["activo"] == 1 else "Inactivo"
                st.write(f"**Cédula:** {fila['cedula']}")
                st.write(f"**Estado:** {estado}")

            with col2:
                if fila["activo"] == 1:
                    if st.button("🔴 Desactivar", key=f"desact_{fila['correo']}"):
                        df.loc[df["correo"] == fila["correo"], "activo"] = 0
                        guardar_usuarios(df)
                        st.success("Usuario desactivado.")
                        st.rerun()
                else:
                    if st.button("🟢 Activar", key=f"act_{fila['correo']}"):
                        df.loc[df["correo"] == fila["correo"], "activo"] = 1
                        guardar_usuarios(df)
                        st.success("Usuario activado.")
                        st.rerun()

            with col3:
                if st.button("🔑 Resetear clave", key=f"reset_{fila['correo']}"):
                    df.loc[df["correo"] == fila["correo"], "clave_hash"] = "temporal123"
                    df.loc[df["correo"] == fila["correo"], "cambiar_clave"] = 1
                    guardar_usuarios(df)
                    st.success(f"Clave reseteada a: **temporal123**")
                    st.rerun()


def crear_usuario_individual():
    st.markdown("#### Crear empleado nuevo")

    with st.form("form_crear_usuario"):
        col1, col2 = st.columns(2)
        with col1:
            cedula = st.text_input("Cédula *")
            nombre = st.text_input("Nombre completo *")
        with col2:
            correo = st.text_input("Correo *")
            clave_temp = st.text_input(
                "Clave temporal *",
                value="temporal123",
                help="El empleado deberá cambiarla en su primer ingreso"
            )

        crear = st.form_submit_button("Crear usuario", use_container_width=True)

    if crear:
        if not cedula or not nombre or not correo:
            st.error("Todos los campos marcados con * son obligatorios.")
            return

        df = cargar_usuarios()

        if correo in df["correo"].values:
            st.error("Ya existe un usuario con ese correo.")
            return
        if cedula in df["cedula"].values:
            st.error("Ya existe un usuario con esa cédula.")
            return

        nueva_fila = {
            "cedula": cedula,
            "nombre": nombre,
            "correo": correo,
            "clave_hash": clave_temp,
            "perfil": "empleado",
            "activo": 1,
            "cambiar_clave": 1
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        guardar_usuarios(df)
        st.success(f"✅ Usuario **{nombre}** creado. Clave temporal: `{clave_temp}`")


def carga_masiva_usuarios():
    st.markdown("#### Carga masiva desde Excel")
    st.info("El archivo debe tener estas columnas: **cedula, nombre, correo**")

    archivo = st.file_uploader("Sube el Excel de empleados", type=["xlsx"])

    if archivo:
        try:
            df_nuevo = pd.read_excel(archivo, dtype={"cedula": str})
            columnas = ["cedula", "nombre", "correo"]

            if not all(col in df_nuevo.columns for col in columnas):
                st.error(f"El archivo debe tener las columnas: {', '.join(columnas)}")
                return

            df_nuevo = df_nuevo[columnas].dropna(subset=columnas)
            df = cargar_usuarios()

            nuevos = 0
            omitidos = 0

            for _, fila in df_nuevo.iterrows():
                if fila["correo"] in df["correo"].values or fila["cedula"] in df["cedula"].values:
                    omitidos += 1
                    continue

                nueva_fila = {
                    "cedula": fila["cedula"],
                    "nombre": fila["nombre"],
                    "correo": fila["correo"],
                    "clave_hash": "temporal123",
                    "perfil": "empleado",
                    "activo": 1,
                    "cambiar_clave": 1
                }
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
                nuevos += 1

            if nuevos > 0:
                guardar_usuarios(df)
                st.success(f"✅ Se crearon {nuevos} nuevo(s) usuario(s).")
            else:
                st.info("No se agregaron usuarios nuevos. Todos los correos o cédulas ya existen.")

            if omitidos > 0:
                st.warning(f"{omitidos} fila(s) omitida(s) por duplicados.")

        except Exception:
            st.error("Hubo un error al procesar el archivo. Verifica que el formato sea correcto.")