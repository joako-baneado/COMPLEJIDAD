import heapq

class Graph:
    def __init__(self):
        self.graph = {}  # Diccionario para almacenar el grafo

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, weight))  # Agrega la arista con su peso

    def dijkstra(self, start):
        # Inicializa las distancias y la cola de prioridad
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]  # (distancia, nodo)

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            # Si encontramos una distancia mayor a la ya conocida, la ignoramos
            if current_distance > distances[current_vertex]:
                continue

            # Explora los vecinos
            for neighbor, weight in self.graph[current_vertex]:
                distance = current_distance + weight

                # Si encontramos un camino más corto, actualizamos la distancia
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

# Ejemplo de uso
if __name__ == "__main__":
    g = Graph()
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 1)
    g.add_edge('D', 'E', 3)

    start_vertex = 'A'
    distances = g.dijkstra(start_vertex)
    print("Distancias desde el vértice:", start_vertex)
    for vertex, distance in distances.items():
        print(f"Distancia a {vertex}: {distance}")
