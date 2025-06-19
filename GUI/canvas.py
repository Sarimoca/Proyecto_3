import tkinter as tk
import time
from Utils.config import *
import random

class Canvas(tk.Canvas):
    def __init__(self, parent, simulation_core, **kwargs):
        super().__init__(parent, **kwargs)
        self.simulation_core = simulation_core
        self.vehicles = {}  # Diccionario de representaciones visuales de vehículos
        self.nodes = {}     # Diccionario de nodos dibujados
        self.edges = {}     # Diccionario de aristas dibujadas
        self.highlighted_route = None
        self.bind("<Button-1>", self.on_canvas_click)
    def draw_node(self, node):
        """Dibuja un nodo con efecto de confirmación"""
        x, y = node.x, node.y
        # Dibujar con color aleatorio
        node_color = self.rgb_to_hex((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        node_circle = self.create_oval(x-NODE_RADIUS, y-NODE_RADIUS,
                                     x+NODE_RADIUS, y+NODE_RADIUS,
                                     fill=node_color, outline="black", width=2)
        node_label = self.create_text(x, y+NODE_RADIUS+15, text=node.name, font=("Arial", 10))
        
        # Restaurar color después de 1 segundo
        #self.after(1000, lambda: self.itemconfig(node_circle, fill=NODE_COLOR))
        
        self.nodes[node.id] = (node_circle, node_label, node)
        
    def draw_edge(self, edge):
        """Dibuja una arista con efecto de confirmación"""
        source_node = self.simulation_core.graph.get_node(edge.source)
        target_node = self.simulation_core.graph.get_node(edge.target)
        if not source_node or not target_node:
            return
            
        x1, y1 = source_node.x, source_node.y
        x2, y2 = target_node.x, target_node.y
        
        # Dibujar con color verde 
        edge_line = self.create_line(x1, y1, x2, y2, fill="green", width=3, arrow=tk.LAST)
        
        # Efecto de parpadeo
        def blink():
            for _ in range(3):
                self.itemconfig(edge_line, dash=(4, 2))
                self.update()
                time.sleep(0.1)
                self.itemconfig(edge_line, dash="")
                self.update()
                time.sleep(0.1)
        
        self.after(100, blink)
        self.edges[edge.id] = (edge_line, None, edge)
        

        
    def update_edge(self, data):
        """Actualiza el estado de una arista (bloqueada o no)"""
        edge_id, blocked = data
        if edge_id in self.edges:
            edge_line, weight_label, edge = self.edges[edge_id]
            edge.blocked = blocked
            print(blocked)
            # Actualizar color
            color = "red" if blocked else "green"
            self.itemconfig(edge_line, fill=color)
            # Actualizar patrón de línea
            if blocked:
                self.itemconfig(edge_line, dash=(4, 2))
            else:
                self.itemconfig(edge_line, dash="")

        self.update()
        
    def add_vehicle(self, vehicle):
        """Añade un vehículo al canvas"""
        # Obtener nodo de inicio
        start_node = self.simulation_core.graph.get_node(vehicle.start)
        if not start_node:
            return
            
        x, y = start_node.x, start_node.y
        
        # Dibujar vehículo como un círculo pequeño
        vehicle_circle = self.create_oval(x - VEHICLE_RADIUS, y - VEHICLE_RADIUS,
                                         x + VEHICLE_RADIUS, y + VEHICLE_RADIUS,
                                         fill=self.rgb_to_hex(vehicle.color), outline="black")
        
        # Guardar referencia
        self.vehicles[vehicle.id] = (vehicle_circle, vehicle)
        
    def update_vehicles(self, _=None):
        """Actualiza la posición de todos los vehículos en el canvas"""
        for vehicle_id, (vehicle_circle, vehicle) in self.vehicles.items():
            # Obtener la arista actual del vehículo
            if vehicle.current_edge_index < len(vehicle.path):
                edge_id = vehicle.path[vehicle.current_edge_index]
                edge = self.simulation_core.graph.get_edge(edge_id)
                if not edge:
                    continue
                    
                source_node = self.simulation_core.graph.get_node(edge.source)
                target_node = self.simulation_core.graph.get_node(edge.target)
                if not source_node or not target_node:
                    continue
                    
                # Calcular posición interpolada
                x1, y1 = source_node.x, source_node.y
                x2, y2 = target_node.x, target_node.y
                x = x1 + (x2 - x1) * vehicle.progress
                y = y1 + (y2 - y1) * vehicle.progress
                
                # Actualizar posición del vehículo
                self.coords(vehicle_circle, 
                            x - VEHICLE_RADIUS, y - VEHICLE_RADIUS,
                            x + VEHICLE_RADIUS, y + VEHICLE_RADIUS)
        
    def highlight_vehicle_route(self, vehicle):
        """Resalta la ruta de un vehículo específico"""
        # Eliminar resaltado anterior si existe
        if self.highlighted_route:
            for line in self.highlighted_route:
                self.delete(line)
            self.highlighted_route = None
            
        # Resaltar nueva ruta
        highlighted = []
        for edge_id in vehicle.path:
            if edge_id in self.edges:
                edge_line, weight_label, edge = self.edges[edge_id]
                
                # Obtener coordenadas de la arista
                coords = self.coords(edge_line)
                if len(coords) >= 4:
                    # Dibujar una línea más gruesa encima
                    highlight = self.create_line(coords, fill="blue", width=4, dash=(2, 2))
                    highlighted.append(highlight)
        
        self.highlighted_route = highlighted
        
    def on_canvas_click(self, event):
        """Maneja clics en el canvas"""
        # Buscar vehículo cerca del punto de clic
        closest_vehicle = None
        min_distance = float('inf')
        
        for vehicle_id, (vehicle_circle, vehicle) in self.vehicles.items():
            coords = self.coords(vehicle_circle)
            if len(coords) >= 2:
                x = (coords[0] + coords[2]) / 2
                y = (coords[1] + coords[3]) / 2
                distance = ((event.x - x) ** 2 + (event.y - y) ** 2) ** 0.5
                
                if distance < min_distance and distance < 20:  # Radio de selección
                    min_distance = distance
                    closest_vehicle = vehicle
        
        # Si encontramos un vehículo, resaltar su ruta
        if closest_vehicle:
            self.simulation_core.event_manager.notify("vehicle_selected", closest_vehicle)
    
    def rgb_to_hex(self, rgb):
        """Convierte un color RGB a formato hexadecimal para tkinter"""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'