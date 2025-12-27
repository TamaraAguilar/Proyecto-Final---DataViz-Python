"""
Proyecto Final - DataViz Python
Lab: Construyendo Interfaces de Datos Interactivas
Dataset: Estudio de indicadores de gobierno digital 2023
Fuente: datos.gob.cl
Autor: Tamara aguilar
Fecha: Diciembre 2025
"""

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

# ---------------------------------------------------------------------------- #
#                             INFORMACION PRINCIPAL                            #
# ---------------------------------------------------------------------------- #
# Configuración de la página
st.set_page_config(
    page_title="Estudio de indicadores de gobierno digital 2023",
    page_icon="🖥️",
    layout="wide"
)


# Título principal
st.title("🖥️ Estudio de indicadores de gobierno digital 2023: Área de informática y/o tecnología")

st.write(
    """
    El presente informe rescata las preguntas relevantes sobre la demografía y composición del Área de Tecnologías de la Información.
    En particular, sobre el género y la formación profesional de los profesionales de las TICS. Si bien el dataset contiene
    otras preguntas pertinentes con respecto al nivel de digitalización de cada institución gubernamental, el foco de interés de este
    proyecto es la :violet[brecha] :violet[de] :violet[género] y el :violet[nivel] :violet[de] :violet[escolaridad] de los trabajadores en tecnología.
    """)

# ---------------------------------------------------------------------------- #
#                                 PETICION HTTP                                #
# ---------------------------------------------------------------------------- #

@st.cache_data # Decorador para almacenar funciones que devuelven datos en caché
def obtener_datos(limit=5000):
    """
    Obtiene datos desde API de datos.gob.cl utilizando método GET

    Args:
        limit (int, optional): Obtiene 5000 registros por default.
    """
    url = "https://datos.gob.cl/api/action/datastore_search"
    resource_id = "e53563d6-26cb-45f4-a4f9-c33d1de2f92e" # ID asociado al dataset

    params = {
        "resource_id": resource_id,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        # Verificar estado de la respuesta
        if response.status_code == 200:
            data = response.json()
            records = data["result"]["records"]

            # Convertir a dataframe
            return pd.DataFrame(records), None
        else:
            return None, f"Error en la petición HTTP: {response.status_code}"

    except Exception as e:
        return None, f"Error: {str(e)}"


# ---------------------------------------------------------------------------- #
#                              INTERFAZ STREAMLIT                              #
# ---------------------------------------------------------------------------- #

# ---------------------------------- Sidebar --------------------------------- #
with st.sidebar:
    # Título
    st.header("Información del proyecto")
    st.info("""
    **Fuente de Datos:**
    Portal de Datos Abiertos del Gobierno de Chile
    
    **Dataset:**
    Estudio de indicadores de gobierno digital 2023

    """)

    st.markdown("---")
    st.markdown("[Enlace Dataset](https://datos.gob.cl/dataset/estudio-de-indicadores-2023)")

# ---------------------------------- Loader ---------------------------------- #
with st.spinner("Cargando datos..."):
    try:
        df, error = obtener_datos()

        if df is None or df.empty: # Si no vienen datos
            st.warning("No se pudieron cargar los datos")
            st.stop()
    except Exception as e:
        st.error(f"Error: {e}")
    

# ---------------------------------------------------------------------------- #
#                                 PROCESAR DATA                                #
# ---------------------------------------------------------------------------- #
# ----------------------------- Seleccionar datos ---------------------------- #
columnas_relevantes = [
    "Tipo", "P2.6a.1", "P2.6a.2", "P2.7.1", "P2.7.2", "P2.7.3", "P2.7.4", 
    "P2.7.5", "P2.7.6", "P2.7.7"
]

df = df[columnas_relevantes].copy()

# Convertir columnas numéricas
for col in columnas_relevantes:
    if col != "Tipo":
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Renombrar columnas
nombres_columnas = {
    "Tipo": "Tipo Institución",
    "P2.6a.1": "Mujeres",
    "P2.6a.2": "Hombres",
    "P2.7.1": "Técnico TIC",
    "P2.7.2": "Técnico Otras Áreas",
    "P2.7.3": "Profesional TIC (s/lic)",
    "P2.7.4": "Profesional Otras (s/lic)",
    "P2.7.5": "Universitario Ciencia/Tec",
    "P2.7.6": "Universitario Otras Áreas",
    "P2.7.7": "Otros"
}

# Renombrar las columnas
df = df.rename(columns=nombres_columnas)

# ----------------------------- Mostrar datos -------------------------------- #
st.subheader("Vista de los datos")
st.write(f"Total de registros: **{len(df)}**")
st.dataframe(df, use_container_width=True, height=400, hide_index=True)

# ----------------------- Gráfico de barras por género ----------------------- #
st.markdown("---")
st.subheader("Distribución de Género por Tipo de Institución")

st.markdown("""
**Análisis de brechas de género en TIC:**

Con respecto a la composición de género de los equipos del área de informática y/o tecnología,
el siguiente gráfico muestra una predominancia masculina en todos los grupos de análisis.


- **Azul**: Representa el porcentaje de hombres
- **Rosa**: Representa el porcentaje de mujeres

Los datos corresponden al período 2022-2023.
""")

# Agrupar por tipo de institución y sumar mujeres y hombres
df_genero = df.groupby("Tipo Institución")[["Mujeres", "Hombres"]].sum()

# Calcular totales y porcentajes
df_genero["Total"] = df_genero["Mujeres"] + df_genero["Hombres"]
df_genero["% Mujeres"] = (df_genero["Mujeres"] / df_genero["Total"] * 100).round(1)
df_genero["% Hombres"] = (df_genero["Hombres"] / df_genero["Total"] * 100).round(1)

# Crear gráfico
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_alpha(0.0) 

# Utilizar misma fuente de Streamlit
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Source Sans Pro', 'Arial', 'sans-serif']

# Colores de barras
color_mujeres = "#ffb3d9"  
color_hombres = "#b3d9ff"  

# Posiciones de las barras
y_pos = range(len(df_genero))

# Barras horizontales
ax.barh(y_pos, df_genero["% Mujeres"], color=color_mujeres, label="Mujeres", height=0.4)
ax.barh(y_pos, df_genero["% Hombres"], left=df_genero["% Mujeres"], 
        color=color_hombres, label="Hombres", height=0.4)

# Agregar etiquetas de porcentaje
for i, (idx, row) in enumerate(df_genero.iterrows()):
    # Etiqueta de mujeres
    ax.text(row["% Mujeres"]/2, i, f'{row["% Mujeres"]:.1f}%', 
            ha='center', va='center', fontweight='bold', color='black')
    # Etiqueta de hombres
    ax.text(row["% Mujeres"] + row["% Hombres"]/2, i, f'{row["% Hombres"]:.1f}%', 
            ha='center', va='center', fontweight='bold', color='black')

# Configurar ejes y título
ax.set_yticks(y_pos)
ax.set_yticklabels(df_genero.index)
ax.set_xlabel('Porcentaje (%)')
ax.set_title('')
ax.set_xlim(0, 100)
ax.legend()

st.pyplot(fig, transparent=True)
st.caption("Datos del año 2023. Fuente: datos.gob.cl")

st.subheader("Resumen por Tipo de Institución")
st.dataframe(df_genero, use_container_width=True)

# ---------------------------------- Footer ---------------------------------- #
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
<p><strong>Proyecto Final - DataViz Python</strong></p>
<p>Fuente: <a href='https://datos.gob.cl/dataset/estudio-de-indicadores-2023'>datos.gob.cl</a></p>
</div>
""", unsafe_allow_html=True)