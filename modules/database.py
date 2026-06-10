import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def conectar_sheets():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    cliente = gspread.authorize(creds)
    sheet = cliente.open_by_key(st.secrets["sheets"]["sheet_id"])
    return sheet

def leer_hoja(nombre_hoja):
    try:
        sheet = conectar_sheets()
        hoja = sheet.worksheet(nombre_hoja)
        datos = hoja.get_all_records()
        df = pd.DataFrame(datos)
        return df.astype(str) if not df.empty else df
    except Exception as e:
        st.error(f"Error leyendo {nombre_hoja}: {e}")
        return pd.DataFrame()

def escribir_hoja(nombre_hoja, df):
    try:
        sheet = conectar_sheets()
        hoja = sheet.worksheet(nombre_hoja)
        hoja.clear()
        df2 = df.astype(str)
        hoja.update(
            [df2.columns.tolist()] + df2.values.tolist()
        )
        return True
    except Exception as e:
        st.error(f"Error escribiendo {nombre_hoja}: {e}")
        return False

def actualizar_celda(nombre_hoja, columna_busqueda, valor_busqueda, columna_actualizar, valor_nuevo):
    """Actualiza una celda específica directamente en Google Sheets sin usar pandas"""
    try:
        sheet = conectar_sheets()
        hoja = sheet.worksheet(nombre_hoja)
        encabezados = hoja.row_values(1)

        col_busq = encabezados.index(columna_busqueda) + 1
        col_act = encabezados.index(columna_actualizar) + 1

        celdas = hoja.col_values(col_busq)
        for i, val in enumerate(celdas[1:], start=2):
            if str(val) == str(valor_busqueda):
                hoja.update_cell(i, col_act, str(valor_nuevo))
                return True
        return False
    except Exception as e:
        st.error(f"Error actualizando celda: {e}")
        return False

def agregar_fila(nombre_hoja, fila_dict):
    try:
        sheet = conectar_sheets()
        hoja = sheet.worksheet(nombre_hoja)
        encabezados = hoja.row_values(1)
        fila = [str(fila_dict.get(col, "")) for col in encabezados]
        hoja.append_row(fila)
        return True
    except Exception as e:
        st.error(f"Error agregando fila en {nombre_hoja}: {e}")
        return False