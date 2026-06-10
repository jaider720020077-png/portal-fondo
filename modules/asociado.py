import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import leer_hoja
from config import *

def dashboard_asociado():
    usuario = st.session_state.usuario
    cedula = str(usuario["cedula"])
    nombre = usuario["nombre"]

    st.markdown(f"### 👤 Bienvenido, {nombre}")
    st.divider()

    # Cargar datos de saldos
    df = leer_hoja("saldos")

    if df.empty:
        st.info("Aún no hay datos financieros disponibles. Consulta con el administrador.")
        return

    # Filtrar por cédula del asociado
    if "cedula" not in df.columns:
        st.error("El archivo de saldos no tiene la columna 'cedula'.")
        return

    df["cedula"] = df["cedula"].astype(str)
    datos = df[df["cedula"] == cedula]

    if datos.empty:
        st.info("No se encontraron datos para tu cédula. Consulta con el administrador.")
        return

    # Mostrar tarjetas con los datos más recientes
    ultimo = datos.iloc[-1]
    mostrar_tarjetas(ultimo)
    st.divider()
    mostrar_graficas(datos)


def mostrar_tarjetas(fila):
    st.markdown("#### 📊 Resumen actual")

    cols = st.columns(3)

    # Detectar columnas disponibles automáticamente
    columnas = fila.index.tolist()

    # Tarjeta 1 — Saldo total
    saldo_col = next((c for c in columnas if "saldo" in c.lower()), None)
    with cols[0]:
        if saldo_col:
            try:
                valor = float(str(fila[saldo_col]).replace(",", "").replace("$", ""))
                st.metric(
                    label="💰 Saldo Total",
                    value=f"${valor:,.0f}"
                )
            except Exception:
                st.metric(label="💰 Saldo Total", value=str(fila[saldo_col]))
        else:
            st.metric(label="💰 Saldo Total", value="N/A")

    # Tarjeta 2 — Créditos
    credito_col = next((c for c in columnas if "credito" in c.lower() or "crédito" in c.lower()), None)
    with cols[1]:
        if credito_col:
            try:
                valor = float(str(fila[credito_col]).replace(",", "").replace("$", ""))
                st.metric(
                    label="🏦 Créditos",
                    value=f"${valor:,.0f}"
                )
            except Exception:
                st.metric(label="🏦 Créditos", value=str(fila[credito_col]))
        else:
            st.metric(label="🏦 Créditos", value="N/A")

    # Tarjeta 3 — Cuotas
    cuota_col = next((c for c in columnas if "cuota" in c.lower()), None)
    with cols[2]:
        if cuota_col:
            try:
                valor = float(str(fila[cuota_col]).replace(",", "").replace("$", ""))
                st.metric(
                    label="📅 Cuota Mensual",
                    value=f"${valor:,.0f}"
                )
            except Exception:
                st.metric(label="📅 Cuota Mensual", value=str(fila[cuota_col]))
        else:
            st.metric(label="📅 Cuota Mensual", value="N/A")


def mostrar_graficas(datos):
    st.markdown("#### 📈 Comportamiento histórico")

    columnas = datos.columns.tolist()

    # Detectar columna de fecha o periodo
    fecha_col = next((c for c in columnas if any(p in c.lower() for p in ["fecha", "mes", "periodo", "period"])), None)

    if fecha_col is None:
        st.info("No se encontró columna de fecha o período para graficar el historial.")
        return

    # Gráfica de saldo
    saldo_col = next((c for c in columnas if "saldo" in c.lower()), None)
    if saldo_col:
        try:
            datos_graf = datos[[fecha_col, saldo_col]].copy()
            datos_graf[saldo_col] = pd.to_numeric(
                datos_graf[saldo_col].astype(str).str.replace(",", "").str.replace("$", ""),
                errors="coerce"
            )
            fig = px.line(
                datos_graf,
                x=fecha_col,
                y=saldo_col,
                title="Evolución del Saldo",
                labels={saldo_col: "Saldo ($)", fecha_col: "Período"},
                color_discrete_sequence=[COLOR_SECUNDARIO]
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo graficar el saldo: {e}")

    # Gráfica de créditos
    credito_col = next((c for c in columnas if "credito" in c.lower() or "crédito" in c.lower()), None)
    if credito_col:
        try:
            datos_graf = datos[[fecha_col, credito_col]].copy()
            datos_graf[credito_col] = pd.to_numeric(
                datos_graf[credito_col].astype(str).str.replace(",", "").str.replace("$", ""),
                errors="coerce"
            )
            fig = px.bar(
                datos_graf,
                x=fecha_col,
                y=credito_col,
                title="Créditos por Período",
                labels={credito_col: "Crédito ($)", fecha_col: "Período"},
                color_discrete_sequence=[COLOR_ACENTO]
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo graficar créditos: {e}")