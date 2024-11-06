import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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
ruta_archivo = 'datasets/dataset 1/data_aristas.xlsx'

# Crear el grafo desde el archivo
G = crear_grafo_desde_excel(ruta_archivo)

# Definir el nodo origen y el nodo destino para calcular el flujo máximo
nodo_origen = 'TAN-159'  # Cambia esto por el nodo de origen que deseas
nodo_destino = 'USR-034'  # Cambia esto por el nodo de destino que deseas

# Calcular el flujo máximo
flujo_max, flujo_detalle = flujo_maximo_ford_fulkerson(G, nodo_origen, nodo_destino)

# Mostrar el flujo máximo
print(f"El flujo máximo de {nodo_origen} a {nodo_destino} es: {flujo_max} l/s")

# Mostrar el detalle del flujo en cada arista
print("Detalle del flujo en cada arista:")
for u, v in flujo_detalle.items():
    for destino, flujo in v.items():
        if flujo > 0:
            print(f"De {u} a {destino}: Flujo = {flujo} l/s")

# Detectar y mostrar los caminos críticos
caminos_criticos = detectar_caminos_criticos(G, flujo_detalle, nodo_origen, nodo_destino)

# Verificar y mostrar los caminos críticos o un mensaje en caso de que no existan
if caminos_criticos:
    print("\nCaminos críticos (caminos con flujo máximo en cada arista):")
    for idx, (camino, ruta) in enumerate(caminos_criticos, start=1):
        # Imprimir la ruta como una lista de nodos
        print(f"\nRuta de camino crítico {idx}: {' -> '.join(ruta)}")
        # También podemos imprimir los detalles de cada conexión en la ruta
        for u, v, flujo, capacidad in camino:
            print(f"De {u} a {v}: Flujo = {flujo} l/s, Capacidad = {capacidad} l/s")
else:
    print("No se encontró ningún camino crítico en la red.")

# Dibujar el grafo sin etiquetas ni flechas
plt.figure(figsize=(10, 6))

# Usar spring_layout para distribuir los nodos de manera visualmente agradable
pos = nx.spring_layout(G, seed=42)

# Dibujar nodos y aristas sin etiquetas ni direcciones
nx.draw_networkx_nodes(G, pos, node_size=10, node_color='skyblue')
nx.draw_networkx_edges(G, pos, edge_color='gray')

# Título opcional
plt.title("Grafo Primitivo")
plt.axis('off')  # Ocultar los ejes
plt.show()