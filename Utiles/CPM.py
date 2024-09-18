from collections import defaultdict

class Project:
    def __init__(self):
        self.graph = defaultdict(list)  # Grafo de actividades
        self.durations = {}  # Duración de cada actividad

    def add_activity(self, activity, duration):
        self.durations[activity] = duration

    def add_dependency(self, u, v):
        self.graph[u].append(v)  # Agrega dependencia

    def critical_path_util(self, u, visited, stack):
        visited[u] = True
        for v in self.graph[u]:
            if not visited[v]:
                self.critical_path_util(v, visited, stack)
        stack.append(u)

    def critical_path(self):
        stack = []
        visited = {activity: False for activity in self.durations}

        # Paso 1: Llenar el stack con el orden topológico
        for activity in self.durations:
            if not visited[activity]:
                self.critical_path_util(activity, visited, stack)

        # Paso 2: Calcular la duración más larga en el camino crítico
        max_duration = 0
        critical_activities = []

        while stack:
            activity = stack.pop()
            if activity in self.durations:
                current_duration = self.durations[activity]
                if current_duration > max_duration:
                    max_duration = current_duration
                    critical_activities = [activity]
                elif current_duration == max_duration:
                    critical_activities.append(activity)

        return max_duration, critical_activities

# Ejemplo de uso
if __name__ == "__main__":
    project = Project()
    project.add_activity('A', 3)
    project.add_activity('B', 2)
    project.add_activity('C', 5)
    project.add_activity('D', 1)
    project.add_activity('E', 4)

    project.add_dependency('A', 'B')
    project.add_dependency('A', 'C')
    project.add_dependency('B', 'D')
    project.add_dependency('C', 'D')
    project.add_dependency('D', 'E')

    duration, critical_activities = project.critical_path()
    print(f"Duración del camino crítico: {duration}")
    print(f"Actividades en el camino crítico: {critical_activities}")
