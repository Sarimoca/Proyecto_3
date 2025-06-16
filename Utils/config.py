# Configuración de la aplicación
DEBUG_MODE = True  # Cambiar a False en producción

# Parámetros de simulación
DEFAULT_VEHICLE_SPEED = 60  # km/h
SIMULATION_UPDATE_INTERVAL = 0.1  # segundos
MAX_TRAFFIC_LOAD = 100  # Carga máxima de tráfico

# Colores para la representación visual
NODE_COLOR = (0, 0, 255)        # Azul para nodos
EDGE_COLOR = (100, 100, 100)    # Gris para aristas
BLOCKED_EDGE_COLOR = (255, 0, 0) # Rojo para rutas bloqueadas
VEHICLE_COLORS = [
    (255, 0, 0),    # Rojo
    (0, 0, 255),    # Azul
    (0, 255, 0),    # Verde
    (255, 255, 0),  # Amarillo
    (0, 255, 255),  # Cian
    (255, 0, 255),  # Magenta
]

# Configuración de la interfaz
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
NODE_RADIUS = 10
VEHICLE_RADIUS = 5