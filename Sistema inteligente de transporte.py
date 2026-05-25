import heapq
import math
from datetime import datetime

# Reglas lógicas

# Regla 1: Nombres y coordenadas de las estaciones
estaciones = {
    "Portal Norte": (4.80, -74.05),
    "Calle 100": (4.76, -74.05),
    "Calle 72": (4.69, -74.05),
    "Calle 26": (4.66, -74.05),
    "Avenida Jiménez": (4.68, -74.07),
    "Portal Sur": (4.53, -74.12),
}

# Regla 2: Conexiones entre estaciones
conexiones = [
    ("Portal Norte", "Calle 100", 8),
    ("Calle 100", "Calle 72", 6),
    ("Calle 72", "Calle 26", 5),
    ("Calle 26", "Portal Sur", 12),
    ("Calle 72", "Avenida Jiménez", 4),
    ("Avenida Jiménez", "Calle 26", 7),
]

# Regla 3: Rutas bidireccionales (grafo)
grafo = {}
for origen, destino, peso in conexiones:
    if origen not in grafo:
        grafo[origen] = []
    if destino not in grafo:
        grafo[destino] = []
    grafo[origen].append((destino, peso))
    grafo[destino].append((origen, peso))

# FUNCIÓN HEURÍSTICA 
# Regla 4: estimación optimista

def distancia_km(coord1, coord2):
    """Distancia euclidiana aproximada en km"""
    return math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2) * 100

def heuristica(estacion_actual, estacion_objetivo):
    """Regla 5: Heurística = distancia/velocidad (vel=30km/h = 2min/km)"""
    dist = distancia_km(estaciones[estacion_actual], estaciones[estacion_objetivo])
    return dist / 1000 * 2  # minutos

# ALGORITMO A* 
# Regla 6: búsqueda informada

def a_estrella(inicio, objetivo):
    open_set = []
    heapq.heappush(open_set, (0 + heuristica(inicio, objetivo), 0, inicio, [inicio]))
    visitados = set()
    
    while open_set:
        f_actual, costo_actual, nodo_actual, path = heapq.heappop(open_set)
        
        if nodo_actual == objetivo:
            return path, costo_actual
        
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)
        
        for vecino, costo in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                nuevo_costo = costo_actual + costo
                nuevo_f = nuevo_costo + heuristica(vecino, objetivo)
                heapq.heappush(open_set, (nuevo_f, nuevo_costo, vecino, path + [vecino]))
    
    return None, float('inf')

# SISTEMA INTELIGENTE 

def mostrar_reglas():
    print("\n📜 BASE DE CONOCIMIENTO (Reglas lógicas):")
    print("1. Si existe conexion(origen, destino, tiempo) entonces se puede viajar")
    print("2. Las rutas son bidireccionales (se puede ir y venir)")
    print("3. Cada estación es un nodo en el grafo")
    print("4. El costo es el tiempo en minutos")
    print("5. La heurística estima tiempo restante (distancia/velocidad)")
    print("6. Se usa A* para minimizar f(n)=g(n)+h(n)")
    print("7. A* garantiza ruta óptima si h(n) es admisible")

def encontrar_ruta(origen, destino):
    print(f"\n{'='*50}")
    print(f"🔍 BUSCANDO RUTA: {origen} → {destino}")
    print(f"{'='*50}")
    
    if origen not in grafo or destino not in grafo:
        print("❌ Error: Estación no existe en la base de conocimiento")
        return None, None
    
    ruta, tiempo = a_estrella(origen, destino)
    
    if ruta:
        print(f"\n✅ Ruta encontrada:")
        for i, estacion in enumerate(ruta, 1):
            print(f"   {i}. {estacion}")
        print(f"⏱️  Tiempo total: {tiempo} minutos")
        
        # Mostrar reglas aplicadas
        print(f"\n🧠 Reglas aplicadas en esta búsqueda:")
        print(f"   - Regla 1: Se verificaron conexiones en el grafo")
        print(f"   - Regla 2: Se permitió movimiento bidireccional")
        print(f"   - Regla 5: Se usó heurística para priorizar nodos")
        print(f"   - Regla 6: Se minimizó f(n) = g(n) + h(n)")
    else:
        print("❌ No existe ruta entre las estaciones")
    
    return ruta, tiempo


# EJECUCIÓN PRINCIPAL 

if __name__ == "__main__":
    print("="*50)
    print("SISTEMA INTELIGENTE DE TRANSPORTE")
    print(f"Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Mostrar todas las reglas
    mostrar_reglas()
    
    # Prueba 1
    encontrar_ruta("Portal Norte", "Portal Sur")
    
    # Prueba 2
    encontrar_ruta("Calle 100", "Avenida Jiménez")
    
    # Prueba 3
    encontrar_ruta("Calle 72", "Portal Norte")
    
    print("\n" + "="*50)
    print("FIN DE LA EJECUCIÓN")
    print("="*50)