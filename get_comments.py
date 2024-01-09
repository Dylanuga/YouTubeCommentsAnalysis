# Importar las bibliotecas necesarias
import pandas as pd
from googleapiclient.discovery import build
from config import api_key

# Definir la clave de API
api_key = api_key

# Construir el objeto youtube usando la clave de API
youtube = build("youtube", "v3", developerKey=api_key)

def buscar_video(youtube, query):
    # Hacer una solicitud a la API de búsqueda de YouTube
    response = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=1  # Solo queremos el primer resultado
    ).execute()

    # Obtener el ID del video del primer resultado
    video_id = response["items"][0]["id"]["videoId"]

    return video_id

# Definir una función para obtener los comentarios de un video
def get_comments(youtube, video_id, comments=[], token=None):
    # Hacer una solicitud a la API para obtener los comentarios
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        pageToken=token,
        maxResults=100  # El máximo permitido por la API
    ).execute()

    # Iterar sobre los elementos de la respuesta
    for item in response["items"]:
        # Obtener el comentario de nivel superior
        comment = item["snippet"]["topLevelComment"]["snippet"]
        # Añadir el comentario a la lista de comentarios
        comments.append(comment)

        # Comprobar si el comentario tiene respuestas
        if item["snippet"]["totalReplyCount"] > 0:
            # Obtener las respuestas del comentario
            replies = youtube.comments().list(
                part="snippet",
                parentId=item["id"],
                maxResults=100  # El máximo permitido por la API
            ).execute()

            # Iterar sobre las respuestas y añadirlas a la lista de comentarios
            for reply in replies["items"]:
                comments.append(reply["snippet"])

    # Comprobar si hay más comentarios en la siguiente página
    if "nextPageToken" in response:
        # Llamar a la función de forma recursiva con el token de la siguiente página
        get_comments(youtube, video_id, comments, response["nextPageToken"])

    # Devolver la lista de comentarios
    return comments

# Solicitar el título del videojuego al usuario
videojuego = input("Por favor, introduce el título de un videojuego: ")

try:
    # Buscar en YouTube "Análisis videojuego"
    video_id = buscar_video(youtube, f"Análisis {videojuego}")
    print("Video ID:", video_id)

    # Llamar a la función con el ID del video
    comments = get_comments(youtube, video_id)

    # Convertir la lista de comentarios en un dataframe de pandas
    df = pd.DataFrame(comments)

    df.to_csv('comentarios_mejorados.csv', sep=',', index=False)


except Exception as e:
    print("Error:", str(e))
