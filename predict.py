import pandas as pd
from collections import Counter
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
import re

# Cargar el modelo y las clases
with open('notebooks/model.pkl', 'rb') as file:
    model, classes = pickle.load(file)

# Cargar el LabelEncoder
with open('notebooks/label_encoder.pkl', 'rb') as file:
    le = pickle.load(file)

# Ajustar el LabelEncoder a tus etiquetas de clase
le.fit(['Negativo', 'Neutro', 'Positivo'])

# Imprimir las clases con las etiquetas de texto correspondientes
for i, sentiment in enumerate(classes):
    print(f"{i}: {le.inverse_transform([sentiment])[0]}")

# Cargar el vectorizador
with open('notebooks/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

stopwords = stopwords.words('spanish')

# Cargar el archivo CSV
df = pd.read_csv('comentarios_mejorados.csv', sep='|')

# Filtrar las filas donde el parent_id sea nulo
df = df[df.parentId.isnull()]

# Eliminar todas las columnas excepto 'textDisplay'
columnas_a_eliminar = ['channelId', 'videoId', 'textOriginal', 'authorDisplayName', 
                       'authorProfileImageUrl', 'authorChannelUrl', 'authorChannelId', 
                       'canRate', 'viewerRating', 'likeCount', 'publishedAt', 
                       'updatedAt', 'parentId']

# Eliminar las columnas
df = df.drop(columnas_a_eliminar, axis=1)

# Función para preprocesar el texto
def preprocess_text(text):
    # Convertir el texto a minúsculas
    text = text.lower()
    # Eliminar los caracteres no alfabéticos
    text = re.sub(r'[^a-záéíóúñü]', ' ', text)
    # Eliminar los caracteres numéricos
    text = re.sub(r'\d', ' ', text)
    # Eliminar las palabras vacías
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

# Aplicar la función de preprocesamiento al texto
df['textDisplay'] = df['textDisplay'].apply(preprocess_text)

# Eliminar las filas donde el texto esté vacío
df = df[df.textDisplay != '']

# Vectorizar el texto
X = vectorizer.transform(df['textDisplay'])
    
# Hacer predicciones
y_pred = model.predict(X)

# Contar las predicciones
counter = Counter(y_pred)

# Imprimir el conteo de predicciones
for sentiment, count in counter.items():
    print(f"{sentiment}: {count}")
