import streamlit as st
import pandas as pd
from datetime import datetime
from modules.auth import cargar_usuarios, guardar_usuarios, hashear_clave
from modules.database import leer_hoja, escribir_hoja, agregar_fila
from config import *


def registrar_acceso(correo, nombre, perfil):
    try:
        fila = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M:%S"),
            "correo": correo,
            "nombre": nombre,
            "perfil": perfil
        }
        agregar_fila("accesos", fila)
    except Exception:
        pass


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
    df = df.astype(str)
    empleados = df[df["perfil"] == "empleado"].copy()

    if empleados.empty:
        st.info("No hay empleados registrados todavía.")
        return

    st.markdown(f"**{len(empleados)} empleados registrados**")

    for _, fila in empleados.iterrows():
        with st.expander(f"{'🟢' if fila['activo'] == '1' else '🔴'} {fila['nombre']} — {fila['correo']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Cédula:** {fila['cedula']}")
                st.write(f"**Estado:** {'Activo' if fila['activo'] == '1' else 'Inactivo'}")
            with col2:
                if fila["activo"] == "1":
                    if st.button("🔴 Desactivar", key=f"desact_{fila['correo']}"):
                        df.loc[df["correo"] == fila["correo"], "activo"] = "0"
                        guardar_usuarios(df)
                        st.toast("Usuario desactivado.", icon="🔴")
                        st.rerun()
                else:
                    if st.button("🟢 Activar", key=f"act_{fila['correo']}"):
                        df.loc[df["correo"] == fila["correo"], "activo"] = "1"
                        guardar_usuarios(df)
                        st.toast("Usuario activado.", icon="🟢")
                        st.rerun()
            with col3:
                if st.button("🔑 Resetear clave", key=f"reset_{fila['correo']}"):
                    df.loc[df["correo"] == fila["correo"], "clave_hash"] = "temporal123"
                    df.loc[df["correo"] == fila["correo"], "cambiar_clave"] = "1"
                    guardar_usuarios(df)
                    st.toast("Clave reseteada a: temporal123", icon="🔑")
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
            "activo": "1",
            "cambiar_clave": "1"
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
            df_nuevo = df_nuevo[columnas].dropna()
            st.dataframe(df_nuevo, use_container_width=True)
            st.markdown(f"**{len(df_nuevo)} empleados encontrados**")

            if st.button("✅ Confirmar carga masiva", use_container_width=True):
                df_actual = cargar_usuarios()
                creados = 0
                omitidos = 0
                for _, fila in df_nuevo.iterrows():
                    if fila["correo"] in df_actual["correo"].values:
                        omitidos += 1
                        continue
                    nueva_fila = {
                        "cedula": fila["cedula"],
                        "nombre": fila["nombre"],
                        "correo": fila["correo"],
                        "clave_hash": "temporal123",
                        "perfil": "empleado",
                        "activo": "1",
                        "cambiar_clave": "1"
                    }
                    df_actual = pd.concat(
                        [df_actual, pd.DataFrame([nueva_fila])],
                        ignore_index=True
                    )
                    creados += 1
                guardar_usuarios(df_actual)
                st.success(f"✅ {creados} usuarios creados. {omitidos} omitidos (ya existían).")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")


def seccion_carga_datos():
    st.markdown("#### Actualización mensual de saldos")
    st.info("Sube el Excel mensual con los saldos actualizados de todos los empleados.")

    archivo = st.file_uploader("Sube el Excel de saldos", type=["xlsx"], key="saldos")

    if archivo:
        try:
            df = pd.read_excel(archivo, dtype={"cedula": str})
            st.dataframe(df.head(10), use_container_width=True)
            st.markdown(f"**{len(df)} registros encontrados**")
            if st.button("✅ Confirmar actualización de saldos", use_container_width=True):
                escribir_hoja("saldos", df)
                st.success("✅ Saldos actualizados. Los empleados ya ven sus nuevos datos.")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")


def seccion_accesos():
    st.markdown("#### Registro de accesos")
    try:
        df = leer_hoja("accesos")
        if df.empty:
            st.info("Aún no hay registros de acceso.")
            return
        df = df.sort_values("fecha", ascending=False)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.info("Aún no hay registros de acceso.")


def seccion_configuracion():
    st.markdown("#### Cambiar contraseña del administrador")
    with st.form("form_cambiar_admin"):
        clave_actual = st.text_input("Contraseña actual", type="password")
        clave_nueva = st.text_input("Nueva contraseña", type="password")
        confirmar = st.text_input("Confirmar nueva contraseña", type="password")
        guardar = st.form_submit_button("Actualizar contraseña", use_container_width=True)

    if guardar:
        from modules.auth import login_admin, cambiar_clave
        ok, _ = login_admin(st.session_state.usuario["correo"], clave_actual)
        if not ok:
            st.error("La contraseña actual es incorrecta.")
        elif len(clave_nueva) < LONGITUD_MINIMA_CLAVE:
            st.error(f"Mínimo {LONGITUD_MINIMA_CLAVE} caracteres.")
        elif clave_nueva != confirmar:
            st.error("Las contraseñas no coinciden.")
        else:
            cambiar_clave(st.session_state.usuario["correo"], clave_nueva)
            st.success("✅ Contraseña actualizada correctamente.")