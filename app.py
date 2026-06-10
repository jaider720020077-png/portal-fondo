import streamlit as st
from config import *
from modules.auth import login_admin, login_empleado, cambiar_clave

st.set_page_config(
    page_title=NOMBRE_FONDO,
    page_icon="💼",
    layout="wide"
)

# ── Estilos básicos ──────────────────────────────────────────
st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; }}
    .login-title {{ 
        color: {COLOR_PRIMARIO}; 
        font-size: 1.8rem; 
        font-weight: 700; 
        margin-bottom: 0.2rem;
    }}
    .login-sub {{ 
        color: {COLOR_TEXTO}; 
        font-size: 1rem; 
        margin-bottom: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

# ── Inicializar sesión ───────────────────────────────────────
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None

# ── Pantalla de login ────────────────────────────────────────
def pantalla_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f'<p class="login-title">💼 {NOMBRE_CORTO}</p>', 
                    unsafe_allow_html=True)
        st.markdown(f'<p class="login-sub">{MENSAJE_BIENVENIDA}</p>', 
                    unsafe_allow_html=True)

        perfil = st.radio("Ingresar como:", 
                          ["Empleado", "Administrador"], 
                          horizontal=True)
        st.divider()

        with st.form("form_login"):
            correo = st.text_input("Correo", placeholder="tucorreo@promedico.com")
            clave = st.text_input("Contraseña", type="password")
            ingresar = st.form_submit_button("Ingresar", use_container_width=True)

        if ingresar:
            if not correo or not clave:
                st.error("Por favor completa todos los campos.")
                return

            if perfil == "Administrador":
                ok, datos = login_admin(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "admin"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")

            else:
                ok, datos, cambiar = login_empleado(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "empleado"
                    st.session_state.cambiar_clave = cambiar
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")

# ── Pantalla cambio de clave ─────────────────────────────────
def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🔐 Cambia tu contraseña")
        st.info("Es tu primer ingreso. Debes crear una contraseña nueva.")

        with st.form("form_cambiar"):
            nueva = st.text_input("Nueva contraseña", type="password")
            confirmar = st.text_input("Confirmar contraseña", type="password")
            guardar = st.form_submit_button("Guardar", use_container_width=True)

        if guardar:
            if len(nueva) < LONGITUD_MINIMA_CLAVE:
                st.error(f"La contraseña debe tener al menos {LONGITUD_MINIMA_CLAVE} caracteres.")
            elif nueva != confirmar:
                st.error("Las contraseñas no coinciden.")
            else:
                cambiar_clave(st.session_state.usuario["correo"], nueva)
                st.session_state.cambiar_clave = False
                st.success("¡Contraseña actualizada! Redirigiendo...")
                st.rerun()

# ── Enrutador principal ──────────────────────────────────────
import streamlit as st
from config import *
from modules.auth import login_admin, login_empleado, cambiar_clave
from modules.admin import panel_admin, registrar_acceso

st.set_page_config(
    page_title=NOMBRE_FONDO,
    page_icon="💼",
    layout="wide"
)

st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; }}
    .login-title {{ 
        color: {COLOR_PRIMARIO}; 
        font-size: 1.8rem; 
        font-weight: 700; 
        margin-bottom: 0.2rem;
    }}
    .login-sub {{ 
        color: {COLOR_TEXTO}; 
        font-size: 1rem; 
        margin-bottom: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None

def pantalla_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f'<p class="login-title">💼 {NOMBRE_CORTO}</p>',
                    unsafe_allow_html=True)
        st.markdown(f'<p class="login-sub">{MENSAJE_BIENVENIDA}</p>',
                    unsafe_allow_html=True)

        perfil = st.radio("Ingresar como:",
                          ["Empleado", "Administrador"],
                          horizontal=True)
        st.divider()

        with st.form("form_login"):
            correo = st.text_input("Correo", placeholder="tucorreo@promedico.com")
            clave = st.text_input("Contraseña", type="password")
            ingresar = st.form_submit_button("Ingresar", use_container_width=True)

        if ingresar:
            if not correo or not clave:
                st.error("Por favor completa todos los campos.")
                return

            if perfil == "Administrador":
                ok, datos = login_admin(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "admin"
                    registrar_acceso(datos["correo"], datos["nombre"], "admin")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
            else:
                ok, datos, cambiar = login_empleado(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "empleado"
                    st.session_state.cambiar_clave = cambiar
                    registrar_acceso(datos["correo"], datos["nombre"], "empleado")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")

def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🔐 Cambia tu contraseña")
        st.info("Es tu primer ingreso. Debes crear una contraseña nueva.")

        with st.form("form_cambiar"):
            nueva = st.text_input("Nueva contraseña", type="password")
            confirmar = st.text_input("Confirmar contraseña", type="password")
            guardar = st.form_submit_button("Guardar", use_container_width=True)

        if guardar:
            if len(nueva) < LONGITUD_MINIMA_CLAVE:
                st.error(f"La contraseña debe tener al menos {LONGITUD_MINIMA_CLAVE} caracteres.")
            elif nueva != confirmar:
                st.error("Las contraseñas no coinciden.")
            else:
                cambiar_clave(st.session_state.usuario["correo"], nueva)
                st.session_state.cambiar_clave = False
                st.success("¡Contraseña actualizada!")
                st.rerun()

# ── Enrutador principal ──────────────────────────────────────
import streamlit as st
from config import *
from modules.auth import login_admin, login_empleado, cambiar_clave
from modules.admin import panel_admin, registrar_acceso

st.set_page_config(
    page_title=NOMBRE_FONDO,
    page_icon="💼",
    layout="wide"
)

st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; }}
    .login-title {{ 
        color: {COLOR_PRIMARIO}; 
        font-size: 1.8rem; 
        font-weight: 700; 
        margin-bottom: 0.2rem;
    }}
    .login-sub {{ 
        color: {COLOR_TEXTO}; 
        font-size: 1rem; 
        margin-bottom: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None

def pantalla_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f'<p class="login-title">💼 {NOMBRE_CORTO}</p>',
                    unsafe_allow_html=True)
        st.markdown(f'<p class="login-sub">{MENSAJE_BIENVENIDA}</p>',
                    unsafe_allow_html=True)

        perfil = st.radio("Ingresar como:",
                          ["Empleado", "Administrador"],
                          horizontal=True)
        st.divider()

        with st.form("form_login"):
            correo = st.text_input("Correo", placeholder="tucorreo@promedico.com")
            clave = st.text_input("Contraseña", type="password")
            ingresar = st.form_submit_button("Ingresar", use_container_width=True)

        if ingresar:
            if not correo or not clave:
                st.error("Por favor completa todos los campos.")
                return

            if perfil == "Administrador":
                ok, datos = login_admin(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "admin"
                    registrar_acceso(datos["correo"], datos["nombre"], "admin")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
            else:
                ok, datos, cambiar = login_empleado(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "empleado"
                    st.session_state.cambiar_clave = cambiar
                    registrar_acceso(datos["correo"], datos["nombre"], "empleado")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")

def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🔐 Cambia tu contraseña")
        st.info("Es tu primer ingreso. Debes crear una contraseña nueva.")

        with st.form("form_cambiar"):
            nueva = st.text_input("Nueva contraseña", type="password")
            confirmar = st.text_input("Confirmar contraseña", type="password")
            guardar = st.form_submit_button("Guardar", use_container_width=True)

        if guardar:
            if len(nueva) < LONGITUD_MINIMA_CLAVE:
                st.error(f"La contraseña debe tener al menos {LONGITUD_MINIMA_CLAVE} caracteres.")
            elif nueva != confirmar:
                st.error("Las contraseñas no coinciden.")
            else:
                cambiar_clave(st.session_state.usuario["correo"], nueva)
                st.session_state.cambiar_clave = False
                st.success("¡Contraseña actualizada!")
                st.rerun()

# ── Enrutador principal ──────────────────────────────────────
if st.session_state.usuario is None:
    pantalla_login()

elif st.session_state.perfil == "empleado" and st.session_state.get("cambiar_clave"):
    pantalla_cambiar_clave()

elif st.session_state.perfil == "admin":
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()
    panel_admin()

elif st.session_state.perfil == "empleado":
    from modules.empleado import dashboard_empleado
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()
    dashboard_empleado()