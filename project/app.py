from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
from utiles import *
import networkx as nx
from pyvis.network import Network

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
    return render_template('mostrar-resultados.html')


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
            }

        elif algoritmo == 'flujo-maximo':
            maxFlow, caminos = flujo_maximo_ford_fulkerson(G, nodo_inicio, nodo_fin)
            print(caminos)
            for camino in caminos:
                path_edges = list(zip(camino, camino[1:]))
            print(path_edges)
            response = {
                'nodos': [{'id': node, 'label': node} for node in camino],
                'aristas': [{'from': edge[0], 'to': edge[1], 'label': str(G[edge[0]][edge[1]].get('weight', 0))} for edge in path_edges],
                'info': f'Flujo maximo: {maxFlow} l/s',
            }

        elif algoritmo == 'caminos-criticos':
            caminos = detectar_caminos_criticos(G, nodo_inicio, nodo_fin)
            response = {
                'nodos': [{'id': node, 'label': node} for node in camino],
                'aristas': [{'from': u, 'to': v, 'label': str(data.get('capacity', 0))} for u, v, data in G.edges(data=True)],
                'info': f'Distancia mínima: {distancia} metros',
            }
        else:
            return jsonify({'error': 'Algoritmo no reconocido.'}), 400

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)



"""
3.0
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresar-dataset')
def ingresarDataset():
    return render_template('ingresar-dataset.html')

@app.route('/usar-dataset')
def usarDataset():
    return render_template('mostrar-resultados.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global G, distancia_minima, camino

    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró el archivo'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No se seleccionó un archivo'}), 400

    try:
        # Leer el archivo Excel y construir el grafo
        df = pd.read_excel(file)
        G = crear_grafo_desde_excel(df)

        # Obtener nodos de inicio y fin desde el formulario
        nodo_inicio = request.form.get('nodo_inicio')
        nodo_fin = request.form.get('nodo_fin')

        if not nodo_inicio or not nodo_fin:
            return jsonify({'error': 'Debe proporcionar nodos de inicio y fin'}), 400

        # Calcular el camino más corto
        distancia_minima, camino = dijkstra(G, nodo_inicio, nodo_fin)

        # Redirigir a la página de resultados
        return redirect(url_for('resultados'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resultados')
def resultados():
    global G, distancia_minima, camino

    if G is None or distancia_minima is None or camino is None:
        return jsonify({'error': 'No hay resultados para mostrar. Por favor, cargue un archivo.'}), 400

    path_edges = list(zip(camino, camino[1:]))

    # Crear grafo interactivo con pyvis
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    for node in camino:
        net.add_node(node, label=node)
    for edge in path_edges:
        net.add_edge(*edge, value=G.edges[edge]['weight'])

    return render_template("mostrar-resultados.html", nodos=net.nodes, aristas=net.edges)

if __name__ == '__main__':
    app.run(debug=True)

"""