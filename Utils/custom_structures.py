class CustomList:
    """Implementación personalizada de una lista dinámica."""
    def __init__(self, initial_data=None):
        self._data = []
        if initial_data is not None:
            self._data = list(initial_data)
    
    def __repr__(self):
        return f"CustomList({self._data})"
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = value
    
    def __delitem__(self, index):
        del self._data[index]
    
    def __iter__(self):
        return iter(self._data)
    
    def append(self, item):
        self._data.append(item)
    
    def insert(self, index, item):
        self._data.insert(index, item)
    
    def remove(self, item):
        self._data.remove(item)
    
    def pop(self, index=-1):
        return self._data.pop(index)
    
    def index(self, item):
        return self._data.index(item)
    
    def clear(self):
        self._data.clear()
    
    def count(self, item):
        return self._data.count(item)
    
    def sort(self, key=None, reverse=False):
        self._data.sort(key=key, reverse=reverse)
    
    def reverse(self):
        self._data.reverse()
    
    def extend(self, other):
        if isinstance(other, CustomList):
            self._data.extend(other._data)
        else:
            self._data.extend(other)
    
    def __contains__(self, item):
        return item in self._data

class CustomDictionary:
    """Implementación personalizada de un diccionario (hash map)."""
    def __init__(self, initial_dict=None):
        self._keys = []
        self._values = []
        if initial_dict is not None:
            for key, value in initial_dict.items():
                self[key] = value
    
    def __repr__(self):
        items = [f"{key}: {value}" for key, value in self.items()]
        return f"CustomDictionary({{{', '.join(items)}}})"
    
    def __len__(self):
        return len(self._keys)
    
    def __getitem__(self, key):
        try:
            index = self._keys.index(key)
            return self._values[index]
        except ValueError:
            raise KeyError(key)
    
    def __setitem__(self, key, value):
        try:
            index = self._keys.index(key)
            self._values[index] = value
        except ValueError:
            self._keys.append(key)
            self._values.append(value)
    
    def __delitem__(self, key):
        try:
            index = self._keys.index(key)
            del self._keys[index]
            del self._values[index]
        except ValueError:
            raise KeyError(key)
    
    def __contains__(self, key):
        return key in self._keys
    
    def keys(self):
        return self._keys.copy()
    
    def values(self):
        return self._values.copy()
    
    def items(self):
        return [(k, v) for k, v in zip(self._keys, self._values)]
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def pop(self, key, default=None):
        try:
            index = self._keys.index(key)
            value = self._values[index]
            del self._keys[index]
            del self._values[index]
            return value
        except ValueError:
            if default is not None:
                return default
            raise KeyError(key)
    
    def clear(self):
        self._keys.clear()
        self._values.clear()
    
    def update(self, other):
        if isinstance(other, CustomDictionary):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

class PriorityQueue:
    """Implementación de una cola de prioridad mínima usando un heap."""
    def __init__(self):
        self._heap = []
        self._index = 0  # Para evitar comparaciones de tuplas cuando las prioridades son iguales
    
    def __repr__(self):
        return f"PriorityQueue({self._heap})"
    
    def __len__(self):
        return len(self._heap)
    
    def empty(self):
        return len(self._heap) == 0
    
    def put(self, item, priority):
        """Añade un elemento a la cola con una prioridad dada."""
        # Usamos un triple: (prioridad, índice, item) para evitar comparar los items directamente
        entry = (priority, self._index, item)
        self._heap.append(entry)
        self._index += 1
        self._sift_up(len(self._heap) - 1)
    
    def get(self):
        """Elimina y devuelve el elemento con la prioridad más baja."""
        if len(self._heap) == 0:
            raise IndexError("get from empty PriorityQueue")
        # Mover el último elemento a la raíz y luego hacer sift down
        last = self._heap.pop()
        if self._heap:
            root = self._heap[0]
            self._heap[0] = last
            self._sift_down(0)
            return root[2]  # Devolver el item
        return last[2]
    
    def _sift_up(self, index):
        """Mueve el elemento en el índice hacia arriba para mantener la propiedad del heap."""
        parent = (index - 1) // 2
        while index > 0 and self._heap[index][0] < self._heap[parent][0]:
            self._heap[index], self._heap[parent] = self._heap[parent], self._heap[index]
            index = parent
            parent = (index - 1) // 2
    
    def _sift_down(self, index):
        """Mueve el elemento en el índice hacia abajo para mantener la propiedad del heap."""
        size = len(self._heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            
            if left < size and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < size and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right
            
            if smallest == index:
                break
                
            self._heap[index], self._heap[smallest] = self._heap[smallest], self._heap[index]
            index = smallest