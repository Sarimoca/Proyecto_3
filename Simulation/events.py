class EventManager:
    def __init__(self):
        self.subscribers = {}
        
    def subscribe(self, event_type, callback):
        """Registra un callback para un tipo de evento"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        
    def unsubscribe(self, event_type, callback):
        """Elimina un callback de un tipo de evento"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
            
    def notify(self, event_type, data=None):
        """Notifica a todos los suscriptores de un evento"""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)