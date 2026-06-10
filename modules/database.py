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
        return pd.DataFrame(datos)
    except Exception as e:
        st.error(f"Error leyendo {nombre_hoja}: {e}")
        return pd.DataFrame()

def escribir_hoja(nombre_hoja, df):
    try:
        sheet = conectar_sheets()
        hoja = sheet.worksheet(nombre_hoja)
        hoja.clear()
        hoja.update(
            [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
        )
        return True
    except Exception as e:
        st.error(f"Error escribiendo {nombre_hoja}: {e}")
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