import streamlit as st
from config import *
from modules.auth import login_admin, login_empleado, cambiar_clave
from modules.admin import panel_admin, registrar_acceso

st.set_page_config(
    page_title=NOMBRE_FONDO,
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilos globales ─────────────────────────────────────────
st.markdown(f"""
<style>
    /* Fondo general */
    .stApp {{
        background-color: {COLOR_FONDO};
    }}

    /* Ocultar header y footer de Streamlit */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    /* Contenedor principal */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }}

    /* Tarjeta de login */
    .login-card {{
        background: white;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        box-shadow: 0 4px 24px rgba(44, 62, 122, 0.10);
        margin-top: 2rem;
    }}

    /* Título del portal */
    .portal-title {{
        color: {COLOR_PRIMARIO};
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }}

    /* Subtítulo */
    .portal-sub {{
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }}

    /* Botón principal */
    .stButton > button {{
        background-color: {COLOR_PRIMARIO};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: background 0.2s;
        width: 100%;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_SECUNDARIO};
        color: white;
    }}

    /* Inputs */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1.5px solid #E5E7EB;
        padding: 0.5rem 0.8rem;
        font-size: 1rem;
        background: white;
        color: {COLOR_TEXTO};
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {COLOR_PRIMARIO};
        box-shadow: 0 0 0 2px rgba(44,62,122,0.10);
    }}

    /* Radio buttons */
    .stRadio > div {{
        gap: 1rem;
    }}

    /* Métricas del dashboard */
    [data-testid="stMetric"] {{
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(44,62,122,0.07);
        border-left: 4px solid {COLOR_PRIMARIO};
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem;
        color: #6B7280;
        font-weight: 500;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {COLOR_PRIMARIO};
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        color: #6B7280;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: white;
        color: {COLOR_PRIMARIO};
        font-weight: 700;
        border-bottom: 2px solid {COLOR_PRIMARIO};
    }}

    /* Divider */
    hr {{
        border-color: #E5E7EB;
        margin: 1rem 0;
    }}

    /* Encabezado del panel */
    .panel-header {{
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(44,62,122,0.07);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    /* Pie de página */
    .footer {{
        text-align: center;
        color: #9CA3AF;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
    }}
</style>
""", unsafe_allow_html=True)

# ── Estado de sesión ─────────────────────────────────────────
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None


# ── Pantalla de login ────────────────────────────────────────
def pantalla_login():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f'<p class="portal-title">💼 {NOMBRE_CORTO}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="portal-sub">{MENSAJE_BIENVENIDA}</p>', unsafe_allow_html=True)

        perfil = st.radio("Ingresar como:", ["Empleado", "Administrador"], horizontal=True)
        st.divider()

        with st.form("form_login"):
            correo = st.text_input("Correo electrónico", placeholder="tucorreo@promedico.com")
            clave  = st.text_input("Contraseña", type="password", placeholder="••••••••")
            ingresar = st.form_submit_button("Ingresar →", use_container_width=True)

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

        st.markdown(f'<p class="footer">{NOMBRE_FONDO} · {CORREO_SOPORTE}</p>', unsafe_allow_html=True)


# ── Pantalla cambio de clave ─────────────────────────────────
def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f'<p class="portal-title">🔐 Nueva contraseña</p>', unsafe_allow_html=True)
        st.markdown('<p class="portal-sub">Es tu primer ingreso. Crea una contraseña segura.</p>', unsafe_allow_html=True)

        with st.form("form_cambiar"):
            nueva    = st.text_input("Nueva contraseña", type="password", placeholder="Mínimo 8 caracteres")
            confirmar = st.text_input("Confirmar contraseña", type="password")
            guardar  = st.form_submit_button("Guardar contraseña →", use_container_width=True)

        if guardar:
            if len(nueva) < LONGITUD_MINIMA_CLAVE:
                st.error(f"Mínimo {LONGITUD_MINIMA_CLAVE} caracteres.")
            elif nueva != confirmar:
                st.error("Las contraseñas no coinciden.")
            else:
                cambiar_clave(st.session_state.usuario["correo"], nueva)
                st.session_state.cambiar_clave = False
                st.success("¡Contraseña actualizada!")
                st.rerun()


# ── Barra superior ───────────────────────────────────────────
def barra_superior(titulo):
    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(f"### {titulo}")
    with col2:
        if st.button("🚪 Salir", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    st.divider()


# ── Enrutador principal ──────────────────────────────────────
if st.session_state.usuario is None:
    pantalla_login()

elif st.session_state.perfil == "empleado" and st.session_state.get("cambiar_clave"):
    pantalla_cambiar_clave()

elif st.session_state.perfil == "admin":
    barra_superior(f"👑 Panel Administrador — {NOMBRE_CORTO}")
    panel_admin()

elif st.session_state.perfil == "empleado":
    from modules.empleado import dashboard_empleado
    barra_superior(f"💼 {NOMBRE_CORTO} — {st.session_state.usuario['nombre']}")
    dashboard_empleado()