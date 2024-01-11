from flask import Flask, render_template, request
import pandas as pd
from config import * # Asegúrate de importar tu archivo de configuración
from get_comments import buscar_video, get_comments
from googleapiclient.discovery import build

# Definir la clave de API
api_key = api_key

# Construir el objeto youtube usando la clave de API
youtube = build("youtube", "v3", developerKey=api_key)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game = request.form.get('game')
        if game:
            video_id = buscar_video(youtube, game)
            comments = get_comments(youtube, video_id)
            df = pd.DataFrame(comments)
            df.to_csv('comentarios_mejorados.csv', sep='|', index=False)
            return render_template('index.html', comments=comments, rawg_key=rawg_key)
    return render_template('index.html', rawg_key=rawg_key)

if __name__ == '__main__':
    app.run(debug=True)