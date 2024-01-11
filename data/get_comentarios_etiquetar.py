import sys
from pathlib import Path

# Agregar la raíz del proyecto al sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from get_comments import buscar_video, get_comments
import pandas as pd
from googleapiclient.discovery import build
from config import api_key


def buscar_videos_lista(youtube, videojuegos):
    video_ids = []

    for videojuego in videojuegos:
        # Realizar la búsqueda en YouTube
        search_response = youtube.search().list(
            q=f"Análisis {videojuego}",
            part="id,snippet",
            maxResults=1
        ).execute()

        # Obtener el ID del primer video en los resultados de la búsqueda
        video_id = search_response['items'][0]['id']['videoId']

        # Agregar el ID del video a la lista
        video_ids.append(video_id)

    return video_ids

# Crear una instancia de la API de YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

# Definir la lista de videojuegos
videojuegos = ["Marvel's Spider-Man 2", "God of War: Ragnarök", "Hi-Fi Rush", "Kingdom Hearts III", "The Lord of the Rings: Gollum"]

# Obtener los IDs de los videos de análisis para cada videojuego
video_ids = buscar_videos_lista(youtube, videojuegos)

# Crear una lista vacía para almacenar los DataFrames
dfs = []

# Inicializar el contador
contador = 1

# Para cada videojuego en la lista
for videojuego, video_id in zip(videojuegos, video_ids):
    try:
        # Imprimir la consulta de búsqueda
        print(f"Buscando: Análisis {videojuego}")

        # Llamar a la función con el ID del video
        comments = get_comments(youtube, video_id)

        # Imprimir los comentarios obtenidos
        print(f"Comentarios obtenidos: {comments}")

    except Exception as e:
        print(f"Error al obtener los comentarios para el videojuego {videojuego}: {str(e)}")
        continue

    try:
        # Convertir la lista de comentarios en un dataframe de pandas
        df = pd.DataFrame(comments)

        # Agregar una nueva columna con el nombre del videojuego
        df['videojuego'] = videojuego

        # Guardar el DataFrame en un archivo CSV
        df.to_csv(f'df_{contador}.csv', sep=',', index=False)

        # Incrementar el contador
        contador += 1

        # Actualizar el videoId anterior
        video_id_anterior = video_id

    except Exception as e:
        print(f"Error al procesar el DataFrame para el videojuego {videojuego}: {str(e)}")

# # Concatenar todos los DataFrames en uno solo
# df_final = pd.concat(dfs)

# columnas_a_eliminar = ['channelId', 'videoId', 'textOriginal', 'authorDisplayName', 
#                        'authorProfileImageUrl', 'authorChannelUrl', 'authorChannelId', 
#                        'canRate', 'viewerRating', 'likeCount', 'publishedAt', 
#                        'updatedAt', 'parentId']

# # Eliminar las columnas
# df_final = df_final.drop(columnas_a_eliminar, axis=1)

# # Crear columna con el sentimiento que se va a rellenar manualmente
# df_final['sentimiento'] = ''

# import re

# def clean_text(text):
#     # Eliminar caracteres especiales y emojis, pero mantener las tildes
#     text = re.sub(r'[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ]+', ' ', text)
#     # Minúsculas
#     text = text.lower()
#     # Eliminar espacios en blanco innecesarios
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# # Aplicar la función de limpieza de texto a la columna 'textDisplay'
# df_final['textDisplay'] = df_final['textDisplay'].apply(clean_text)

# # Mostrar las primeras filas del DataFrame
# print(df_final.head())

# # Guardar el DataFrame final en un archivo CSV
# df_final.to_csv('dataset_labeled_clean.csv', sep=',', index=False)