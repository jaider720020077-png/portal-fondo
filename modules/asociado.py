import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import leer_hoja
from modules.auth import cambiar_clave
from config import *


def dashboard_asociado(pagina="resumen"):
    if pagina == "resumen":
        pagina_resumen()
    elif pagina == "ahorros":
        pagina_ahorros()
    elif pagina == "creditos":
        pagina_creditos()
    elif pagina == "clave":
        pagina_cambiar_clave()


def cargar_datos_asociado():
    usuario = st.session_state.usuario
    cedula = str(usuario["cedula"])
    df = leer_hoja("saldos")
    if df.empty:
        return None
    df["cedula"] = df["cedula"].astype(str)
    datos = df[df["cedula"] == cedula]
    return datos if not datos.empty else None


def pagina_resumen():
    datos = cargar_datos_asociado()

    if datos is None:
        st.markdown("""
        <div style="background:white;border-radius:12px;border:0.5px solid #EBEBEB;
                    padding:2rem;text-align:center;margin-top:1rem">
            <div style="font-size:2rem;margin-bottom:10px">📭</div>
            <div style="font-size:15px;font-weight:500;color:#1A1A2E;margin-bottom:6px">
                Aún no hay datos disponibles
            </div>
            <div style="font-size:13px;color:#9CA3AF">
                El administrador aún no ha cargado tu información financiera.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    ultimo = datos.iloc[-1]
    columnas = ultimo.index.tolist()

    # Tarjetas métricas
    saldo_col   = next((c for c in columnas if "saldo" in c.lower()), None)
    credito_col = next((c for c in columnas if "credito" in c.lower() or "crédito" in c.lower()), None)
    cuota_col   = next((c for c in columnas if "cuota" in c.lower()), None)

    col1, col2, col3 = st.columns(3)
    with col1:
        if saldo_col:
            try:
                val = float(str(ultimo[saldo_col]).replace(",","").replace("$","").replace(".","").replace(",","."))
                st.metric("💰 Saldo Total", f"${val:,.0f}")
            except:
                st.metric("💰 Saldo Total", str(ultimo[saldo_col]))
        else:
            st.metric("💰 Saldo Total", "N/A")

    with col2:
        if credito_col:
            try:
                val = float(str(ultimo[credito_col]).replace(",","").replace("$","").replace(".","").replace(",","."))
                st.metric("🏦 Créditos Activos", f"${val:,.0f}")
            except:
                st.metric("🏦 Créditos Activos", str(ultimo[credito_col]))
        else:
            st.metric("🏦 Créditos Activos", "N/A")

    with col3:
        if cuota_col:
            try:
                val = float(str(ultimo[cuota_col]).replace(",","").replace("$","").replace(".","").replace(",","."))
                st.metric("📅 Cuota Mensual", f"${val:,.0f}")
            except:
                st.metric("📅 Cuota Mensual", str(ultimo[cuota_col]))
        else:
            st.metric("📅 Cuota Mensual", "N/A")

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfica
    fecha_col = next((c for c in columnas if any(p in c.lower() for p in ["fecha","mes","periodo","period"])), None)
    if fecha_col and saldo_col:
        try:
            graf = datos[[fecha_col, saldo_col]].copy()
            graf[saldo_col] = pd.to_numeric(
                graf[saldo_col].astype(str).str.replace(",","").str.replace("$",""),
                errors="coerce"
            )
            fig = px.area(
                graf, x=fecha_col, y=saldo_col,
                title="Evolución del Saldo",
                labels={saldo_col: "Saldo ($)", fecha_col: "Período"},
                color_discrete_sequence=[COLOR_PRIMARIO]
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font_color="#1A1A2E",
                title_font_size=14,
                margin=dict(t=40, b=20, l=20, r=20)
            )
            fig.update_traces(fillcolor=f"rgba(200,16,46,0.1)")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo graficar: {e}")


def pagina_ahorros():
    datos = cargar_datos_asociado()
    if datos is None:
        st.info("No hay datos de ahorros disponibles.")
        return
    st.markdown("#### Detalle de tus aportes")
    st.dataframe(datos, use_container_width=True)


def pagina_creditos():
    datos = cargar_datos_asociado()
    if datos is None:
        st.info("No hay datos de créditos disponibles.")
        return
    columnas = datos.columns.tolist()
    credito_cols = [c for c in columnas if "credito" in c.lower() or "crédito" in c.lower() or "cuota" in c.lower()]
    if credito_cols:
        st.markdown("#### Estado de tus créditos")
        st.dataframe(datos[credito_cols], use_container_width=True)
    else:
        st.info("No se encontraron columnas de créditos en tus datos.")


def pagina_cambiar_clave():
    st.markdown("""
    <div style="background:white;border-radius:12px;border:0.5px solid #EBEBEB;
                padding:1.5rem;max-width:480px;margin-bottom:1rem">
        <div style="font-size:15px;font-weight:600;color:#1A1A2E;margin-bottom:4px">
            🔐 Cambiar contraseña
        </div>
        <div style="font-size:13px;color:#9CA3AF">
            Usa una contraseña segura de al menos 8 caracteres.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_clave_asociado"):
        actual    = st.text_input("Contraseña actual", type="password")
        nueva     = st.text_input("Nueva contraseña", type="password")
        confirmar = st.text_input("Confirmar nueva contraseña", type="password")
        guardar   = st.form_submit_button("Actualizar contraseña", use_container_width=True)

    if guardar:
        from modules.auth import login_asociado
        ok, _, _ = login_asociado(st.session_state.usuario["correo"], actual)
        if not ok:
            st.error("La contraseña actual es incorrecta.")
        elif len(nueva) < LONGITUD_MINIMA_CLAVE:
            st.error(f"Mínimo {LONGITUD_MINIMA_CLAVE} caracteres.")
        elif nueva != confirmar:
            st.error("Las contraseñas no coinciden.")
        else:
            cambiar_clave(st.session_state.usuario["correo"], nueva)
            st.success("✅ Contraseña actualizada correctamente.")