import streamlit as st
from config import *
from modules.auth import login_admin, login_asociado, cambiar_clave
from modules.admin import panel_admin, registrar_acceso

st.set_page_config(
    page_title=NOMBRE_FONDO,
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(f"""
<style>
    .stApp {{ background-color: {COLOR_FONDO}; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 0rem; padding-bottom: 2rem; max-width: 1200px; }}

    /* Navbar */
    .navbar {{
        background: {COLOR_PRIMARIO};
        padding: 14px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        margin-left: -4rem;
        margin-right: -4rem;
        margin-top: -1rem;
    }}
    .navbar-name {{ font-size: 15px; font-weight: 500; color: white; }}
    .navbar-sub {{ font-size: 11px; color: rgba(255,255,255,0.65); }}
    .navbar-icon {{
        width: 36px; height: 36px;
        background: rgba(255,255,255,0.2);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        margin-right: 10px; float: left;
    }}

    /* Login */
    .login-bg {{
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
    }}
    .login-card {{
        background: white;
        border-radius: 16px;
        border: 0.5px solid #E5E7EB;
        padding: 2.5rem 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    .login-logo-box {{
        width: 48px; height: 48px;
        background: {COLOR_PRIMARIO};
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 14px;
        font-size: 24px;
    }}
    .login-title {{
        font-size: 22px;
        font-weight: 500;
        color: {COLOR_TEXTO};
        margin-bottom: 2px;
    }}
    .login-org {{
        font-size: 12px;
        color: #9CA3AF;
        margin-bottom: 6px;
    }}
    .login-sub {{
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 1.4rem;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid #F3F4F6;
    }}
    .login-footer {{
        text-align: center;
        font-size: 11px;
        color: #9CA3AF;
        margin-top: 1.2rem;
        padding-top: 1rem;
        border-top: 1px solid #F3F4F6;
    }}

    /* Botones */
    .stButton > button {{
        background-color: {COLOR_PRIMARIO};
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 500;
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
        border: 0.5px solid #D1D5DB;
        background: #FAFAFA;
        color: #111827;
        font-size: 0.95rem;
        padding: 0.5rem 0.8rem;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {COLOR_PRIMARIO};
        box-shadow: 0 0 0 2px rgba(200,16,46,0.10);
    }}
    .stTextInput label p {{
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
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
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        border: 0.5px solid #E5E7EB;
        border-left: 4px solid {COLOR_PRIMARIO};
    }}
    div[data-testid="stMetricLabel"] p {{
        color: #6B7280 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {COLOR_TEXTO} !important;
        font-size: 1.5rem !important;
        font-weight: 500 !important;
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
        font-size: 0.88rem;
        color: #6B7280;
        border: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: white !important;
        color: {COLOR_PRIMARIO} !important;
        font-weight: 600;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }}

    /* Expanders */
    details summary {{
        background: #F9FAFB;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        color: {COLOR_TEXTO};
        border: 0.5px solid #E5E7EB;
    }}

    /* Títulos */
    h1, h2, h3, h4 {{
        color: {COLOR_TEXTO} !important;
    }}

    /* Tabla de accesos */
    .stDataFrame {{ border-radius: 10px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None


def navbar(nombre, rol):
    icono = "👑" if rol == "admin" else "👤"
    label = "Administrador" if rol == "admin" else "Asociado"
    st.markdown(f"""
    <div class="navbar">
        <div style="display:flex;align-items:center">
            <div style="width:36px;height:36px;background:rgba(255,255,255,0.2);border-radius:8px;
                        display:flex;align-items:center;justify-content:center;margin-right:12px;font-size:20px">
                🏦
            </div>
            <div>
                <div class="navbar-name">{NOMBRE_CORTO}</div>
                <div class="navbar-sub">{NOMBRE_FONDO}</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:14px">
            <div style="text-align:right">
                <div class="navbar-name">{icono} {nombre}</div>
                <div class="navbar-sub">{label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def pantalla_login():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:75vh">
            <div style="background:white;border-radius:16px;border:0.5px solid #E5E7EB;
                        padding:2.5rem 2rem;box-shadow:0 4px 20px rgba(0,0,0,0.06);width:100%">
                <div style="width:48px;height:48px;background:{COLOR_PRIMARIO};border-radius:12px;
                            display:flex;align-items:center;justify-content:center;
                            margin-bottom:14px;font-size:24px">🏦</div>
                <div style="font-size:22px;font-weight:500;color:{COLOR_TEXTO};margin-bottom:2px">{NOMBRE_CORTO}</div>
                <div style="font-size:12px;color:#9CA3AF;margin-bottom:6px">{NOMBRE_FONDO}</div>
                <div style="font-size:13px;color:#6B7280;margin-bottom:1.4rem;
                            padding-bottom:1.2rem;border-bottom:1px solid #F3F4F6">{MENSAJE_BIENVENIDA}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        perfil = st.radio("Ingresar como:", ["Asociado", "Administrador"], horizontal=True)
        st.divider()

        with st.form("form_login"):
            correo = st.text_input("Correo electrónico", placeholder="tucorreo@promedico.com.co")
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
                ok, datos, cambiar = login_asociado(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "asociado"
                    st.session_state.cambiar_clave = cambiar
                    registrar_acceso(datos["correo"], datos["nombre"], "asociado")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")

        st.markdown(f'<div class="login-footer">{NOMBRE_FONDO} · {CORREO_SOPORTE}</div>', unsafe_allow_html=True)


def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown(f"""
        <div style="background:white;border-radius:16px;border:0.5px solid #E5E7EB;
                    padding:2.5rem 2rem;box-shadow:0 4px 20px rgba(0,0,0,0.06);margin-top:3rem">
            <div style="font-size:22px;font-weight:500;color:{COLOR_TEXTO};margin-bottom:6px">🔐 Nueva contraseña</div>
            <div style="font-size:13px;color:#6B7280;margin-bottom:1.4rem;
                        padding-bottom:1.2rem;border-bottom:1px solid #F3F4F6">
                Es tu primer ingreso. Crea una contraseña segura.
            </div>
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


# ── Enrutador ────────────────────────────────────────────────
if st.session_state.usuario is None:
    pantalla_login()

elif st.session_state.perfil == "asociado" and st.session_state.get("cambiar_clave"):
    pantalla_cambiar_clave()

elif st.session_state.perfil == "admin":
    navbar(st.session_state.usuario["nombre"], "admin")
    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()
    panel_admin()

elif st.session_state.perfil == "asociado":
    from modules.asociado import dashboard_asociado
    navbar(st.session_state.usuario["nombre"], "asociado")
    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button("🚪 Salir"):
            st.session_state.clear()
            st.rerun()
    dashboard_asociado()