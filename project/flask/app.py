from flask import Flask, render_template, request, jsonify
import pandas as pd
from utiles import *

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresar-dataset')
def ingresarDataset():
    return render_template('ingresar-dataset.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró el archivo'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No se seleccionó un archivo'}), 400

    try:
        # Lee el archivo Excel en un DataFrame de pandas
        df = pd.read_excel(file)
        G = crear_grafo_desde_excel(df)

        distancia_minima, camino = dijkstra(G, nodo_inicio, nodo_fin)
        
        print(f"\nDistancia mínima desde {nodo_inicio} hasta {nodo_fin}: {distancia_minima} metros")
        print(f"Camino más corto: {' -> '.join(camino)}")

        #graficar(G,camino)
        #introducir aca metodo para graficar
        
        print(df.head())

        return jsonify({'message': 'Archivo recibido y procesado con éxito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresar-dataset', methods=['POST'])
def ingresarDataset():
    return render_template('ingresar-dataset.html')

@app.route('/usar-dataset')
def usarDataset():
    return render_template('usar-dataset.html')

# Ruta para procesar el archivo subido
@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica si se ha subido un archivo
    if 'file' not in request.files:
        return "No se subió ningún archivo."

    file = request.files['file']
    
    # Verifica que el archivo tenga extensión .xlsx
    if file.filename == '':
        return "El archivo no tiene nombre."
    if not file.filename.endswith('.xlsx'):
        return "Solo se permiten archivos .xlsx."

    # Lee el archivo en un DataFrame de pandas
    df = pd.read_excel(file)
    
    # Llama a una función para procesar el DataFrame
    resultado = procesar_excel(df)
    
    return f"Resultado del procesamiento: {resultado}"

def procesar_excel(df):
    # Ejemplo de procesamiento: devuelve la cantidad de filas y columnas del archivo
    filas, columnas = df.shape
    return f"El archivo tiene {filas} filas y {columnas} columnas."
"""

if __name__ == '__main__':
    app.run(debug=True)

