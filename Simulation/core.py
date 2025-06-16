import time
import random
from Utils.helpers import generate_random_id
from Utils.custom_structures import CustomList
from .graph import Graph, Node, Edge
from .vehicle import Vehicle
from .algorithms import ShortestPath, Recommendations
from .events import EventManager

class SimulationCore:
    def __init__(self):
        self.graph = Graph()
        self.vehicles = CustomList()
        self.speed_factor = 1.0
        self.time = 0
        self.running = False
        self.event_manager = EventManager()
        
    def add_node(self, name, x, y):
        """Agrega un nuevo nodo (ciudad/punto de interés) al grafo"""
        node_id = generate_random_id()
        node = Node(node_id, name, x, y)
        self.graph.add_node(node)
        self.event_manager.notify("node_added", node)
        return node_id
        
    def add_edge(self, source_id, target_id, weight, bidirectional=True):
        """Crea una nueva arista (carretera) entre dos nodos"""
        edge_id = generate_random_id()
        edge = Edge(edge_id, source_id, target_id, weight)
        self.graph.add_edge(edge_id, edge)
        
        # Si es bidireccional, crear la arista inversa
        if bidirectional:
            reverse_edge_id = generate_random_id()
            reverse_edge = Edge(reverse_edge_id, target_id, source_id, weight)
            self.graph.add_edge(reverse_edge_id, reverse_edge)
            
        self.event_manager.notify("edge_added", edge)
        return edge_id
        
    def generate_vehicles(self, count):
        """Genera vehículos con rutas aleatorias"""
        node_ids = self.graph.get_node_ids()
        if len(node_ids) < 2:
            return
            
        for i in range(count):
            start_id = node_ids[random.randint(0, len(node_ids)-1)]
            end_id = node_ids[random.randint(0, len(node_ids)-1)]
            while start_id == end_id:
                end_id = node_ids[random.randint(0, len(node_ids)-1)]
                
            vehicle = Vehicle(f"v{i+1}", start_id, end_id)
            vehicle.calculate_route(self.graph)
            self.vehicles.append(vehicle)
            self.event_manager.notify("vehicle_created", vehicle)
    
    def update_simulation(self, delta_time):
        """Actualiza el estado de la simulación"""
        if not self.running:
            return
            
        self.time += delta_time * self.speed_factor
        
        # Actualizar posición de los vehículos
        for vehicle in self.vehicles:
            vehicle.move(delta_time * self.speed_factor, self.graph)
            
        self.event_manager.notify("simulation_updated")
        
    def start_simulation(self):
        self.running = True
        self.event_manager.notify("simulation_started")
        
    def pause_simulation(self):
        self.running = False
        self.event_manager.notify("simulation_paused")
        
    def set_speed_factor(self, factor):
        self.speed_factor = max(0.1, min(factor, 10.0))
        self.event_manager.notify("speed_changed", self.speed_factor)
        
    def block_route(self, edge_id, blocked=True):
        """Bloquea/desbloquea una ruta y recalcula rutas afectadas"""
        edge = self.graph.get_edge(edge_id)
        if edge:
            # Solo notificar si cambia el estado
            if edge.blocked != blocked:
                edge.blocked = blocked
                
                # Recalcular rutas para vehículos afectados
                for vehicle in self.vehicles:
                    # Verificar si el vehículo está usando esta arista
                    if edge_id in vehicle.path:
                        # Guardar posición actual para mantener progreso
                        current_progress = vehicle.progress
                        current_index = vehicle.current_edge_index
                        
                        # Recalcular ruta desde el principio
                        vehicle.calculate_route(self.graph)
                        
                        # Intentar mantener posición similar en la nueva ruta
                        if vehicle.path:
                            # Mantener el índice actual si es posible
                            vehicle.current_edge_index = min(current_index, len(vehicle.path) - 1)
                            vehicle.progress = current_progress
                
                # Notificar sobre el cambio
                self.event_manager.notify("route_blocked", (edge_id, blocked))
            
    def get_vehicle_route(self, vehicle_id):
        """Obtiene la ruta de un vehículo específico"""
        for vehicle in self.vehicles:
            if vehicle.id == vehicle_id:
                return vehicle.path
        return None
        
    def get_critical_points(self):
        """Obtiene recomendaciones de puntos críticos"""
        return Recommendations.find_critical_points(self.graph)