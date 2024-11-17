from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
from utiles import *
import networkx as nx
from pyvis.network import Network
import os

app = Flask(__name__)

G = None  # Variable global para almacenar el grafo
Gnd = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ingresar-dataset')
def ingresarDataset():
    return render_template('ingresar-dataset.html')


@app.route('/usar-dataset')
def usarDataset():
        global G
        global Gnd

        # Ruta del archivo predefinido
        file_path = os.path.join(os.path.dirname(__file__), 'data_aristas.xlsx')

        try:
            # Leer el archivo Excel y construir el grafo
            df = pd.read_excel(file_path)
            G = crear_grafo_desde_excel(df)
            Gnd = crear_grafonodirigido_desde_excel(df)
            return render_template('mostrar-resultados.html')
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    global G
    global Gnd

    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró el archivo'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No se seleccionó un archivo'}), 400

    try:
        # Leer el archivo Excel y construir el grafo
        df = pd.read_excel(file)
        G = crear_grafo_desde_excel(df)
        Gnd = crear_grafonodirigido_desde_excel(df)
        return redirect(url_for('usarDataset'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/calcular/<algoritmo>', methods=['POST'])
def calcular_algoritmo(algoritmo):
    global G
    global Gnd


    if G is None:
        return jsonify({'error': 'No hay un grafo cargado.'}), 400

    nodo_inicio = request.json.get('nodo_inicio')
    nodo_fin = request.json.get('nodo_fin')

    if not nodo_inicio or not nodo_fin:
        return jsonify({'error': 'Debe proporcionar nodos de inicio y fin.'}), 400

    try:
        camino = []
        distancia = 0

        if algoritmo == 'dijkstra':
            distancia, camino = dijkstra(Gnd, nodo_inicio, nodo_fin)
            print(camino)

            path_edges = list(zip(camino, camino[1:]))
            print(path_edges)
            response = {
                'nodos': [{'id': node, 'label': node} for node in camino],
                'aristas': [{'from': edge[0], 'to': edge[1], 'label': str(Gnd[edge[0]][edge[1]].get('weight', 0))} for edge in path_edges],
                'info': f'Distancia mínima: {distancia} metros',
                'description': f"Detalle del camino minimo: {camino} ",
            }

        elif algoritmo == 'flujo-maximo':
            maxFlow, caminos = flujo_maximo_ford_fulkerson(G, nodo_inicio, nodo_fin)

            if caminos:

                path_edges = []
                nodes = set()
                for camino in caminos:
                    path_edges.extend(list(zip(camino, camino[1:])))
                    nodes.update(camino)
                
                print(path_edges)
                response = {
                    'nodos': [{'id': node, 'label': node} for node in nodes],
                    'aristas': [{'from': edge[0], 'to': edge[1], 'label': str(G[edge[0]][edge[1]].get('weight', 0))} for edge in path_edges],
                    'info': f'Flujo maximo: {maxFlow} l/s',
                    'description': f"Detalle del flujo en cada arista: {caminos} ",
                }
            else:
                return jsonify({'error': 'No se encontraron caminos.'}), 400

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
