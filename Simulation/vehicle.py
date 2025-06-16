import random
from Utils.custom_structures import CustomList
from .algorithms import ShortestPath

class Vehicle:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.path = CustomList()  # Lista de edge IDs
        self.current_edge_index = 0
        self.progress = 0.0  # Progreso en la arista actual (0-1)
        self.speed = random.uniform(40, 80)  # km/h
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    def calculate_route(self, graph):
        """Calcula la ruta más corta usando Dijkstra"""
        self.path = ShortestPath.dijkstra(graph, self.start, self.end)
        self.current_edge_index = 0
        self.progress = 0.0
        
    def move(self, delta_time, graph):
        """Mueve el vehículo actualizando la carga vehicular"""
        if len(self.path) == 0 or self.current_edge_index >= len(self.path):
            return
            
        current_edge_id = self.path[self.current_edge_index]
        edge = graph.get_edge(current_edge_id)
        
        if not edge or edge.blocked:
            # Si estaba en esta arista, reducir carga
            if self.current_edge_index < len(self.path):
                current_edge = graph.get_edge(current_edge_id)
                if current_edge and current_edge.traffic_load > 0:
                    current_edge.traffic_load -= 1
            self.calculate_route(graph)
            return
            
        # Si acaba de entrar en esta arista, aumentar carga
        if self.progress == 0.0:
            edge.traffic_load += 1
            
        # Calcular distancia a recorrer
        distance_km = self.speed * (delta_time / 3600)
        edge_length = edge.weight
        
        # Actualizar progreso
        self.progress += distance_km / edge_length
        
        # Si completamos esta arista, pasar a la siguiente
        if self.progress >= 1.0:
            # Reducir carga de la arista que estamos dejando
            edge.traffic_load -= 1
            
            self.current_edge_index += 1
            self.progress = 0.0
            
            if self.current_edge_index >= len(self.path):
                self.current_edge_index = 0
                self.progress = 0.0