import pandas as pd
import networkx as nx

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

# Ruta del archivo de Excel
ruta_archivo = 'datasets/dataset 1/data_aristas.xlsx'

# Crear el grafo desde el archivo
G = crear_grafo_desde_excel(ruta_archivo)

# Definir el nodo origen y el nodo destino para calcular el flujo máximo
nodo_origen = 'EST-037'  # Cambia esto por el nodo de origen que deseas
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
