class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Número de vértices
        self.graph = [[0] * vertices for _ in range(vertices)]  # Matriz de adyacencia

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def _dfs(self, s, t, parent):
        visited = [False] * self.V
        stack = [s]
        visited[s] = True

        while stack:
            u = stack.pop()

            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0:  # Hay capacidad disponible
                    stack.append(v)
                    visited[v] = True
                    parent[v] = u

                    if v == t:  # Si hemos llegado al sumidero
                        return True
        return False

    def ford_fulkerson(self, source, sink):
        parent = [-1] * self.V  # Array para almacenar el camino
        max_flow = 0

        while self._dfs(source, sink, parent):
            # Encontrar la capacidad mínima a lo largo del camino encontrado
            path_flow = float('Inf')
            v = sink

            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = parent[v]

            # Actualizar las capacidades residuales de las aristas
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return max_flow

# Ejemplo de uso
if __name__ == "__main__":
    g = Graph(6)
    g.add_edge(0, 1, 16)
    g.add_edge(0, 2, 13)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 3, 12)
    g.add_edge(2, 1, 4)
    g.add_edge(2, 4, 14)
    g.add_edge(3, 2, 9)
    g.add_edge(3, 5, 20)
    g.add_edge(4, 3, 7)
    g.add_edge(4, 5, 4)

    source = 0
    sink = 5
    print("El flujo máximo es:", g.ford_fulkerson(source, sink))
