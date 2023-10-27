#  original web

#%%writefile ventasDV2.py

# cargar librerias
from typing import List, Tuple

import streamlit as st
import types  # Importa types en lugar de builtins
import pandas as pd
import pip
pip.main(["install", "openpyxl"])
import altair as alt


def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

set_page_config()

# Define una función de hash personalizada para tu función
def my_hash_func(func):
    return id(func)

@st.cache_resource(hash_funcs={types.FunctionType: my_hash_func})

def load_data(url):
    # Cargamos los datos desde el archivo Excel
    return pd.read_excel(url)

url = "https://github.com/Vitotoju/Compensar/raw/main/Ventas_Videojuegos.xlsx"
dataset = load_data(url)

# crear la lista headers
headers = ["Nombre","Plataforma","Año","Genero","Editorial","Ventas_NA","Ventas_EU","Ventas_JP","Ventas_Otros","Ventas_Global"]
dataset.columns = headers
df = dataset

# Cadena Más Común (Moda)  -  para reemplazar los datos vacios con el valor más frecuente o la moda
most_common_string = df['Editorial'].value_counts().idxmax()
df['Editorial'].fillna(most_common_string, inplace=True)

# eliminar la primera fila de cabecera (del excel cargado)
df = df.drop([0], axis=0)

#Actualización del index
df.reset_index(drop=True)

#Convertir el tipo de datos al formato apropiado 
df[["Ventas_NA"]] = df[["Ventas_NA"]].astype("float")
df[["Ventas_EU"]] = df[["Ventas_EU"]].astype("float")
df[["Ventas_JP"]] = df[["Ventas_JP"]].astype("float")
df[["Ventas_Otros"]] = df[["Ventas_Otros"]].astype("float")
df['Año'] = df['Año'].astype('object')
df['Plataforma'] = df['Plataforma'].astype(str)
df['Genero'] = df['Genero'].astype(str)
df['Editorial'] = df['Editorial'].astype(str)

st.sidebar.header("Opciones a filtrar: ")

# Filtros Laterales
filtro_plataformas = st.sidebar.selectbox('Filtrar por Plataforma', ['Todos'] + df['Plataforma'].unique().tolist())
filtro_generos = st.sidebar.selectbox('Filtrar por Género', ['Todos'] + df['Genero'].unique().tolist())
filtro_editoriall = st.sidebar.selectbox('Filtrar por Editorial', ['Todos'] + df['Editorial'].unique().tolist())

st.sidebar.info('Created by Victor - Diana')

# Aplicar filtros a los datos
filtro_anos = df['Año'].unique().tolist()

if filtro_plataformas == 'Todos':
    mask_plataforma = df['Plataforma'].notna()
else:
    mask_plataforma = df['Plataforma'] == filtro_plataformas

if filtro_generos == 'Todos':
    mask_genero = df['Genero'].notna()
else:
    mask_genero = df['Genero'] == filtro_generos

if filtro_editoriall == 'Todos':
    mask_editorial = df['Editorial'].notna()
else:
    mask_editorial = df['Editorial'] == filtro_editoriall

# Crear gráficas de barras

with st.container():
  st.subheader("Bienvenidos a mi sitio web VENTAS :wave:")
  st.title("📊 Ventas de Video Juegos")
  st.write(" Esta es una pagina para mostrar los resultados")

  anual_selector = st.slider('Año de ventas :',
                           min_value = min(filtro_anos),
                           max_value = max(filtro_anos),
                           value = (min(filtro_anos),max(filtro_anos))
                           )

# Aplicar filtros a los datos

  # Combinar las máscaras de filtro
  mask = df['Año'].between(*anual_selector) & mask_plataforma & mask_genero & mask_editorial
  numero_resultados = df[mask].shape[0]
  st.markdown(f'*Resultados Disponibles:{numero_resultados}*')

## KPIs

  @st.cache_data
  def calculate_kpis(df: pd.DataFrame) -> List[float]:
        total_ventas =(df[mask]['Ventas_Global'].sum())
        Vlr_Ventas = f"{total_ventas:.2f}M"
        total_orders = df[mask]['Nombre'].nunique()
        Promedio_ventas = f"{total_ventas / total_orders:.2f}K"
        return [Vlr_Ventas, total_orders, Promedio_ventas, total_orders]
  

  def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
        st.header("KPI Metrics")
        for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(4), zip(kpi_names, kpis))):
            col.metric(label=kpi_name, value=kpi_value)


  kpis = calculate_kpis(df)
  kpi_names = ["Vlr_Ventas", "Cantidad Videojuegos", "Promedio Ventas", "Total Video Juegos"]
  display_kpi_metrics(kpis, kpi_names)


  st.write("---")
  st.subheader("Top 10 Products by Sales")
  st.write(df[mask].head(10))

with st.container():
  st.write("---")
  left_column , right_column = st.columns(2)

  totalg_por_grupo_na = df[mask].groupby(['Genero'])['Ventas_NA'].sum().reset_index()
  totalg_por_grupo_na = totalg_por_grupo_na.rename(columns={'Ventas_NA': 'Total_Grupo'})
  totalg_por_grupo_eu = df[mask].groupby(['Genero'])['Ventas_EU'].sum().reset_index()
  totalg_por_grupo_eu = totalg_por_grupo_eu.rename(columns={'Ventas_EU': 'Total_Grupo'})
  totalg_por_grupo_jp = df[mask].groupby(['Genero'])['Ventas_JP'].sum().reset_index()
  totalg_por_grupo_jp = totalg_por_grupo_jp.rename(columns={'Ventas_JP': 'Total_Grupo'})
  totalg_por_grupo_otros = df[mask].groupby(['Genero'])['Ventas_Otros'].sum().reset_index()
  totalg_por_grupo_otros = totalg_por_grupo_otros.rename(columns={'Ventas_Otros': 'Total_Grupo'})
  totalg_por_grupo = pd.concat([totalg_por_grupo_na, totalg_por_grupo_eu, totalg_por_grupo_jp, totalg_por_grupo_otros],
                               keys=['Ventas NA', 'Ventas EU', 'Ventas JP', 'Ventas Otros'], names=['Tipo']).reset_index()
  
  totalp_por_grupo_na = df[mask].groupby(['Plataforma'])['Ventas_NA'].sum().reset_index()
  totalp_por_grupo_na = totalp_por_grupo_na.rename(columns={'Ventas_NA': 'Total_Grupo'})
  totalp_por_grupo_eu = df[mask].groupby(['Plataforma'])['Ventas_EU'].sum().reset_index()
  totalp_por_grupo_eu = totalp_por_grupo_eu.rename(columns={'Ventas_EU': 'Total_Grupo'})
  totalp_por_grupo_jp = df[mask].groupby(['Plataforma'])['Ventas_JP'].sum().reset_index()
  totalp_por_grupo_jp = totalp_por_grupo_jp.rename(columns={'Ventas_JP': 'Total_Grupo'})
  totalp_por_grupo_otros = df[mask].groupby(['Plataforma'])['Ventas_Otros'].sum().reset_index()
  totalp_por_grupo_otros = totalp_por_grupo_otros.rename(columns={'Ventas_Otros': 'Total_Grupo'})
  totalp_por_grupo = pd.concat([totalp_por_grupo_na, totalp_por_grupo_eu, totalp_por_grupo_jp, totalp_por_grupo_otros],
                               keys=['Ventas NA', 'Ventas EU', 'Ventas JP', 'Ventas Otros'], names=['Tipo']).reset_index()
  
  totale_por_grupo_na = df[mask].groupby(['Editorial'])['Ventas_NA'].sum().reset_index()
  totale_por_grupo_na = totale_por_grupo_na.rename(columns={'Ventas_NA': 'Total_Grupo'})
  totale_por_grupo_eu = df[mask].groupby(['Editorial'])['Ventas_EU'].sum().reset_index()
  totale_por_grupo_eu = totale_por_grupo_eu.rename(columns={'Ventas_EU': 'Total_Grupo'})
  totale_por_grupo_jp = df[mask].groupby(['Editorial'])['Ventas_JP'].sum().reset_index()
  totale_por_grupo_jp = totale_por_grupo_jp.rename(columns={'Ventas_JP': 'Total_Grupo'})
  totale_por_grupo_otros = df[mask].groupby(['Editorial'])['Ventas_Otros'].sum().reset_index()
  totale_por_grupo_otros = totale_por_grupo_otros.rename(columns={'Ventas_Otros': 'Total_Grupo'})
  totale_por_grupo = pd.concat([totale_por_grupo_na, totale_por_grupo_eu, totale_por_grupo_jp, totale_por_grupo_otros],
                               keys=['Ventas NA', 'Ventas EU', 'Ventas JP', 'Ventas Otros'], names=['Tipo']).reset_index()

with st.container():
    st.write("---")
    st.header("Ventas Genero")
    st.write("Esta imagen muestra Total Ventas de todos los tipos")
    bars = alt.Chart(totalg_por_grupo).mark_bar().encode(
        x=alt.X('Genero:N', title="Género"),
        y=alt.Y('Total_Grupo:Q', title="Total de Ventas"),
        xOffset="Tipo:N",
        color=alt.Color('Tipo:N', title="Tipo de Ventas")
    ).properties(width=1000, height=400)

    text = alt.Chart(totalg_por_grupo).mark_text(dx=3, dy=-15, color='black').encode(
        x=alt.X('Genero:N'),
        y=alt.Y('sum(Total_Grupo):Q',).stack('zero'),
        xOffset="Tipo:N",
        detail='Tipo:N',
        text=alt.Text('sum(Total_Grupo):Q', format='.1f')
    )
    chart = (bars + text)
    st.altair_chart(chart)
with st.expander("Análisis"):
    st.write("1. Hay una tendencia siempre que la Region NA supera en ventas\n"
             "2. El genero que mas vendio es : Action\n"
             "3. El genero que menores ventas tuvo fue : Strategy\n"
             "4. La Region que menos ventas tuvo fue Otros")

with st.container():
    st.write("---")
    st.header("Ventas Plataforma")
    st.write("Esta imagen muestra Total Ventas de todos los tipos")
    bars = alt.Chart(totalp_por_grupo).mark_bar().encode(
        x=alt.X('sum(Total_Grupo):Q', title="Total de Ventas").stack('zero'),
        y=alt.Y('Plataforma:N', title="Plataforma"),
        color=alt.Color('Tipo', title="Tipo de Ventas")
    ).properties(width=800, height=800)

    text = alt.Chart(totalp_por_grupo).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('sum(Total_Grupo):Q',).stack('zero'),
        y=alt.Y('Plataforma:N'),
        detail='Tipo:N',
        text=alt.Text('sum(Total_Grupo):Q', format='.1f')
    )
    chart = (bars + text)
    st.altair_chart(chart)

with st.expander("Análisis"):
    st.write("1. Hay una tendencia siempre que la Region NA supera en ventas\n"
             "2. La Plataforma que mas vendio fue : PS2\n"
             "3. Las Plataformas que no tuvieron ventas fueron : 3DO, GG, NG, PCFX, TG16, WS\n"
             "4. Las Plataforma con mas ventas fueron : PS2, X360, PS3, Wii")
  
# Agregar los totales por plataforma
total_por_plataforma = totalp_por_grupo.groupby('Plataforma')['Total_Grupo'].sum().reset_index()

with st.container():
    st.write("---")
    st.header("Ventas Plataforma")
    st.write("Esta imagen muestra Total Ventas de todos los tipos")
    
    # Crear un gráfico de torta con Altair
    pie_chart = alt.Chart(total_por_plataforma).mark_arc().encode(
        color=alt.Color('Plataforma:N', title="Plataforma"),
        theta=alt.Theta('Total_Grupo:Q', title="Total de Ventas"),
        tooltip=['Plataforma:N', alt.Tooltip('Total_Grupo:Q', format='.1f')]
    ).properties(width=400, height=400)

    st.altair_chart(pie_chart)

with st.container():
    st.write("---")
    st.header("Ventas Editorial")
    st.write("Esta imagen muestra Total Ventas de todos los tipos")
    chart = alt.Chart(totale_por_grupo).mark_bar().encode(
        x=alt.X('Editorial:N', title="Editorial"),
        y=alt.Y('Total_Grupo:Q', title="Total de Ventas"),
        color=alt.Color('Tipo:N', title="Tipo de Ventas")
    ).properties(width=1200, height=1000)
    st.altair_chart(chart)

with st.container():
    st.write("---")
    st.header("Ventas x Año")
    df['Año'] = pd.to_datetime(df['Año'], format='%Y')
    totala_por_grupo = df[mask].groupby(['Año'])[['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Ventas_Otros']].sum().reset_index()
    # Reformatear los datos para que estén en formato largo
    totala_por_grupo = totala_por_grupo.melt(id_vars=['Año'], var_name='Tipo', value_name='Total_Grupo')
    chart = alt.Chart(totala_por_grupo).mark_line().encode(
        x=alt.X('Año:T', title="Año"),
        y=alt.Y('Total_Grupo:Q', title="Total de Ventas"),
        color=alt.Color('Tipo:N', title="Tipo de Ventas")
    ).properties(width=800, height=400)
    st.altair_chart(chart)
with st.expander("Análisis"):
    st.write("1. Se evidencia que el año 2008, tuvo mas ventas en todas las regiones\n"
             "2. Se Evidencia que la decada los 80 fueron las ventas mas bajas\n"
             "3. La Region que mas ventas tuvo fue NA\n"
             "4. La Region que menos ventas tuvo fue Otros")

# %%
