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

st.markdown(f"""
<style>
    .stApp {{ background-color: #F0F4F8; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px; }}

    /* Navbar superior */
    .navbar {{
        background: {COLOR_PRIMARIO};
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }}
    .navbar-title {{ font-size: 1.3rem; font-weight: 700; color: white; }}
    .navbar-sub {{ font-size: 0.85rem; color: rgba(255,255,255,0.75); }}

    /* Tarjeta blanca */
    .card {{
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }}

    /* Título de sección */
    .section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {COLOR_PRIMARIO};
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {COLOR_SECUNDARIO};
    }}

    /* Login card */
    .login-wrapper {{
        background: white;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        box-shadow: 0 4px 24px rgba(44,62,122,0.12);
    }}
    .login-logo {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {COLOR_PRIMARIO};
        margin-bottom: 0.2rem;
    }}
    .login-sub {{
        font-size: 0.95rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
    }}

    /* Botones */
    .stButton > button {{
        background-color: {COLOR_PRIMARIO};
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.55rem 1.2rem;
        width: 100%;
        transition: background 0.2s;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_SECUNDARIO} !important;
        color: white !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1.5px solid #D1D5DB;
        background: #FAFAFA;
        color: #111827;
        font-size: 0.95rem;
        padding: 0.5rem 0.8rem;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {COLOR_PRIMARIO};
        box-shadow: 0 0 0 2px rgba(44,62,122,0.12);
    }}
    .stTextInput label, .stTextInput p {{
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }}

    /* Radio */
    div[data-testid="stRadio"] label p {{
        color: #374151 !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stRadio"] > label > div > p {{
        color: {COLOR_PRIMARIO} !important;
        font-weight: 600 !important;
    }}

    /* Métricas */
    div[data-testid="stMetric"] {{
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(44,62,122,0.08);
        border-top: 4px solid {COLOR_PRIMARIO};
    }}
    div[data-testid="stMetricLabel"] p {{
        color: #6B7280 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {COLOR_PRIMARIO} !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: #F3F4F6;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
        border-bottom: none;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.45rem 1.1rem;
        font-weight: 500;
        font-size: 0.9rem;
        color: #6B7280;
        border: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: white !important;
        color: {COLOR_PRIMARIO} !important;
        font-weight: 700;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background: #F9FAFB;
        border-radius: 8px;
        font-weight: 500;
        color: {COLOR_TEXTO};
    }}

    /* Títulos Streamlit */
    h1, h2, h3, h4 {{
        color: {COLOR_PRIMARIO} !important;
    }}

    /* Footer */
    .footer {{
        text-align: center;
        color: #9CA3AF;
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
    }}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None


def pantalla_login():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown(f"""
        <div class="login-wrapper">
            <div class="login-logo">💼 {NOMBRE_CORTO}</div>
            <div class="login-sub">{MENSAJE_BIENVENIDA}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

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

        st.markdown(f'<div class="footer">{NOMBRE_FONDO} · {CORREO_SOPORTE}</div>', unsafe_allow_html=True)


def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown(f"""
        <div class="login-wrapper">
            <div class="login-logo">🔐 Nueva contraseña</div>
            <div class="login-sub">Es tu primer ingreso. Crea una contraseña segura.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("form_cambiar"):
            nueva     = st.text_input("Nueva contraseña", type="password", placeholder="Mínimo 8 caracteres")
            confirmar = st.text_input("Confirmar contraseña", type="password")
            guardar   = st.form_submit_button("Guardar contraseña →", use_container_width=True)

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


def barra_superior(nombre_usuario, perfil):
    icono = "👑" if perfil == "admin" else "👤"
    rol   = "Administrador" if perfil == "admin" else "Empleado"
    st.markdown(f"""
    <div class="navbar">
        <div>
            <div class="navbar-title">💼 {NOMBRE_CORTO}</div>
            <div class="navbar-sub">{NOMBRE_FONDO}</div>
        </div>
        <div style="text-align:right">
            <div class="navbar-title">{icono} {nombre_usuario}</div>
            <div class="navbar-sub">{rol}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


if st.session_state.usuario is None:
    pantalla_login()

elif st.session_state.perfil == "empleado" and st.session_state.get("cambiar_clave"):
    pantalla_cambiar_clave()

elif st.session_state.perfil == "admin":
    barra_superior(st.session_state.usuario["nombre"], "admin")
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()
    panel_admin()

elif st.session_state.perfil == "empleado":
    from modules.empleado import dashboard_empleado
    barra_superior(st.session_state.usuario["nombre"], "empleado")
    col1, col2 = st.columns([9, 1])
    with col2:
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()
    dashboard_empleado()