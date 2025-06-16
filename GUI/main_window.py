import tkinter as tk
from .canvas import Canvas
from .controls import ControlPanel

class MainWindow(tk.Tk):
    def __init__(self, simulation_core):
        super().__init__()
        self.title("Traffic Simulator")
        self.geometry("1200x800")
        self.simulation_core = simulation_core
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self, textvariable=self.status_var, 
                                 bd=1, relief=tk.SUNKEN, anchor=tk.W)
        
        self.setup_ui()
        self.setup_event_listeners()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas
        self.canvas = Canvas(main_frame, self.simulation_core, width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Panel de control
        self.control_panel = ControlPanel(main_frame, self.simulation_core, self.canvas)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Barra de estado
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_status(self, message, duration=3000):
        """Actualiza la barra de estado temporalmente"""
        self.status_var.set(message)
        if duration > 0:
            self.after(duration, lambda: self.status_var.set(""))
        
    def setup_event_listeners(self):
        # Suscribir a eventos de la simulación
        self.simulation_core.event_manager.subscribe("node_added", self.canvas.draw_node)
        self.simulation_core.event_manager.subscribe("edge_added", self.canvas.draw_edge)
        self.simulation_core.event_manager.subscribe("vehicle_created", self.canvas.add_vehicle)
        self.simulation_core.event_manager.subscribe("simulation_updated", self.canvas.update_vehicles)
        self.simulation_core.event_manager.subscribe("route_blocked", self.canvas.update_edge)
        self.simulation_core.event_manager.subscribe("vehicle_route_updated", self.canvas.highlight_vehicle_route)
        
    def run(self):
        # Iniciar el loop de actualización de la simulación
        self.update_simulation()
        self.mainloop()
        
    def update_simulation(self):
        if self.simulation_core.running:
            self.simulation_core.update_simulation(0.1)  # Actualizar cada 100 ms
        
        # Programar la próxima actualización
        self.after(100, self.update_simulation)