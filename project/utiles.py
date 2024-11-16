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

# Función para calcular el flujo máximo usando Ford-Fulkerson
def flujo_maximo_ford_fulkerson(G, origen, destino):
    # Crear un diccionario para almacenar el flujo en cada arista
    flujo_dict = {}
    
    # Inicializar el flujo en cada arista a cero
    for u in G:
        flujo_dict[u] = {}
        for v in G[u]:
            flujo_dict[u][v] = 0
    
    # Función auxiliar para encontrar un camino aumentante
    def encontrar_camino_aumentante(G, flujo_dict, origen, destino):
        # Crear una lista para almacenar el camino aumentante
        camino = []
        
        # Crear una lista para almacenar los nodos visitados
        visitados = []
        
        # Función auxiliar para hacer una búsqueda en profundidad
        def dfs(G, flujo_dict, actual, destino, visitados, camino):
            visitados.append(actual)
            
            # Si llegamos al destino, hemos encontrado un camino aumentante
            if actual == destino:
                return True
            
            # Recorrer los nodos adyacentes en el grafo residual
            for vecino in G[actual]:
                # Verificar si la arista no está saturada (flujo < capacidad)
                if flujo_dict[actual][vecino] < G[actual][vecino]:
                    # Verificar si el vecino no ha sido visitado
                    if vecino not in visitados:
                        # Añadir el vecino al camino
                        camino.append((actual, vecino))
                        
                        # Hacer una búsqueda en profundidad desde el vecino
                        if dfs(G, flujo_dict, vecino, destino, visitados, camino):
                            return True
                        
                        # Si no se encontró un camino aumentante, retroceder
                        camino.pop()
            
            return False
        
        # Iniciar la búsqueda en profundidad desde el origen
        dfs(G, flujo_dict, origen, destino, visitados, camino)
        
        return camino
    
    # Encontrar un camino aumentante hasta que no haya más
    while True:
        # Encontrar un camino aumentante
        camino = encontrar_camino_aumentante(G, flujo_dict, origen, destino)
        
        # Si no se encontró un camino aumentante, terminar
        if not camino:
            break
        
        # Calcular el flujo máximo que se puede enviar por el camino aumentante
        flujo_maximo = float('inf')
        for u, v in camino:
            capacidad = G[u][v]
            flujo_actual = flujo_dict[u][v]
            flujo_maximo = min(flujo_maximo, capacidad - flujo_actual)
        
        # Actualizar el flujo en cada arista del camino aumentante
        for u, v in camino:
            flujo_dict[u][v] += flujo_maximo
            flujo_dict[v][u] -= flujo_maximo
    
    # Calcular el flujo máximo total desde el origen
    flujo_max = sum(flujo_dict[origen].values())
    
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

def graficar(G,camino):
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
    plt.show()


nodo_inicio = 'TAN-159'  # Cambia esto por el nodo de origen que deseas
nodo_fin = 'USR-034'  # Cambia esto por el nodo de destino que deseas
