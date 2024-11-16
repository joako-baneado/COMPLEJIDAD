import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq   # Importamos heapq para Dijkstra


# Función para leer el archivo Excel y crear el grafo
def crear_grafo_desde_excel(df_):
    df = df_
    G = nx.DiGraph()  # Grafo dirigido
    
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

def obtener_grafico(G,camino):
    # Graficar solo el camino mínimo en el grafo
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)  # Posición de los nodos para el gráfico

    # Resaltar solo el camino mínimo en el gráfico
    path_edges = list(zip(camino, camino[1:]))  # Crear las aristas del camino mínimo
    nx.draw_networkx_nodes(G, pos, nodelist=camino, node_size=50, node_color='orange')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='orange', width=2)

    # Etiquetas opcionales para los nodos en el camino
    nx.draw_networkx_labels(G, pos, labels={node: node for node in camino}, font_size=8)

    # Título y mostrar el gráfico
    plt.title(f"Camino mínimo desde {nodo_inicio} hasta {nodo_fin}")
    plt.axis('off')  # Ocultar los ejes
    plt.savefig('grafico.png')


nodo_inicio = 'TAN-159'  # Cambia esto por el nodo de origen que deseas
nodo_fin = 'USR-034'  # Cambia esto por el nodo de destino que deseas