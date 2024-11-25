import heapq

def dijkstra(grafo, inicio, destino):
    # Diccionario para almacenar las distancias mínimas desde el inicio a cada nodo
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0

    # Diccionario para rastrear el camino más corto
    padres = {nodo: None for nodo in grafo}

    # Cola de prioridad para procesar los nodos en orden de distancia
    cola = [(0, inicio)]  # (distancia_acumulada, nodo)

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si alcanzamos el nodo destino, no necesitamos continuar
        if nodo_actual == destino:
            break

        # Explorar vecinos
        for vecino, peso in grafo[nodo_actual]:
            distancia_nueva = distancia_actual + peso

            # Actualizar si encontramos un camino más corto
            if distancia_nueva < distancias[vecino]:
                distancias[vecino] = distancia_nueva
                padres[vecino] = nodo_actual
                heapq.heappush(cola, (distancia_nueva, vecino))

    # Reconstruir el camino más corto
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()

    return distancias[destino], camino

# Ejemplo de grafo: {nodo: [(vecino, peso)]}
grafo = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 6)],
    'C': [('A', 4), ('B', 2), ('D', 3)],
    'D': [('B', 6), ('C', 3)]
}

# Probar el algoritmo
origen = 'A'
destino = 'D'
costo, camino = dijkstra(grafo, origen, destino)

print(f"Costo mínimo desde {origen} hasta {destino}: {costo}")
print(f"Camino: {' -> '.join(camino)}")
