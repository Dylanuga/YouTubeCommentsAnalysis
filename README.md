# Analisis de comentarios de Youtube sobre videojuegos
## Introducción
El objetivo de este proyecto es analizar los comentarios de Youtube sobre videojuegos, para ello se ha utilizado la API de Youtube para obtener los comentarios de los videos de los canales de videojuegos más populares. Una vez obtenidos los comentarios se ha realizado un preprocesamiento de los mismos para eliminar las palabras que no aportan información y se ha realizado un análisis de sentimiento para obtener la polaridad de los comentarios. Finalmente se ha realizado un análisis de los resultados obtenidos.

## Obtención de los comentarios
En el script get_comments.py se ha utilizado la API de Youtube para obtener los comentarios de los videos de los canales de videojuegos más populares. Para ello se ha utilizado la librería [googleapiclient.discovery]