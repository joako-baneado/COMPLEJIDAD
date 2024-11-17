import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq   # Importamos heapq para Dijkstra
from collections import deque, defaultdict

# Función para leer el archivo Excel y crear el grafo
def crear_grafo_desde_excel(df_):
    df = df_
    G = nx.DiGraph()  # Grafo dirigido
    
    # Agregar nodos y aristas al grafo
    for index, row in df.iterrows():
        origen = row['ID Origen']
        destino = row['ID Destino']
        capacidad =row['Capacidad Flujo (l/s)']
        
        # Añadir una arista con la capacidad como peso
        G.add_edge(origen, destino, weight=capacidad)
    
    return G

def crear_grafonodirigido_desde_excel(df_):
    df = df_
    G = nx.Graph()  # Grafo nodirigido
    
    # Agregar nodos y aristas al grafo
    for index, row in df.iterrows():
        origen = row['ID Origen']
        destino = row['ID Destino']
        distancia = row['Longitud Tubería (m)']
        
        # Añadir una arista con la capacidad como peso
        G.add_edge(origen, destino, weight=distancia)
    
    return G

# Modificación en el algoritmo de Dijkstra para recibir nodo de inicio y fin
def dijkstra(G, start, end):
    distances = {node: float('infinity') for node in G.nodes}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {node: None for node in G.nodes}  # Para rastrear el camino

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:  # Terminar al llegar al nodo de destino
            break

        if current_distance > distances[current_node]:
            continue
        
        for neighbor in G.neighbors(current_node):
            weight = G[current_node][neighbor]['weight']
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node  # Almacenar el nodo previo
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruir el camino mínimo desde el nodo final hacia atrás
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path = path[::-1]  # Invertir el camino para mostrar de inicio a fin

    return distances[end], path

def bfs_capacity(graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        current = queue.popleft()
    
        for neighbor, capacity in graph[current].items():
            if neighbor not in visited and capacity > 0:
                parent[neighbor] = current
                visited.add(neighbor)
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False


def flujo_maximo_ford_fulkerson(graph, source, sink):
    # Create a residual graph
    residual_graph = defaultdict(lambda: defaultdict(int))
    for u in graph:
        for v, attributes in graph[u].items():
            residual_graph[u][v] = attributes['weight']

    parent = {}
    max_flow_value = 0
    flow_dict = defaultdict(lambda: defaultdict(int))
    caminos_recorridos = []

    while bfs_capacity(residual_graph, source, sink, parent):
        # Find the minimum capacity in the path from source to sink
        path_flow = float('Inf')
        s = sink
        camino_actual = []  # Lista para el camino actual
        while s != source:
            camino_actual.append(s)
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]
        camino_actual.append(source)
        camino_actual.reverse()  # Invertir para que esté en orden de fuente a sumidero
        caminos_recorridos.append(camino_actual)
        # Update residual graph capacities
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            flow_dict[u][v] += path_flow  # Track the flow
            v = parent[v]
        
        max_flow_value += path_flow

    # Clean up flow_dict to remove zero flows
    for u in list(flow_dict.keys()):
        for v in list(flow_dict[u].keys()):
            if flow_dict[u][v] == 0:
                del flow_dict[u][v]
        if not flow_dict[u]:
            del flow_dict[u]

    return max_flow_value, caminos_recorridos