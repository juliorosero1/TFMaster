import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

# Lista manual de stopwords en español, convertidas a minúsculas


stop_words_spanish = [
    'el', 'la', 'los', 'las', 'en', 'por', 'un', 'una', 'y', 'a', 'se', 'que', 'de', 
    'del', 'al', 'con', 'para', 'es', 'su', 'lo', 'como', 'más', 'pero', 'no', 'le',
    'me', 'mi', 'te', 'tu', 'sí', 'ya', 'si', 'todo', 'esta', 'este', 'ser', 'son',
    'ha', 'hay', 'sus', 'o', 'qué', 'cuál', 'cual', 'nos', 'nosotros', 'ustedes', 'vosotros',
    'ellos', 'ellas', 'también', 'muy', 'aquí', 'allí', 'allá', 'debe', 'donde', 'sobre',
    'estos', 'tienen', 'solo', 'puede', 'porque', 'entre', 'hace', 'hasta', 'sin', 'la', 'un'
]





# Agregar palabras adicionales que no son útiles
custom_stopwords = set([word.lower() for word in stop_words_spanish + ['https', 'co', 'rt', 't', 'c']])

# Leer datos
df = pd.read_csv("sentimientosTweet_3.csv")

# Función para eliminar stopwords manualmente
def remove_stopwords(text):
    tokens = text.lower().split()
    cleaned_tokens = [word for word in tokens if word not in custom_stopwords]
    return ' '.join(cleaned_tokens)

# Aplicar la función a cada tweet
df['cleaned_tweet'] = df['tweet'].apply(remove_stopwords)

# Vectorizar los tweets limpios (palabras y bigramas)
vectorizer = TfidfVectorizer(max_df=0.9, min_df=2, ngram_range=(1, 2))  # Unigramas y bigramas
X = vectorizer.fit_transform(df['cleaned_tweet'])

# Aplicar KMeans para encontrar tópicos
num_clusters = 5  # Puedes ajustar el número de clústeres según tus necesidades
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Asignar clústeres al DataFrame
df['cluster'] = kmeans.labels_

# Obtener los términos de la vectorización
terms = vectorizer.get_feature_names_out()
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

# Contador de palabras
word_counts = Counter()

# Recopilar las palabras más comunes por clúster y contarlas
for i in range(num_clusters):
    common_terms = [terms[ind] for ind in order_centroids[i, :10]]  # No se filtra por unigramas o bigramas aquí
    word_counts.update(common_terms)

# Guardar las palabras y sus frecuencias en un archivo CSV
with open('frecuenciaPal.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = pd.DataFrame.from_dict(word_counts, orient='index', columns=['frecuencia']).reset_index()
    writer.columns = ['palabra', 'frecuencia']
    writer.to_csv(file, index=False)

print("El archivo frecuenciaPal.csv ha sido creado con éxito.")
