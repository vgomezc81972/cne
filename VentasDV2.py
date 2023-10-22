#  original web

#%%writefile ventasDV2.py

# cargar librerias

import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import types  # Importa types en lugar de builtins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import numpy as np

# cargar datos,  trasnformacion datos , limpieza de datos

# Define una función de hash personalizada para tu función
def my_hash_func(func):
    return id(func)

@st.cache_resource(hash_funcs={types.FunctionType: my_hash_func})

def load_data(url):
    # Cargamos los datos desde el archivo Excel
    return pd.read_excel(url)

# Puedes ajustar la URL del archivo a tu ubicación
url = "https://github.com/Vitotoju/Compensar/raw/main/Ventas_Videojuegos.xlsx"
dataset = load_data(url)

# crear la lista headers
headers = ["Nombre","Plataforma","Año","Genero","Editorial","Ventas_NA","Ventas_EU","Ventas_JP","Ventas_Otros","Ventas_Global"]
dataset.columns = headers

df = dataset[['Plataforma','Año','Genero','Editorial','Ventas_NA','Ventas_EU','Ventas_JP','Ventas_Otros','Ventas_Global']].copy()

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

# Crear gráficas de barras
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(7, 5))

with st.container():
  st.subheader("Bienvenidos a mi sitio web ddd :wave:")
  st.title("Ventas de Video Juegos")
  st.write(" Esta es una pagina para mostrar los resultados")
  st.write("[Mas informacion >>>](https://github.com/Vitotoju)")

with st.container():
  st.write("---")
  left_column, right_column = st.columns(2)
left_column, right_column = st.columns(2)

with left_column:
    st.header("Mi objetivo")
    
    st.write("Esta iamgen muestra Total  ventas x genero")
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))
    total_por_grupo =df.groupby(['Genero'])['Ventas_NA'].sum().reset_index()
    total_por_grupo = total_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})

    ax = sns.barplot(data=total_por_grupo, x='Genero', y='Total_Grupo', palette='viridis')
    ax.set_title('Distribución de Ventas por Género')
    ax.set_xlabel('Género')
    ax.set_ylabel('Ventas_NA')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', weight='bold')
    st.pyplot(plt)

with right_column:
    st.header("Mi objetivo")
    
    st.write("Esta iamgen muestra Total  Ventas x Año")
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))
    total_por_grupo =df.groupby(['Año'])['Ventas_NA'].sum().reset_index()
    total_por_grupo = total_por_grupo.rename(columns={'Ventas_NA': 'Total_Grupo'})

    ax = sns.barplot(data=total_por_grupo, x='Año', y='Total_Grupo', palette='viridis')
    ax.set_title('Distribución de Ventas por Año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ventas_NA')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=8)
    ax.tick_params(axis='x', labelsize=8)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=6, color='black', weight='bold')

    st.pyplot(plt)


