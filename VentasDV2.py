#  original web

#%%writefile ventasDV2.py

# cargar librerias

import streamlit as st
import types  # Importa types en lugar de builtins
import pandas as pd
import pip
pip.main(["install", "openpyxl"])
import altair as alt


# cargar datos,  trasnformacion datos , limpieza de datos

# Define una función de hash personalizada para tu función
def my_hash_func(func):
    return id(func)

@st.cache_resource(hash_funcs={types.FunctionType: my_hash_func})

def load_data(url):
    # Cargamos los datos desde el archivo Excel
    return pd.read_excel(url)

# Puedes ajustar la URL del archivo a tu ubicación
#dataset = pd.read_excel('Ventas_Videojuegos.xlsx')
url = "https://github.com/Vitotoju/Compensar/raw/main/Ventas_Videojuegos.xlsx"
dataset = load_data(url)
#st.write(dataset)

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

# Filtros interactivos
#filtro_ano = st.sidebar.selectbox('Filtrar por Año', df['Año'].unique())
filtro_anos = df['Año'].unique().tolist()
filtro_plataforma = df['Plataforma'].unique().tolist()
filtro_genero = df['Genero'].unique().tolist()
filtro_editorial = st.sidebar.selectbox('Filtrar por Editorial', df['Editorial'].unique())


# Crear gráficas de barras

with st.container():
  st.subheader("Bienvenidos a mi sitio web ddd :wave:")
  st.title("Ventas de Video Juegos")
  st.write(" Esta es una pagina para mostrar los resultados")
  anual_selector = st.slider('Año de ventas :',
                           min_value = min(filtro_anos),
                           max_value = max(filtro_anos),
                           value = (min(filtro_anos),max(filtro_anos))
                           )

  plataforma_selector = st.multiselect('Plataforma :',
                            filtro_plataforma,
                            default = filtro_plataforma
                            )

  genero_selector = st.multiselect('Genero :',
                            filtro_genero,
                            default = filtro_genero
                            )

  mask = (df['Año'].between(*anual_selector)&(df['Plataforma'].isin(plataforma_selector))&(df['Genero'].isin(genero_selector)))
  st.write(df)

  numero_resultados = df[mask].shape[0]
  st.markdown(f'*Resultados Disponibles:{numero_resultados}*')

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
    chart = alt.Chart(totalg_por_grupo).mark_bar().encode(
        x=alt.X('Genero:N', title="Género"),
        y=alt.Y('Total_Grupo:Q', title="Total de Ventas"),
        color=alt.Color('Tipo:N', title="Tipo de Ventas")
    ).properties(width=800, height=400)
    st.altair_chart(chart)

with st.container():
    st.write("---")
    st.header("Ventas Plataforma")
    st.write("Esta imagen muestra Total Ventas de todos los tipos")
    chart = alt.Chart(totalp_por_grupo).mark_bar().encode(
        x=alt.X('Plataforma:N', title="Plataforma"),
        y=alt.Y('Total_Grupo:Q', title="Total de Ventas"),
        color=alt.Color('Tipo:N', title="Tipo de Ventas")
    ).properties(width=800, height=400)
    st.altair_chart(chart)

with st.container():
    st.write("---")
    st.header("Ventas Editorial")
    st.write("Esta imagen muestra Total Ventas de todos los tipos")
    chart = alt.Chart(totale_por_grupo).mark_bar().encode(
        x=alt.X('Editorial:N', title="Editorial"),
        y=alt.Y('Total_Grupo:Q', title="Total de Ventas"),
        color=alt.Color('Tipo:N', title="Tipo de Ventas")
    ).properties(width=800, height=400)
    st.altair_chart(chart)

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)

with left_column:
    st.write("---") 
    st.header("Ventas Genero")   
    st.write("Esta imagen muestra Total Ventas x Año")
    tortag_por_grupo = df[mask].groupby(['Genero'])['Ventas_NA'].sum().reset_index()
    tortag_por_grupo = tortag_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})
    tortag_por_grupo = tortag_por_grupo.reset_index()

    # Especifica explícitamente el tipo de datos para Total_Grupo
    tortag_por_grupo['Total_Grupo'] = tortag_por_grupo['Total_Grupo'].astype(float)

    c = alt.Chart(tortag_por_grupo).mark_arc().encode(theta="Total_Grupo:Q", color="Genero:N")
    st.altair_chart(c)

with right_column:
    st.write("---")
    st.header("Ventas Plataforma")
    st.write("Esta imagen muestra Total Ventas x Año")
    tortap_por_grupo = df[mask].groupby(['Plataforma'])['Ventas_NA'].sum().reset_index()
    tortap_por_grupo = tortap_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})
    tortap_por_grupo = tortap_por_grupo.reset_index()

    # Especifica explícitamente el tipo de datos para Total_Grupo
    tortap_por_grupo['Total_Grupo'] = tortap_por_grupo['Total_Grupo'].astype(float)

    c = alt.Chart(tortap_por_grupo).mark_arc().encode(theta="Total_Grupo:Q", color="Plataforma:N")
    st.altair_chart(c)
