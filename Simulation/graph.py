from Utils.custom_structures import CustomDictionary, CustomList

class Node:
    def __init__(self, id, name, x, y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.traffic = 0  # Nueva propiedad para tráfico acumulado
        
    def __str__(self):
        return f"{self.name} ({self.x},{self.y})"

class Edge:
    def __init__(self, id, source, target, weight):
        self.id = id
        self.source = source
        self.target = target
        self.weight = weight
        self.traffic_load = 0  # Carga vehicular
        self.blocked = False   # Estado de bloqueo
        
    def __str__(self):
        status = "BLOQUEADA" if self.blocked else "Activa"
        return f"{self.source} → {self.target} ({self.weight} km) [{status}]"

class Graph:
    def __init__(self):
        self.nodes = CustomDictionary()
        self.edges = CustomDictionary()
        self.adjacency = CustomDictionary()  # Para almacenar relaciones nodo->vecinos
        
    def add_node(self, node):
        self.nodes[node.id] = node
        self.adjacency[node.id] = CustomList()
        
    def add_edge(self, edge_id, edge):
        self.edges[edge_id] = edge
        
        # Actualizar lista de adyacencia
        if edge.source in self.adjacency:
            self.adjacency[edge.source].append(edge.target)
        else:
            self.adjacency[edge.source] = CustomList([edge.target])
            
    def get_node(self, node_id):
        return self.nodes.get(node_id)
        
    def get_edge(self, edge_id):
        return self.edges.get(edge_id)
        
    def get_node_ids(self):
        return self.nodes.keys()
        
    def get_edge_ids(self):
        return self.edges.keys()
        
    def get_neighbors(self, node_id):
        return self.adjacency.get(node_id, CustomList())
        
    def get_edge_between(self, source_id, target_id):
        """Obtiene la arista entre dos nodos (si existe)"""
        for edge_id, edge in self.edges.items():
            if edge.source == source_id and edge.target == target_id:
                return edge
        return None
        
    def update_traffic_load(self, edge_id, delta):
        """Actualiza la carga vehicular de una arista"""
        edge = self.get_edge(edge_id)
        if edge:
            edge.traffic_load = max(0, edge.traffic_load + delta)