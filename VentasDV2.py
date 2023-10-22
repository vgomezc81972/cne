#  original web

#%%writefile ventasDV2.py

# cargar librerias

import streamlit as st
import types  # Importa types en lugar de builtins
import pandas as pd
import pip
pip.main(["install", "openpyxl"])
import plotly.express as px

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
#  st.write(df)

  numero_resultados = df[mask].shape[0]
  st.markdown(f'*Resultados Disponibles:{numero_resultados}*')

with st.container():
  st.write("---")
  left_column, right_column = st.columns(2)

with left_column:
    st.header("Mi objetivo")
    
    st.write("Esta imagen muestra Total Ventas x Género")
    total_por_grupo = df[mask].groupby(['Genero'])['Ventas_NA'].sum().reset_index()
    total_por_grupo = total_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})
    st.bar_chart(total_por_grupo.set_index('Genero'))
with right_column:
    st.header("Mi objetivo")
    
    st.write("Esta imagen muestra Total Ventas x Año")
    total_por_grupo = df[mask].groupby(['Año'])['Ventas_NA'].sum().reset_index()
    total_por_grupo = total_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})
    st.bar_chart(total_por_grupo.set_index('Año'))

with st.container():
  st.write("---")
  left_column, right_column = st.columns(2)

  with left_column:
    st.header("Mi objetivo")
    
    st.write("Esta imagen muestra Total Ventas x Género")
    total_por_grupo = df[mask].groupby(['Genero'])['Ventas_NA'].sum().reset_index()
    total_por_grupo = total_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})
    st.bar_chart(total_por_grupo.set_index('Genero'))
    #st.bar_chart.update_traces(texttemplate='%{text}', textposition='outside')

with right_column:
    st.header("Mi objetivo")
    
    st.write("Esta imagen muestra Total Ventas x Año")
    pla_por_grupo = df[mask].groupby(['Plataforma'])['Ventas_NA'].sum().reset_index()
    pla_por_grupo = pla_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})
    pla_por_grupo = pla_por_grupo.reset_index()
    
    #bar_chart = px.bar(pla_por_grupo, x='Plataforma', y='Total_Grupo', title='Total de Ventas por Plataforma')
    bar_chart = px.bar(pla_por_grupo, x='Plataforma', y='Total_Grupo', color_discrete_sequence = ['#f5b632']*len(pla_por_grupo), title='Total de Ventas por Plataforma')
    #bar_chart.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(bar_chart)
