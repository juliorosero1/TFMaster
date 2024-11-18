import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import json
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium
import matplotlib.pyplot as plt
import numpy as np




# Activar el layout amplio
st.set_page_config(layout="wide")

# Cargar stopwords desde un archivo de texto
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()
    return stopwords

# Cargar las stopwords desde un archivo
stop_words_spanish = load_stopwords('stop_words_spanish.txt')
custom_stopwords = set([word.lower() for word in stop_words_spanish + ['https', 'co', 'rt', 't', 'c']])

# Función para eliminar stopwords manualmente
def remove_stopwords(text):
    tokens = text.lower().split()
    cleaned_tokens = [word for word in tokens if word not in custom_stopwords]
    return ' '.join(cleaned_tokens)

# Cargar los datos
df = pd.read_csv("sentimientosTweet_3.csv")

# Convertir la columna 'fecha' al tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d %H:%M:%S')

# Establecer 'fecha' como el índice del DataFrame
df.set_index('fecha', inplace=True)

# Preprocesar los tweets
df['cleaned_tweet'] = df['tweet'].apply(remove_stopwords)

# Convertir la columna de emociones a listas
df['emocion'] = df['emocion'].apply(lambda x: x.strip("[]").replace("'", "").split(", "))

# Ajustar nombres de países en los datos para que coincidan con el GeoJSON
df['pais'] = df['pais'].replace(
    ['EEUU', 'España', 'Republica Dominicana'],
    ['United States', 'Spain', 'Dominican Rep.']
)

# Sidebar para seleccionar la vista
st.sidebar.title("Seleccione la Vista")
view = st.sidebar.selectbox("Elige una vista", ["Vista Global", "Vista Comparativa entre Países"])




# Vista Global
if view == "Vista Global":
    st.title("Análisis Global de Emociones y Países")

    # Control para ajustar las dimensiones del mapa
    st.sidebar.title("Mapa de calor (dimensiones)")
    map_width = st.sidebar.slider("Ancho del Mapa (px)", min_value=500, max_value=1000, value=600)
    map_height = st.sidebar.slider("Alto del Mapa (px)", min_value=400, max_value=600, value=500)

    # Control de visualización (nube de palabras o gráfico de barras) en la barra lateral
    st.sidebar.title("Palabras Frecuentes")
    visualizacion_seleccionada = st.sidebar.radio("Seleccione la visualización:", ("Nube de Palabras", "Gráfico de Barras"))


    st.header("Mapa de Calor por Emoción y Palabras Frecuentes")
    emocion_seleccionada = st.selectbox("Seleccione una Emoción", ['miedo', 'ira', 'expectante', 'confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria'])

    if map_width > 730:
        # Si el mapa es más grande, se muestran el mapa y la nube de palabras en filas diferentes

        porcen = df.groupby('pais').sum()[['miedo', 'ira', 'expectante', 'confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria']]
        porcen = porcen.assign(suma=porcen.sum(axis=1))
        porcen = porcen.apply(lambda x: (x / porcen['suma']) * 100, axis=0)
        porcen = porcen.reset_index()

        # Cargar archivo geojson para el mapa
        data_geo = json.load(open('hispano.geojson'))

        # Crear el mapa
        world_map = folium.Map(location=[17.57, -59.74], zoom_start=2.4, tiles='cartodbpositron')

        # Crear Choropleth
        choropleth = folium.Choropleth(
            geo_data=data_geo,
            data=porcen,
            columns=['pais', emocion_seleccionada],
            key_on='feature.properties.name',
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.4,
            legend_name=f"Porcentaje de {emocion_seleccionada.capitalize()} por País"
        ).add_to(world_map)

        choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['name'], labels=False))

        # Mostrar el mapa con ajuste automático
        folium_static(world_map, width=map_width, height=map_height)


        if visualizacion_seleccionada == "Nube de Palabras":
            # Nube de Palabras en la siguiente fila
            filtered_tweets = df[df['emocion'].apply(lambda x: emocion_seleccionada in x)]
            wordcloud_text = ' '.join(filtered_tweets['cleaned_tweet'])
            wordcloud = WordCloud(background_color='white', width=1200, height=250).generate(wordcloud_text)
            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot(plt, use_container_width=True)
        else:
            # Mostrar las palabras más frecuentes según la emoción seleccionada
            filtered_tweets = df[df['emocion'].apply(lambda x: emocion_seleccionada in x)]
            all_words = ' '.join(filtered_tweets['cleaned_tweet']).split()
            word_counts = Counter(all_words).most_common(20)

            # Crear DataFrame con las palabras más frecuentes
            df_word_freq = pd.DataFrame(word_counts, columns=['Palabra', 'Frecuencia'])

            # Gráfico de barras con las palabras más frecuentes
            fig_freq = px.bar(df_word_freq, x='Palabra', y='Frecuencia', title="Palabras más Frecuentes",
                                labels={"Palabra": "Palabra", "Frecuencia": "Frecuencia"},
                                color='Frecuencia', color_continuous_scale='Blues')
            st.plotly_chart(fig_freq, use_container_width=True)
    else:

        # Mostrar el mapa y la nube de palabras en la misma fila
        col_map, col_wordcloud = st.columns([1, 1], gap="large")

        # Mapa de Calor por Emociones
        with col_map:

            columns_to_check = ['miedo', 'ira', 'expectante', 'confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria']
            df[columns_to_check] = df[columns_to_check].apply(pd.to_numeric, errors='coerce')

            # Ahora, realiza la agrupación y la suma de forma segura
            porcen = df.groupby('pais')[columns_to_check].sum()            
            porcen = porcen.assign(suma=porcen.sum(axis=1))
            porcen = porcen.apply(lambda x: (x / porcen['suma']) * 100, axis=0)
            porcen = porcen.reset_index()

            # Cargar archivo geojson para el mapa
            data_geo = json.load(open('hispano.geojson'))

            # Crear el mapa
            world_map = folium.Map(location=[17.57, -85.74], zoom_start=2.4, tiles='cartodbpositron')

            # Crear Choropleth
            choropleth = folium.Choropleth(
                geo_data=data_geo,
                data=porcen,
                columns=['pais', emocion_seleccionada],
                key_on='feature.properties.name',
                fill_color="YlOrRd",
                fill_opacity=0.7,
                line_opacity=0.4,
                legend_name=f"Porcentaje de {emocion_seleccionada.capitalize()} por País"
            ).add_to(world_map)

            choropleth.geojson.add_child(folium.features.GeoJsonTooltip(['name'], labels=False))

            # Mostrar el mapa con ajuste automático
            folium_static(world_map, width=map_width, height=map_height)

        # Nube de Palabras sincronizada con la emoción seleccionada
        with col_wordcloud:
            if visualizacion_seleccionada == "Nube de Palabras":
                # Nube de Palabras sincronizada con la emoción seleccionada
                filtered_tweets = df[df['emocion'].apply(lambda x: emocion_seleccionada in x)]
                wordcloud_text = ' '.join(filtered_tweets['cleaned_tweet'])
                wordcloud = WordCloud(background_color='white', width=800, height=730).generate(wordcloud_text)
                plt.figure(figsize=(10, 6))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot(plt, use_container_width=True)
            else:
                # Mostrar las palabras más frecuentes según la emoción seleccionada
                filtered_tweets = df[df['emocion'].apply(lambda x: emocion_seleccionada in x)]
                all_words = ' '.join(filtered_tweets['cleaned_tweet']).split()
                word_counts = Counter(all_words).most_common(20)

                # Crear DataFrame con las palabras más frecuentes
                df_word_freq = pd.DataFrame(word_counts, columns=['Palabra', 'Frecuencia'])

                # Gráfico de barras con las palabras más frecuentes
                fig_freq = px.bar(df_word_freq, x='Palabra', y='Frecuencia', title="Palabras más Frecuentes",
                                  labels={"Palabra": "Palabra", "Frecuencia": "Frecuencia"},
                                  color='Frecuencia', color_continuous_scale='Blues')
                st.plotly_chart(fig_freq, use_container_width=True)


    st.header("Distribución de Polaridad y Comparación de Emociones")
    col_polaridad, col_emociones = st.columns([1, 1])
   

    # Gráfico de Polaridad
    with col_polaridad:
        polaridad_counts = df['polaridad'].value_counts()
        fig_polaridad = px.pie(polaridad_counts, names=polaridad_counts.index, values=polaridad_counts.values,
                               title="Distribución de Polaridades")
        st.plotly_chart(fig_polaridad, use_container_width=True)

    # Gráfico de Barras para Diferencia entre Emociones
    with col_emociones:
        emociones_counts = df.explode('emocion')['emocion'].value_counts()
        colores = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#ff6666','#ffcc66']  # Colores personalizados
        fig_emociones = px.bar(emociones_counts, x=emociones_counts.index, y=emociones_counts.values,
                               title="Diferencia entre Emociones", labels={"x": "Emoción", "y": "Cantidad de Tweets"},
                               color=emociones_counts.index, color_discrete_sequence=colores)
        st.plotly_chart(fig_emociones, use_container_width=True)





   # Evolución temporal de la intensidad de todas las emociones, con meses como eje X
    df_temporal = df[['miedo', 'ira', 'expectante', 'confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria']].resample('ME').sum()
    df_total = df_temporal.sum(axis=1)
    df_temporal = df_temporal.div(df_total, axis=0) * 100  # Convertir los valores a porcentajes
    df_temporal = df_temporal.reset_index()

    # Usar el mes en lugar de la fecha completa
    df_temporal['mes'] = df_temporal['fecha'].dt.strftime('%b %Y')  # Formatear la columna de fecha como Mes Año

    # Graficar la evolución temporal en porcentaje para todas las emociones
    # Graficar la evolución temporal en porcentaje para todas las emociones
    fig_temporal = px.line(
        df_temporal, 
        x='mes', 
        y=df_temporal.columns[1:-1], 
        title="Evolución Temporal del Porcentaje de Todas las Emociones (por Mes)",
        markers=True,
        labels={"value": "Porcentaje", "variable": "Emoción"}   
    )


    # Actualizar layout del gráfico
    fig_temporal.update_layout(
        xaxis_title="Mes", 
        yaxis_title="Porcentaje", 
        hovermode="x unified",  # Mostrar la línea vertical al pasar el cursor por un mes
        yaxis_ticksuffix="%",
    )

    # Mostrar el gráfico
    st.plotly_chart(fig_temporal, use_container_width=True)


# Vista Comparativa entre Países
elif view == "Vista Comparativa entre Países":

    st.title("Comparación de Emociones entre Países")
    # Selección de países y emoción, limitando la cantidad de países a seleccionar
    paises = df['pais'].unique()

    # Seleccionar aleatoriamente 5 países de la lista de países únicos
    selected_paises_random = np.random.choice(paises, size=5, replace=False)

   
    selected_paises = st.sidebar.multiselect("Seleccione País(es) (máximo 5)", options=paises, default=paises[:5],  max_selections=5)

   

    emociones = set(emocion for sublist in df['emocion'] for emocion in sublist)
    st.sidebar.title("Emociones")

    selected_emocion = st.sidebar.selectbox("Seleccione Emoción", options=emociones, index=list(emociones).index("miedo"))

    # Diagrama de burbujas para ver todos los países simultáneamente
    st.header("Relación de Emociones por País")
    emociones_por_pais = df.explode('emocion').groupby(['pais', 'emocion']).size().reset_index(name='Cantidad')
    fig_bubble = px.scatter(emociones_por_pais, x='pais', y='emocion', size='Cantidad', color='emocion',
                            title="Relación de Emociones por País", 
                            labels={"Cantidad": "Cantidad de Tweets", "emocion": "Emoción", "pais": "País"})
    fig_bubble.update_layout(xaxis_title="País", yaxis_title="Emoción", showlegend=False)
    st.plotly_chart(fig_bubble, use_container_width=True)





    st.header(f"Evolución de emociones")




    # Filtrar datos según países y emoción seleccionada
    temporal_por_pais = df[(df['pais'].isin(selected_paises)) & df['emocion'].apply(lambda x: selected_emocion in x)]


    # Agrupar por mes y país, luego sumar la emoción seleccionada
    temporal_por_pais = temporal_por_pais.groupby([pd.Grouper(freq='ME'), 'pais'])[selected_emocion].sum().reset_index()
    

    # Calcular el porcentaje mensual de la emoción seleccionada respecto al total de emociones
    temporal_por_pais['porcentaje'] = temporal_por_pais.groupby('fecha')[selected_emocion].transform(lambda x: (x / x.sum()) * 100)

    # Crear gráfico de líneas para mostrar la evolución temporal
    fig_temporal_paises = px.line(
        temporal_por_pais, 
        x='fecha', 
        y='porcentaje', 
        color='pais', 
        title=f"Evolución Temporal de {selected_emocion.capitalize()} en Países Seleccionados (en %)",
        markers=True,  # Añadir puntos en la línea
        line_shape='linear'  # Para una línea más clara
        
    )

    # Mejorar la presentación del eje X (solo mostrar meses)
    fig_temporal_paises.update_xaxes(
        dtick="M1",  # Marcar los meses
        tickformat="%b %Y",  # Mostrar el mes y año
        tickangle=0,  # Inclinación para mejor legibilidad,
        tickvals=pd.date_range(start='2024-01-01', end='2024-06-30', freq='ME'),  # Forzar las fechas correctas
        ticktext=['Enero 2024', 'Febrero 2024', 'Marzo 2024', 'Abril 2024', 'Mayo 2024', 'Junio 2024']  # Etiquetas personalizadas


    )

    # Etiquetas de los ejes
    fig_temporal_paises.update_layout(
        xaxis_title="Mes",
        yaxis_title=f"Porcentaje de {selected_emocion.capitalize()}",
        yaxis_ticksuffix="%",  # Añadir el símbolo de porcentaje en el eje Y
        hovermode="x unified",  # Mostrar una línea que cruza todos los países para facilitar la comparación


    )

    # Mostrar el gráfico
    st.plotly_chart(fig_temporal_paises, use_container_width=True)







    st.sidebar.title("Seleccione País")


    # Selección de un país específico para la nube de palabras y gráfico de radar
    pais_nube = st.sidebar.selectbox("Seleccione un País para ver la Nube de Palabras y Gráfico de Radar", options= paises)
   


    st.header(f"Análisis Comparativo de Emociones {pais_nube} - Emoción: {selected_emocion.capitalize()}")


    # Colocar el gráfico de radar y la nube de palabras en la misma fila
    col_radar, col_wordcloud = st.columns(2)

    

    # Gráfico de Radar para comparar emociones en el país seleccionado
    with col_radar:
        emociones_por_pais_radar = df[df['pais'] == pais_nube].groupby('pais').sum()[['miedo', 'ira', 'expectante', 'confianza', 'sorpresa', 'tristeza', 'repulsion', 'alegria']]
        emociones_por_pais_radar = emociones_por_pais_radar.reset_index()

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=emociones_por_pais_radar.iloc[0, 1:],
            theta=emociones_por_pais_radar.columns[1:],
            fill='toself',
            name=pais_nube
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, emociones_por_pais_radar.iloc[0, 1:].max()]
                )),
            showlegend=False,
            title=f"Intensidad de Emociones en {pais_nube}"
        )

        st.plotly_chart(fig_radar, use_container_width=True)


        

    # Nube de Palabras por País y Emoción Seleccionada
    with col_wordcloud:
        filtered_tweets = df[(df['pais'] == pais_nube) & df['emocion'].apply(lambda x: selected_emocion in x)]['cleaned_tweet']
        wordcloud_text = ' '.join(filtered_tweets)
        wordcloud = WordCloud(background_color='white', width=800, height=500).generate(wordcloud_text)
        plt.figure(figsize=(14, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt, use_container_width=True)
else:
    st.write("No hay países seleccionados.")