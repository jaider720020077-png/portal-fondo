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
    .stApp {{ background-color: #F5F6FA; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}

    /* Sidebar */
    .sidebar-container {{
        position: fixed;
        left: 0; top: 0; bottom: 0;
        width: 240px;
        background: #1A1A2E;
        z-index: 100;
        display: flex;
        flex-direction: column;
        padding: 0;
    }}
    .sidebar-header {{
        padding: 20px 18px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .sidebar-logo {{
        width: 40px; height: 40px;
        background: {COLOR_PRIMARIO};
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; margin-bottom: 10px;
    }}
    .sidebar-name {{ font-size: 15px; font-weight: 600; color: white; }}
    .sidebar-org {{ font-size: 11px; color: rgba(255,255,255,0.4); margin-top: 2px; }}

    .sidebar-user {{
        padding: 14px 18px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        display: flex; align-items: center; gap: 10px;
    }}
    .user-avatar {{
        width: 36px; height: 36px;
        background: {COLOR_PRIMARIO};
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 13px; font-weight: 600; color: white; flex-shrink: 0;
    }}
    .user-info-name {{ font-size: 12px; font-weight: 500; color: white; line-height: 1.3; }}
    .user-info-role {{ font-size: 10px; color: rgba(255,255,255,0.4); }}

    .nav-section {{ padding: 14px 10px 6px; flex: 1; }}
    .nav-label {{
        font-size: 10px; color: rgba(255,255,255,0.3);
        text-transform: uppercase; letter-spacing: 0.08em;
        padding: 0 8px; margin-bottom: 6px; margin-top: 10px;
    }}

    .sidebar-footer {{
        padding: 12px 10px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }}

    /* Topbar */
    .topbar {{
        background: white;
        padding: 14px 28px;
        border-bottom: 1px solid #EBEBEB;
        display: flex; align-items: center; justify-content: space-between;
    }}
    .topbar-title {{ font-size: 16px; font-weight: 600; color: #1A1A2E; }}
    .topbar-sub {{ font-size: 12px; color: #9CA3AF; margin-top: 2px; }}
    .topbar-badge {{
        background: #FFF0F2; color: {COLOR_PRIMARIO};
        border: 0.5px solid #FECDD3;
        border-radius: 20px; padding: 4px 12px;
        font-size: 11px; font-weight: 500;
    }}

    /* Contenido principal */
    .main-content {{
        margin-left: 240px;
        min-height: 100vh;
        background: #F5F6FA;
    }}
    .page-content {{ padding: 24px 28px; }}

    /* Login */
    .login-split {{
        display: flex;
        width: 680px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(0,0,0,0.13);
    }}
    .login-left {{
        width: 220px;
        background: #1A1A2E;
        padding: 32px 24px;
        display: flex; flex-direction: column; justify-content: space-between;
        flex-shrink: 0;
    }}
    .login-right {{
        flex: 1; background: white; padding: 32px 28px;
        display: flex; flex-direction: column; justify-content: center;
    }}
    .login-right-title {{ font-size: 20px; font-weight: 600; color: #1A1A2E; margin-bottom: 4px; }}
    .login-right-sub {{ font-size: 13px; color: #9CA3AF; margin-bottom: 22px; padding-bottom: 18px; border-bottom: 1px solid #F3F4F6; }}
    .login-footer {{ font-size: 10px; color: rgba(255,255,255,0.3); line-height: 1.6; }}

    /* Botones */
    .stButton > button {{
        background-color: {COLOR_PRIMARIO} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: background 0.2s !important;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_SECUNDARIO} !important;
        color: white !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input {{
        border-radius: 8px !important;
        border: 0.5px solid #D1D5DB !important;
        background: #FAFAFA !important;
        color: #111827 !important;
        font-size: 0.9rem !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: {COLOR_PRIMARIO} !important;
        box-shadow: 0 0 0 2px rgba(200,16,46,0.10) !important;
    }}
    .stTextInput label p {{
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}

    /* Radio */
    div[data-testid="stRadio"] label p {{
        color: #374151 !important;
        font-weight: 500 !important;
    }}

    /* Métricas */
    div[data-testid="stMetric"] {{
        background: white !important;
        border-radius: 10px !important;
        padding: 1.2rem 1.5rem !important;
        border: 0.5px solid #EBEBEB !important;
        border-left: 4px solid {COLOR_PRIMARIO} !important;
    }}
    div[data-testid="stMetricLabel"] p {{
        color: #6B7280 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: #1A1A2E !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: #F3F4F6 !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 4px !important;
        border-bottom: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        color: #6B7280 !important;
        border: none !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: white !important;
        color: {COLOR_PRIMARIO} !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }}

    /* Títulos */
    h1, h2, h3, h4 {{ color: #1A1A2E !important; }}

    /* Dataframe */
    .stDataFrame {{ border-radius: 10px !important; overflow: hidden !important; }}

    /* Selectbox */
    .stSelectbox label p {{ color: #374151 !important; font-weight: 500 !important; font-size: 0.85rem !important; }}

    /* Form */
    .stForm {{ background: white !important; border-radius: 12px !important; padding: 1.5rem !important; border: 0.5px solid #EBEBEB !important; }}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "perfil" not in st.session_state:
    st.session_state.perfil = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "resumen"


def iniciales(nombre):
    partes = nombre.strip().split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[1][0]).upper()
    return nombre[:2].upper()


def sidebar_admin():
    nombre = st.session_state.usuario["nombre"]
    ini = iniciales(nombre)
    pagina = st.session_state.get("pagina", "usuarios")

    st.markdown(f"""
    <div class="sidebar-container">
        <div class="sidebar-header">
            <div class="sidebar-logo">🏦</div>
            <div class="sidebar-name">{NOMBRE_CORTO}</div>
            <div class="sidebar-org">{NOMBRE_FONDO}</div>
        </div>
        <div class="sidebar-user">
            <div class="user-avatar">{ini}</div>
            <div>
                <div class="user-info-name">{nombre}</div>
                <div class="user-info-role">Administrador</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("**GESTIÓN**")
        if st.button("👥  Usuarios", use_container_width=True,
                     type="primary" if pagina == "usuarios" else "secondary"):
            st.session_state.pagina = "usuarios"
            st.rerun()
        if st.button("📂  Carga de datos", use_container_width=True,
                     type="primary" if pagina == "carga" else "secondary"):
            st.session_state.pagina = "carga"
            st.rerun()
        if st.button("📋  Registro de accesos", use_container_width=True,
                     type="primary" if pagina == "accesos" else "secondary"):
            st.session_state.pagina = "accesos"
            st.rerun()
        st.markdown("**SISTEMA**")
        if st.button("⚙️  Configuración", use_container_width=True,
                     type="primary" if pagina == "config" else "secondary"):
            st.session_state.pagina = "config"
            st.rerun()
        st.markdown("---")
        if st.button("🚪  Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.rerun()


def sidebar_asociado():
    nombre = st.session_state.usuario["nombre"]
    ini = iniciales(nombre)
    pagina = st.session_state.get("pagina", "resumen")

    with st.sidebar:
        st.markdown(f"### 🏦 {NOMBRE_CORTO}")
        st.caption(NOMBRE_FONDO)
        st.markdown("---")
        st.markdown(f"**{ini} {nombre}**")
        st.caption("Asociado")
        st.markdown("---")
        st.markdown("**MI CUENTA**")
        if st.button("📊  Resumen", use_container_width=True,
                     type="primary" if pagina == "resumen" else "secondary"):
            st.session_state.pagina = "resumen"
            st.rerun()
        if st.button("💰  Mis ahorros", use_container_width=True,
                     type="primary" if pagina == "ahorros" else "secondary"):
            st.session_state.pagina = "ahorros"
            st.rerun()
        if st.button("🏦  Mis créditos", use_container_width=True,
                     type="primary" if pagina == "creditos" else "secondary"):
            st.session_state.pagina = "creditos"
            st.rerun()
        st.markdown("**PERFIL**")
        if st.button("🔐  Cambiar clave", use_container_width=True,
                     type="primary" if pagina == "clave" else "secondary"):
            st.session_state.pagina = "clave"
            st.rerun()
        st.markdown("---")
        if st.button("🚪  Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.rerun()


def topbar(titulo, subtitulo, badge=None):
    badge_html = f'<span class="topbar-badge">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">{titulo}</div>
            <div class="topbar-sub">{subtitulo}</div>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def pantalla_login():
    st.markdown("""
    <style>
        .block-container { display: flex; align-items: center; justify-content: center; min-height: 100vh; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown(f"""
        <div style="display:flex;justify-content:center;margin-top:5vh">
        <div class="login-split">
            <div class="login-left">
                <div>
                    <div style="width:44px;height:44px;background:{COLOR_PRIMARIO};border-radius:12px;
                                display:flex;align-items:center;justify-content:center;
                                font-size:24px;margin-bottom:16px">🏦</div>
                    <div style="font-size:20px;font-weight:600;color:white;margin-bottom:6px">{NOMBRE_CORTO}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.45);line-height:1.5;margin-bottom:20px">{NOMBRE_FONDO}</div>
                    <div style="font-size:12px;color:rgba(255,255,255,0.55);line-height:1.6">
                        Consulta tu estado de cuenta, créditos y ahorros en un solo lugar.
                    </div>
                </div>
                <div class="login-footer">
                    {CORREO_SOPORTE}
                </div>
            </div>
            <div class="login-right">
                <div class="login-right-title">Bienvenido 👋</div>
                <div class="login-right-sub">Ingresa con tu correo y contraseña</div>
            </div>
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
                    st.session_state.pagina = "usuarios"
                    registrar_acceso(datos["correo"], datos["nombre"], "admin")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
            else:
                ok, datos, cambiar = login_asociado(correo, clave)
                if ok:
                    st.session_state.usuario = datos
                    st.session_state.perfil = "asociado"
                    st.session_state.pagina = "resumen"
                    st.session_state.cambiar_clave = cambiar
                    registrar_acceso(datos["correo"], datos["nombre"], "asociado")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")

        st.markdown(f'<div style="text-align:center;color:#9CA3AF;font-size:11px;margin-top:1rem">{NOMBRE_FONDO} · {CORREO_SOPORTE}</div>', unsafe_allow_html=True)


def pantalla_cambiar_clave():
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:white;border-radius:16px;border:0.5px solid #E5E7EB;
                    padding:2.5rem 2rem;box-shadow:0 4px 20px rgba(0,0,0,0.06)">
            <div style="font-size:22px;font-weight:600;color:#1A1A2E;margin-bottom:6px">🔐 Nueva contraseña</div>
            <div style="font-size:13px;color:#6B7280;margin-bottom:1.4rem;
                        padding-bottom:1.2rem;border-bottom:1px solid #F3F4F6">
                Es tu primer ingreso. Crea una contraseña segura para proteger tu cuenta.
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
                st.success("¡Contraseña actualizada correctamente!")
                st.rerun()


# ── Enrutador ────────────────────────────────────────────────
if st.session_state.usuario is None:
    pantalla_login()

elif st.session_state.perfil == "asociado" and st.session_state.get("cambiar_clave"):
    pantalla_cambiar_clave()

elif st.session_state.perfil == "admin":
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background: #1A1A2E !important;
            min-width: 240px !important;
        }
        section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }
        section[data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            border: none !important;
            color: rgba(255,255,255,0.75) !important;
            text-align: left !important;
            font-weight: 400 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 0.8rem !important;
            border-radius: 8px !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,0.08) !important;
            color: white !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: {COLOR_PRIMARIO} !important;
            color: white !important;
            font-weight: 600 !important;
        }
    </style>
    """.replace("{COLOR_PRIMARIO}", COLOR_PRIMARIO), unsafe_allow_html=True)
    sidebar_admin()
    from modules.admin import (seccion_usuarios, seccion_carga_datos,
                                seccion_accesos, seccion_configuracion)
    pagina = st.session_state.get("pagina", "usuarios")
    titulos = {
        "usuarios": ("Gestión de Usuarios", "Administra los asociados del fondo"),
        "carga":    ("Carga de Datos", "Actualiza los saldos mensuales"),
        "accesos":  ("Registro de Accesos", "Historial de ingresos al portal"),
        "config":   ("Configuración", "Ajustes del administrador"),
    }
    titulo, subtitulo = titulos.get(pagina, ("Panel", ""))
    topbar(titulo, subtitulo)
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    if pagina == "usuarios":
        seccion_usuarios()
    elif pagina == "carga":
        seccion_carga_datos()
    elif pagina == "accesos":
        seccion_accesos()
    elif pagina == "config":
        seccion_configuracion()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.perfil == "asociado":
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background: #1A1A2E !important;
            min-width: 240px !important;
        }
        section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }
        section[data-testid="stSidebar"] .stButton > button {
            background: transparent !important;
            border: none !important;
            color: rgba(255,255,255,0.75) !important;
            text-align: left !important;
            font-weight: 400 !important;
            font-size: 0.88rem !important;
            padding: 0.45rem 0.8rem !important;
            border-radius: 8px !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,255,255,0.08) !important;
            color: white !important;
        }
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: #C8102E !important;
            color: white !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    sidebar_asociado()
    from modules.asociado import dashboard_asociado
    nombre = st.session_state.usuario["nombre"].split()[0]
    pagina = st.session_state.get("pagina", "resumen")
    titulos = {
        "resumen":  (f"Bienvenido, {nombre} 👋", "Aquí está el resumen de tu cuenta"),
        "ahorros":  ("Mis Ahorros", "Detalle de tus aportes y saldo"),
        "creditos": ("Mis Créditos", "Estado de tus créditos activos"),
        "clave":    ("Cambiar Contraseña", "Actualiza tu contraseña de acceso"),
    }
    titulo, subtitulo = titulos.get(pagina, ("Mi cuenta", ""))
    topbar(titulo, subtitulo)
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    dashboard_asociado(pagina)
    st.markdown('</div>', unsafe_allow_html=True)