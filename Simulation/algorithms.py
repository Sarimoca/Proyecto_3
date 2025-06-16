from Utils.custom_structures import PriorityQueue, CustomDictionary, CustomList

class ShortestPath:
    @staticmethod
    def dijkstra(graph, start, end):
        """Calcula la ruta más corta usando el algoritmo de Dijkstra"""
        # Inicializar estructuras
        distances = CustomDictionary()
        previous = CustomDictionary()
        queue = PriorityQueue()
        
        # Inicializar distancias
        for node_id in graph.get_node_ids():
            distances[node_id] = float('inf')
            previous[node_id] = None
        distances[start] = 0
        
        queue.put(start, 0)
        
        while not queue.empty():
            current = queue.get()
            
            if current == end:
                break
                
            neighbors = graph.get_neighbors(current)
            for neighbor in neighbors:
                edge = graph.get_edge_between(current, neighbor)
                if not edge or edge.blocked:
                    continue
                    
                # Calcular peso considerando tráfico
                weight = edge.weight * (1 + edge.traffic_load * 0.1)
                alt = distances[current] + weight
                
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = (current, edge.id)
                    queue.put(neighbor, alt)
        
        # Reconstruir ruta
        path = CustomList()
        current = end
        while current != start:
            if current not in previous or previous[current] is None:
                return CustomList()  # No hay ruta
                
            current, edge_id = previous[current]
            path.insert(0, edge_id)  # Añadir al inicio
            
        return path

class Recommendations:
    @staticmethod
    def find_critical_points(graph):
        """Identifica puntos críticos con carga vehicular real"""
        # 1. Aristas con mayor carga vehicular
        all_edges = []
        for edge_id in graph.get_edge_ids():
            edge = graph.get_edge(edge_id)
            all_edges.append(edge)
        
        # Ordenar por carga vehicular (de mayor a menor)
        all_edges.sort(key=lambda e: e.traffic_load, reverse=True)
        
        # Tomar las top 3
        critical_edges = all_edges[:3] if len(all_edges) > 3 else all_edges
        
        # 2. Nodos con mayor tráfico acumulado
        node_traffic = {}
        for edge in all_edges:
            # Sumar tráfico de la arista a los nodos de origen y destino
            node_traffic[edge.source] = node_traffic.get(edge.source, 0) + edge.traffic_load
            node_traffic[edge.target] = node_traffic.get(edge.target, 0) + edge.traffic_load
        
        # Encontrar nodos con mayor tráfico acumulado
        critical_nodes = []
        if node_traffic:
            max_traffic = max(node_traffic.values())
            for node_id, traffic in node_traffic.items():
                if traffic == max_traffic:
                    node = graph.get_node(node_id)
                    if node:
                        # Guardar el tráfico en el nodo para mostrarlo
                        node.traffic = traffic
                        critical_nodes.append(node)
        
        return {
            "high_traffic_edges": critical_edges,
            "high_traffic_nodes": critical_nodes
        }