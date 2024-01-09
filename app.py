from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game = request.form.get('game')
        if game:
            # obtén los comentarios de YouTube aquí
            # procesa los comentarios con pandas aquí
            resultados = None  # reemplaza None con tus resultados procesados
            return render_template('resultados.html', resultados=resultados)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)