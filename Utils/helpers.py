import random
import string
import math

def generate_random_id(length=8):
    """Genera un ID aleatorio de longitud dada."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def euclidean_distance(x1, y1, x2, y2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def is_numeric(value):
    """Verifica si un valor es numérico (int o float)."""
    return isinstance(value, (int, float))

def calculate_edge_weight(node1, node2, traffic_load=0):
    """Calcula el peso de una arista considerando distancia y tráfico."""
    distance = euclidean_distance(node1.x, node1.y, node2.x, node2.y)
    return distance * (1 + traffic_load * 0.1)  # Aumento del 10% por unidad de tráfico