import pandas as pd
from tqdm import tqdm  # barra carga
import sys
import ClasificadorLocalidad_2 as clo
#import ClasificadorNoticia_2 as cln

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

####################################
# SELECCIONAR EL ARCHIVO YA CON LA UBICACIÓN
# Cargar los datos desde el archivo CSV
#data = pd.read_csv('tweetsUbicacion.csv')
data = pd.read_csv('data.csv')


# Limpieza en caso de obtener tweets por web scraping
if "T" in data.fecha[3]:
    id_list = []
    for i in range(data.fecha.count()):
        data.at[i, 'fecha'] = data.at[i, 'fecha'].replace('T', " ").replace('.000Z', "")
        id_list.append(i + 1)

    data.insert(loc=0, column="id", value=id_list)
print(data)

# Columnas seleccionadas
cols = ['id', 'user', 'fecha', 'tweet', 'locacion']

# Limpiar tweets repetidos y registros vacíos en locacion
df = data.drop_duplicates(subset=['tweet'], keep='first')
df['locacion'] = df['locacion'].fillna("NA")  # Rellenar valores NA en locacion

# Convertir la columna id a string
df['id'] = df['id'].astype(str)
print(df)

# Eliminar registros erróneos en el campo id
aux = []
for i in df.index:
    if 'a' in df.at[i, 'id'] or 'e' in df.at[i, 'id']:
        print(df.at[i, 'id'])
    else:
        aux.append([df.at[i, 'id'], df.at[i, 'user'], df.at[i, 'fecha'], df.at[i, 'tweet'], df.at[i, 'locacion']])

df = pd.DataFrame(aux, columns=cols)

# Asignación de países basado en la locación
print("\nCorrigiendo localidad en tweets:")
bucle = tqdm(total=df.shape[0], position=0, leave=False)  # Barra de carga

# Utilizar una lista para acumular resultados y luego convertir a DataFrame
resultados = []
for tw in df['locacion']:
    resultados.append({'locacion': clo.clasificarPais(tw)})
    bucle.set_description(f"Cargando... {tw}")  # Actualización de la barra de carga
    bucle.update(1)

bucle.close()

# Convertir la lista de resultados en un DataFrame
pais = pd.DataFrame(resultados)

# Asignar el DataFrame de paises al DataFrame principal
temp = df.assign(pais=pais['locacion'].values)
temp.to_csv("limpiezaXlocacion_2.csv", index=False, header=True, encoding="utf-8")

print("\n   => Corrección realizada satisfactoriamente!!!")
print("\n    => Reducción de registros de " + str(data.shape[0]) + " a " + str(temp.shape[0]) + "\n")
