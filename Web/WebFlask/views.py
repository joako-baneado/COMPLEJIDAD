from WebFlask import app
from flask import render_template
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        "index.html",
        name = "Sistema de Distribucion de Agua",
        title = "SISTEMA DE DISTRIBUCION DE AGUA",
        subtitle1 = "INGRESAR DATASET",
        subtitle2 = "USAR DATASET PREDETERMINADO",
        message1 = "Ir a ingresar dataset",
        message2 = "Mostrar algoritmos")

@app.route('/ingresar-dataset')
def ingresar_dataset():
    return render_template(
        "ingresar-dataset.html",
        name = "Ingresar Dataset",
        title = "INGRESAR DATASET",
        content = "(El archivo xlsx debe tener el formato de la siguiente imagen)",
        button = "Seleccionar archivo")

# Función para leer el archivo Excel y crear el grafo
def crear_grafo_desde_excel(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    G = nx.DiGraph()  # Grafo dirigido
    
    # Agregar nodos y aristas al grafo
    for index, row in df.iterrows():
        origen = row['ID Origen']
        destino = row['ID Destino']
        capacidad = row['Capacidad Flujo (l/s)']
        
        # Añadir una arista con la capacidad como peso
        G.add_edge(origen, destino, capacity=capacidad)
    
    return G

# Función para calcular el flujo máximo usando Ford-Fulkerson
def flujo_maximo_ford_fulkerson(G, origen, destino):
    # Usar la función de flujo máximo de NetworkX
    flujo_max, flujo_dict = nx.maximum_flow(G, origen, destino, capacity='capacity')
    return flujo_max, flujo_dict

# Función para detectar y mostrar caminos críticos
def detectar_caminos_criticos(G, flujo_dict, origen, destino):
    # Crear una lista para almacenar los caminos críticos
    caminos_criticos = []
    
    # Función auxiliar para hacer una búsqueda de camino crítico
    def buscar_camino_critico(nodo_actual, camino_actual, ruta_actual):
        if nodo_actual == destino:  # Si llegamos al destino, añadimos el camino completo
            caminos_criticos.append((camino_actual, ruta_actual))
            return
        
        # Recorrer los nodos adyacentes en el flujo
        for vecino, flujo in flujo_dict[nodo_actual].items():
            capacidad = G[nodo_actual][vecino]['capacity']
            
            # Verificar si la arista está saturada (flujo == capacidad)
            if flujo == capacidad and flujo > 0:
                # Continuar buscando en el siguiente nodo, añadiendo la arista al camino actual
                buscar_camino_critico(vecino, camino_actual + [(nodo_actual, vecino, flujo, capacidad)], ruta_actual + [vecino])
    
    # Iniciar la búsqueda desde el origen
    buscar_camino_critico(origen, [], [origen])
    
    return caminos_criticos

# Ruta del archivo de Excel
ruta_archivo = 'WebFlask/datasets/dataset 1/data_aristas.xlsx'

# Crear el grafo desde el archivo
G = crear_grafo_desde_excel(ruta_archivo)

# Definir el nodo origen y el nodo destino para calcular el flujo máximo
nodo_origen = 'TAN-159'  # Cambia esto por el nodo de origen que deseas
nodo_destino = 'USR-034'  # Cambia esto por el nodo de destino que deseas

# Calcular el flujo máximo
flujo_max, flujo_detalle = flujo_maximo_ford_fulkerson(G, nodo_origen, nodo_destino)

lista = []

for u, v in flujo_detalle.items():
    for destino, flujo in v.items():
        if flujo > 0:
            lista.append(f"De {u} a {destino}: Flujo = {flujo} l/s")

# Detectar y mostrar los caminos críticos
caminos_criticos = detectar_caminos_criticos(G, flujo_detalle, nodo_origen, nodo_destino)

lista1 = []
lista2= []
lista3 = []
lista4 = []

# Verificar y mostrar los caminos críticos o un mensaje en caso de que no existan
if caminos_criticos:
    lista1.append("\nCaminos criticos (caminos con flujo maximo en cada arista):")
    for idx, (camino, ruta) in enumerate(caminos_criticos, start=1):
        # Imprimir la ruta como una lista de nodos
        lista2.append(f"\nRuta de camino critico {idx}: {' -> '.join(ruta)}")
        # También podemos imprimir los detalles de cada conexión en la ruta
        for u, v, flujo, capacidad in camino:
            lista3.append(f"De {u} a {v}: Flujo = {flujo} l/s, Capacidad = {capacidad} l/s")
else:
    lista4.append("No se encontro ningun camino critico en la red.")

@app.route('/mostrar-algoritmos')
def mostrar_algoritmos():
    return render_template(
        "mostrar-algoritmos.html",
        name = "Mostrar Resultados",
        button1 = "Mostrar lista de nodos",
        button2 = "Flujo maximo",
        button3 = "Camino minimo",
        button4 = "Caminos criticos",
        title1 = "Nodo Inicial",
        title2 = "Nodo Final")

@app.route('/flujo-maximo')
def maximo():
    return render_template(
        "maximo.html",
        name = "Flujo maximo",
        grafo = "",
        content1 = f"El flujo maximo de {nodo_origen} a {nodo_destino} es: {flujo_max} l/s",
        content2 = "Detalle del flujo en cada arista:",
        content3 = lista)

@app.route('/camino-critico')
def critico():
    return render_template(
        "camino-critico.html",
        name = "Camino critico",
        grafo = "",
        content1 = f"El camino critico de {nodo_origen} a {nodo_destino}:",
        content2 = lista1,
        content3 = lista2,
        content4 = lista3,
        content5 = lista4)

@app.route('/camino-minimo')
def minimo():
    return render_template(
        "camino-minimo.html",
        name = "Camino minimo",
        grafo = "",
        content1 = f"El camino minimo de {nodo_origen} a {nodo_destino}:",
        #content2 = f"\nDistancia minima desde {nodo_origen} hasta {nodo_destino}: {distancia_minima} metros",
        #content3 = f"Camino mas corto: {' -> '.join(camino)}"
        )