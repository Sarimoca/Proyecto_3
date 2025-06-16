from Simulation.core import SimulationCore
from GUI.main_window import MainWindow

def main():
    # Crear núcleo de simulación
    core = SimulationCore()
    
    # Crear y ejecutar ventana principal
    app = MainWindow(core)
    app.run()

if __name__ == "__main__":
    main()