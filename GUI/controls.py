import tkinter as tk
from tkinter import ttk, messagebox
from Utils.config import *

class ControlPanel(tk.Frame):
    def __init__(self, parent, simulation_core, canvas):
        super().__init__(parent, bd=1, relief=tk.RAISED)
        self.simulation_core = simulation_core
        self.canvas = canvas
        self.parent = parent  # Guardar referencia al padre para la barra de estado
        # Mapeos para nombres a IDs
        self.node_name_to_id = {}
        self.edge_desc_to_id = {}
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        title = tk.Label(self, text="Controles de Simulación", font=("Arial", 12, "bold"))
        title.pack(pady=10)
        
        # Panel para agregar nodos
        node_frame = tk.LabelFrame(self, text="Agregar Nodo", padx=5, pady=5)
        node_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(node_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.node_name = tk.Entry(node_frame, width=15)
        self.node_name.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(node_frame, text="Posición X:").grid(row=1, column=0, sticky=tk.W)
        self.node_x = tk.Entry(node_frame, width=8)
        self.node_x.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(node_frame, text="Posición Y:").grid(row=2, column=0, sticky=tk.W)
        self.node_y = tk.Entry(node_frame, width=8)
        self.node_y.grid(row=2, column=1, padx=5, pady=2)
        
        btn_add_node = tk.Button(node_frame, text="Agregar Nodo", command=self.add_node)
        btn_add_node.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Panel para agregar aristas
        edge_frame = tk.LabelFrame(self, text="Agregar Arista", padx=5, pady=5)
        edge_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(edge_frame, text="Desde:").grid(row=0, column=0, sticky=tk.W)
        self.edge_from = ttk.Combobox(edge_frame, width=12)
        self.edge_from.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(edge_frame, text="Hacia:").grid(row=1, column=0, sticky=tk.W)
        self.edge_to = ttk.Combobox(edge_frame, width=12)
        self.edge_to.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(edge_frame, text="Distancia (km):").grid(row=2, column=0, sticky=tk.W)
        self.edge_weight = tk.Entry(edge_frame, width=8)
        self.edge_weight.grid(row=2, column=1, padx=5, pady=2)
        
        self.bidirectional = tk.BooleanVar(value=True)
        tk.Checkbutton(edge_frame, text="Bidireccional", variable=self.bidirectional).grid(row=3, column=0, columnspan=2)
        
        btn_add_edge = tk.Button(edge_frame, text="Agregar Arista", command=self.add_edge)
        btn_add_edge.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Panel para vehículos
        vehicle_frame = tk.LabelFrame(self, text="Vehículos", padx=5, pady=5)
        vehicle_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(vehicle_frame, text="Cantidad:").grid(row=0, column=0, sticky=tk.W)
        self.vehicle_count = tk.Scale(vehicle_frame, from_=1, to=50, orient=tk.HORIZONTAL, length=150)
        self.vehicle_count.set(10)
        self.vehicle_count.grid(row=0, column=1, padx=5, pady=2)
        
        btn_gen_vehicles = tk.Button(vehicle_frame, text="Generar Vehículos", command=self.generate_vehicles)
        btn_gen_vehicles.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Panel para control de simulación
        sim_frame = tk.LabelFrame(self, text="Control de Simulación", padx=5, pady=5)
        sim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(sim_frame, text="Velocidad:").grid(row=0, column=0, sticky=tk.W)
        self.speed_scale = tk.Scale(sim_frame, from_=0.1, to=5, resolution=0.1, 
                                   orient=tk.HORIZONTAL, length=150)
        self.speed_scale.set(1.0)
        self.speed_scale.grid(row=0, column=1, padx=5, pady=2)
        
        btn_frame = tk.Frame(sim_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.btn_start = tk.Button(btn_frame, text="Iniciar", width=8, command=self.start_simulation)
        self.btn_start.pack(side=tk.LEFT, padx=2)
        
        self.btn_pause = tk.Button(btn_frame, text="Pausar", width=8, command=self.pause_simulation, state=tk.DISABLED)
        self.btn_pause.pack(side=tk.LEFT, padx=2)
        
        # Panel para bloqueo de rutas
        block_frame = tk.LabelFrame(self, text="Bloquear Rutas", padx=5, pady=5)
        block_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(block_frame, text="Arista ID:").grid(row=0, column=0, sticky=tk.W)
        self.block_id = ttk.Combobox(block_frame, width=12)
        self.block_id.grid(row=0, column=1, padx=5, pady=2)
        
        btn_block = tk.Button(block_frame, text="Bloquear", command=lambda: self.block_route(True))
        btn_block.grid(row=1, column=0, pady=5)
        
        btn_unblock = tk.Button(block_frame, text="Desbloquear", command=lambda: self.block_route(False))
        btn_unblock.grid(row=1, column=1, pady=5)
        
        # Panel para recomendaciones
        rec_frame = tk.LabelFrame(self, text="Análisis", padx=5, pady=5)
        rec_frame.pack(fill=tk.X, padx=5, pady=5)
        
        btn_recommend = tk.Button(rec_frame, text="Mostrar Puntos Críticos", command=self.show_recommendations)
        btn_recommend.pack(pady=5)
        
        # Actualizar comboboxes
        self.update_comboboxes()
        
        # Suscribir a eventos para actualizar comboboxes
        self.simulation_core.event_manager.subscribe("node_added", self.update_comboboxes)
        self.simulation_core.event_manager.subscribe("edge_added", self.update_comboboxes)
        self.simulation_core.event_manager.subscribe("vehicle_selected", self.show_vehicle_info)
        
    def update_comboboxes(self, _=None):
        """Actualiza los comboboxes con nombres de nodos y descripciones de aristas"""
        # Limpiar mapeos anteriores
        self.node_name_to_id = {}
        self.edge_desc_to_id = {}
        
        # Para nodos: mostrar solo nombres
        node_options = []
        for node_id in self.simulation_core.graph.get_node_ids():
            node = self.simulation_core.graph.get_node(node_id)
            node_name = node.name
            node_options.append(node_name)
            self.node_name_to_id[node_name] = node_id
        
        # Para aristas: mostrar descripción (origen → destino)
        edge_options = []
        for edge_id in self.simulation_core.graph.get_edge_ids():
            edge = self.simulation_core.graph.get_edge(edge_id)
            source_name = self.simulation_core.graph.get_node(edge.source).name
            target_name = self.simulation_core.graph.get_node(edge.target).name
            edge_desc = f"{source_name} → {target_name}"
            edge_options.append(edge_desc)
            self.edge_desc_to_id[edge_desc] = edge_id
        
        # Actualizar comboboxes
        self.edge_from['values'] = node_options
        self.edge_to['values'] = node_options
        self.block_id['values'] = edge_options
        
    def add_node(self):
        """Agrega un nuevo nodo al grafo"""
        name = self.node_name.get()
        try:
            x = float(self.node_x.get())
            y = float(self.node_y.get())
        except ValueError:
            messagebox.showerror("Error", "Las coordenadas deben ser números válidos")
            return
            
        if not name:
            messagebox.showerror("Error", "Debe ingresar un nombre para el nodo")
            return
            
        node_id = self.simulation_core.add_node(name, x, y)
        messagebox.showinfo("Éxito", f"Nodo '{name}' creado en posición ({x}, {y})")
        self.parent.set_status(f"Nodo '{name}' agregado exitosamente")
        
        # Limpiar campos y enfocar el campo de nombre
        self.node_name.delete(0, tk.END)
        self.node_x.delete(0, tk.END)
        self.node_y.delete(0, tk.END)
        self.node_name.focus_set()
        
    def add_edge(self):
        """Agrega una nueva arista al grafo"""
        from_name = self.edge_from.get()
        to_name = self.edge_to.get()
        weight = self.edge_weight.get()
        
        if not from_name or not to_name:
            messagebox.showerror("Error", "Debe seleccionar nodos de origen y destino")
            return
            
        # Obtener IDs de los nombres
        if from_name not in self.node_name_to_id or to_name not in self.node_name_to_id:
            messagebox.showerror("Error", "Nodo no encontrado")
            return
            
        from_id = self.node_name_to_id[from_name]
        to_id = self.node_name_to_id[to_name]
        
        if from_id == to_id:
            messagebox.showerror("Error", "No puede conectar un nodo consigo mismo")
            return
            
        try:
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "La distancia debe ser un número válido")
            return
            
        self.simulation_core.add_edge(from_id, to_id, weight, self.bidirectional.get())
        messagebox.showinfo("Éxito", f"Carretera creada: {from_name} ↔ {to_name} ({weight} km)")
        self.parent.set_status(f"Carretera {from_name}-{to_name} añadida")
        
        # Limpiar campos y enfocar el campo 'Desde'
        self.edge_from.set('')
        self.edge_to.set('')
        self.edge_weight.delete(0, tk.END)
        self.edge_from.focus_set()
        
    def generate_vehicles(self):
        """Genera vehículos aleatorios"""
        count = self.vehicle_count.get()
        self.simulation_core.generate_vehicles(count)
        
    def start_simulation(self):
        """Inicia la simulación"""
        self.simulation_core.start_simulation()
        self.btn_start.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        
    def pause_simulation(self):
        """Pausa la simulación"""
        self.simulation_core.pause_simulation()
        self.btn_start.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        
    def set_speed(self):
        """Establece la velocidad de la simulación"""
        speed = self.speed_scale.get()
        self.simulation_core.set_speed_factor(speed)
        
    def block_route(self, blocked):
        """Bloquea o desbloquea una ruta usando la descripción de la arista"""
        edge_desc = self.block_id.get()
        if not edge_desc:
            return
            
        # Obtener ID de la arista a partir de la descripción
        if edge_desc not in self.edge_desc_to_id:
            messagebox.showerror("Error", "Arista no encontrada")
            return
            
        edge_id = self.edge_desc_to_id[edge_desc]
        
        # Obtener nombres para el mensaje
        edge = self.simulation_core.graph.get_edge(edge_id)
        if edge:
            source = self.simulation_core.graph.get_node(edge.source).name
            target = self.simulation_core.graph.get_node(edge.target).name
            
            self.simulation_core.block_route(edge_id, blocked)
            action = "bloqueada" if blocked else "desbloqueada"
            messagebox.showinfo("Éxito", f"Ruta {source} → {target} {action}")
            #self.parent.set_status(f"Ruta {source}-{target} {action}")
        
    def show_recommendations(self):
        """Muestra recomendaciones de puntos críticos"""
        critical_points = self.simulation_core.get_critical_points()
        
        # Crear ventana emergente
        popup = tk.Toplevel(self)
        popup.title("Puntos Críticos")
        popup.geometry("400x300")
        
        # Crear notebook (pestañas)
        notebook = ttk.Notebook(popup)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña para aristas con alto tráfico
        edges_frame = ttk.Frame(notebook)
        notebook.add(edges_frame, text="Aristas Congestionadas")
        
        tk.Label(edges_frame, text="Aristas con mayor carga vehicular:", font=("Arial", 10)).pack(pady=5)
        
        if critical_points["high_traffic_edges"]:
            for edge in critical_points["high_traffic_edges"]:
                source = self.simulation_core.graph.get_node(edge.source).name
                target = self.simulation_core.graph.get_node(edge.target).name
                tk.Label(edges_frame, text=f"{source} → {target}: {edge.traffic_load:.1f} vehículos").pack(anchor=tk.W)
        else:
            tk.Label(edges_frame, text="No hay datos disponibles").pack()
        
        # Pestaña para nodos con alta conectividad
        nodes_frame = ttk.Frame(notebook)
        notebook.add(nodes_frame, text="Nodos Importantes")
        
        tk.Label(nodes_frame, text="Nodos con mayor tráfico acumulado:", font=("Arial", 10)).pack(pady=5)
        
        if critical_points["high_traffic_nodes"]:
            for node in critical_points["high_traffic_nodes"]:
                tk.Label(nodes_frame, text=f"{node.name}: {node.traffic:.1f} vehículos").pack(anchor=tk.W)
        else:
            tk.Label(nodes_frame, text="No hay datos disponibles").pack()
            
        # Botón para cerrar
        btn_close = tk.Button(popup, text="Cerrar", command=popup.destroy)
        btn_close.pack(pady=10)
        
    def show_vehicle_info(self, vehicle):
        """Muestra información sobre un vehículo seleccionado"""
        # Crear ventana emergente
        popup = tk.Toplevel(self)
        popup.title(f"Información del Vehículo {vehicle.id}")
        popup.geometry("300x200")
        
        # Obtener nombres de nodos
        start_node = self.simulation_core.graph.get_node(vehicle.start).name
        end_node = self.simulation_core.graph.get_node(vehicle.end).name
        
        # Mostrar información
        tk.Label(popup, text=f"Vehículo: {vehicle.id}", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(popup, text=f"Origen: {start_node}").pack(anchor=tk.W, padx=20)
        tk.Label(popup, text=f"Destino: {end_node}").pack(anchor=tk.W, padx=20)
        tk.Label(popup, text=f"Velocidad: {vehicle.speed:.1f} km/h").pack(anchor=tk.W, padx=20)
        tk.Label(popup, text=f"Ruta: {len(vehicle.path)} segmentos").pack(anchor=tk.W, padx=20)
        
        # Botón para mostrar ruta
        btn_show_route = tk.Button(popup, text="Mostrar Ruta", 
                                  command=lambda: self.canvas.highlight_vehicle_route(vehicle))
        btn_show_route.pack(pady=10)
        
        # Botón para cerrar
        btn_close = tk.Button(popup, text="Cerrar", command=popup.destroy)
        btn_close.pack()