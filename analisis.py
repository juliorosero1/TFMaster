import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo CSV
df = pd.read_csv('sentimientosTweet_3.csv')

# Asegúrate de que exista una columna con las emociones predichas
# Aquí usaremos la columna 'emocion' como la emoción real
# Agrega o reemplaza la columna 'emocion_predicha' con los valores que predijo tu modelo
# Ejemplo (esto es solo para propósitos de demostración):
df['emocion_predicha'] = df['emocion']  # Simulación, reemplazar con las emociones predichas

# Extraer las columnas de emociones reales y predichas
y_real = df['emocion']  # Columna de emociones reales
y_pred = df['emocion_predicha']  # Columna de emociones predichas

# Crear la matriz de confusión
cm = confusion_matrix(y_real, y_pred)

# Visualizar la matriz de confusión
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=set(y_real), yticklabels=set(y_real))
plt.xlabel('Predicho')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.show()
