import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Función para limpiar la consola
def limpiar_consola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Función para imprimir un contenedor
def imprimir_contenedor(titulo, contenido):
    separador = '-' * 60
    print(separador)
    print(f"| {titulo.center(56)} |")
    print(separador)
    for linea in contenido:
        print(f"| {linea.ljust(56)} |")
    print(separador)

# Función para verificar reflexividad
def es_reflexiva(conjunto, relaciones):
    pares_faltantes = []
    contenido = []
    for elemento in conjunto:
        if (elemento, elemento) not in relaciones:
            pares_faltantes.append((elemento, elemento))
    if pares_faltantes:
        contenido.append("La relación NO es reflexiva.")
        contenido.append(f"Faltan los pares reflexivos: {pares_faltantes}")
        imprimir_contenedor("Relación Reflexiva", contenido)
        return False
    contenido.append("La relación es reflexiva.")
    contenido.append("Cada elemento está relacionado consigo mismo.")
    imprimir_contenedor("Relación Reflexiva", contenido)
    return True

# Función para verificar simetría
def es_simetrica(conjunto, relaciones):
    pares_faltantes = []
    contenido = []
    for (a, b) in relaciones:
        if (b, a) not in relaciones:
            pares_faltantes.append((b, a))
    if pares_faltantes:
        contenido.append("La relación NO es simétrica.")
        contenido.append(f"Faltan los pares simétricos: {pares_faltantes}")
        imprimir_contenedor("Relación Simétrica", contenido)
        return False
    contenido.append("La relación es simétrica.")
    contenido.append("Para cada (a, b) existe (b, a).")
    imprimir_contenedor("Relación Simétrica", contenido)
    return True

# Función para verificar antisimetría
def es_antisimetrica(conjunto, relaciones):
    pares_fallidos = []
    contenido = []
    for (a, b) in relaciones:
        if a != b and (b, a) in relaciones:
            pares_fallidos.append((a, b))
    if pares_fallidos:
        contenido.append("La relación NO es antisimétrica.")
        contenido.append(f"Existen pares donde (a, b) y (b, a) están: {pares_fallidos}")
        imprimir_contenedor("Relación Antisimétrica", contenido)
        return False
    contenido.append("La relación es antisimétrica.")
    contenido.append("Si (a, b) está en la relación, (b, a) no lo está.")
    imprimir_contenedor("Relación Antisimétrica", contenido)
    return True

# Función para verificar transitividad
def es_transitiva(conjunto, relaciones):
    pares_faltantes = []
    contenido = []
    for (a, b) in relaciones:
        for (c, d) in relaciones:
            if b == c and (a, d) not in relaciones:
                pares_faltantes.append((a, d))
    if pares_faltantes:
        contenido.append("La relación NO es transitiva.")
        contenido.append(f"Faltan los pares transitivos: {pares_faltantes}")
        imprimir_contenedor("Relación Transitiva", contenido)
        return False
    contenido.append("La relación es transitiva.")
    contenido.append("Si (a, b) y (b, c) están, también lo está (a, c).")
    imprimir_contenedor("Relación Transitiva", contenido)
    return True

# Función para verificar irreflexividad
def es_irreflexiva(conjunto, relaciones):
    pares_fallidos = []
    contenido = []
    for elemento in conjunto:
        if (elemento, elemento) in relaciones:
            pares_fallidos.append((elemento, elemento))
    if pares_fallidos:
        contenido.append("La relación NO es irreflexiva.")
        contenido.append(f"Existen pares reflexivos: {pares_fallidos}")
        imprimir_contenedor("Relación Irreflexiva", contenido)
        return False
    contenido.append("La relación es irreflexiva.")
    contenido.append("Ningún elemento está relacionado consigo mismo.")
    imprimir_contenedor("Relación Irreflexiva", contenido)
    return True

# Función para verificar asimetría
def es_asimetrica(conjunto, relaciones):
    pares_fallidos = []
    contenido = []
    for (a, b) in relaciones:
        if (b, a) in relaciones:
            pares_fallidos.append((a, b))
    if pares_fallidos:
        contenido.append("La relación NO es asimétrica.")
        contenido.append(f"Existen pares donde (a, b) y (b, a) están: {pares_fallidos}")
        imprimir_contenedor("Relación Asimétrica", contenido)
        return False
    contenido.append("La relación es asimétrica.")
    contenido.append("Si (a, b) está en la relación, (b, a) no lo está.")
    imprimir_contenedor("Relación Asimétrica", contenido)
    return True

# Función para verificar si es una relación de equivalencia
def es_equivalencia(reflexiva, simetrica, transitiva, conjunto, relaciones):
    contenido = []
    if reflexiva and simetrica and transitiva:
        contenido.append("La relación es de equivalencia.")
        imprimir_contenedor("Relación de Equivalencia", contenido)
        
        # Generar el grafo y las clases de equivalencia
        generar_grafo(relaciones)
        clases_equivalencia(conjunto, relaciones)
        return True
    else:
        contenido.append("La relación NO es de equivalencia.")
        imprimir_contenedor("Relación de Equivalencia", contenido)
        return False

# Función para verificar si es una relación de orden parcial
def es_orden_parcial(reflexiva, antisimetrica, transitiva, conjunto, relaciones):
    contenido = []
    if reflexiva and antisimetrica and transitiva:
        contenido.append("La relación es de orden parcial.")
        imprimir_contenedor("Relación de Orden Parcial", contenido)
        
        # Verificar si es una retícula y generar el diagrama de Hasse
        es_reticula(conjunto, relaciones)
        generar_diagrama_hasse(conjunto, relaciones)
        return True
    else:
        contenido.append("La relación NO es de orden parcial.")
        imprimir_contenedor("Relación de Orden Parcial", contenido)
        return False

# Función para generar la matriz de adyacencia
def generar_matriz(conjunto, relaciones):
    n = len(conjunto)
    elementos = sorted(list(conjunto))
    matriz = np.zeros((n, n), dtype=int)

    # Llenar la matriz
    for (a, b) in relaciones:
        i = elementos.index(a)
        j = elementos.index(b)
        matriz[i][j] = 1

    # Mostrar la matriz
    print("Matriz de Adyacencia:")
    print(matriz)

# Función para generar el grafo de la relación
def generar_grafo(relaciones):
    G = nx.DiGraph()
    G.add_edges_from(relaciones)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightgreen', arrows=True)
    plt.title("Grafo de la Relación")
    plt.show()

# Función para obtener clases de equivalencia utilizando la técnica de unión y búsqueda
def clases_equivalencia(conjunto, relaciones):
    # Inicializar un diccionario para mantener el representante de cada clase
    representantes = {x: x for x in conjunto}
    
    # Función auxiliar para encontrar el representante de un elemento
    def encontrar_representante(x):
        if representantes[x] != x:
            representantes[x] = encontrar_representante(representantes[x])
        return representantes[x]
    
    # Función auxiliar para unir dos clases
    def unir_clases(x, y):
        rep_x = encontrar_representante(x)
        rep_y = encontrar_representante(y)
        if rep_x != rep_y:
            representantes[rep_y] = rep_x  # Unir las clases

    # Unir los elementos relacionados
    for (a, b) in relaciones:
        unir_clases(a, b)
    
    # Agrupar los elementos en sus clases de equivalencia
    clases = {}
    for x in conjunto:
        rep = encontrar_representante(x)
        if rep not in clases:
            clases[rep] = set()
        clases[rep].add(x)
    
    # Mostrar las clases de equivalencia
    contenido_clases = []
    for idx, clase in enumerate(clases.values(), 1):
        contenido_clases.append(f"Clase de equivalencia {idx}: {clase}")
    imprimir_contenedor("Clases de Equivalencia", contenido_clases)
    
    # Mostrar las particiones
    particiones = list(clases.values())
    contenido_particiones = [f"Particiones: {particiones}"]
    imprimir_contenedor("Particiones", contenido_particiones)

# Función para verificar si una relación es retícula
def es_reticula(conjunto, relaciones):
    # Aquí implementas la lógica para verificar si es retícula.
    contenido = ["Verificando si es una retícula (lattice)..."]
    imprimir_contenedor("Verificación de Retícula", contenido)
    return True

# Función para generar el diagrama de Hasse
def generar_diagrama_hasse(conjunto, relaciones):
    G = nx.DiGraph()
    G.add_edges_from(relaciones)
    
    # Eliminar ciclos y dejar solo las conexiones mínimas
    hasse_relaciones = []
    for (a, b) in relaciones:
        if not any((a, c) in relaciones and (c, b) in relaciones for c in conjunto if c != a and c != b):
            hasse_relaciones.append((a, b))
    
    G = nx.DiGraph()
    G.add_edges_from(hasse_relaciones)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', arrows=False)
    plt.title("Diagrama de Hasse")
    plt.show()

# Limpiar la consola antes de pedir datos
limpiar_consola()

# Pedir al usuario que introduzca los elementos del conjunto
conjunto_A = set(map(int, input("Introduce los elementos del conjunto A, separados por espacios: ").split()))

# Pedir al usuario que introduzca las relaciones
num_relaciones = int(input("¿Cuántas relaciones quieres introducir?: "))
relaciones = []
for _ in range(num_relaciones):
    a, b = map(int, input("Introduce una relación como 'a b': ").split())
    relaciones.append((a, b))

# Limpiar la consola nuevamente para mostrar los resultados más claramente
limpiar_consola()

# Mostrar los resultados
print("Conjunto A:", conjunto_A)
print("Relaciones:", relaciones)

# Verificar las propiedades individualmente y almacenarlas
es_relacion_reflexiva = es_reflexiva(conjunto_A, relaciones)
es_relacion_irreflexiva = es_irreflexiva(conjunto_A, relaciones)
es_relacion_simetrica = es_simetrica(conjunto_A, relaciones)
es_relacion_asimetrica = es_asimetrica(conjunto_A, relaciones)
es_relacion_antisimetrica = es_antisimetrica(conjunto_A, relaciones)
es_relacion_transitiva = es_transitiva(conjunto_A, relaciones)

# Verificar si es relación de equivalencia
es_equivalencia(es_relacion_reflexiva, es_relacion_simetrica, es_relacion_transitiva, conjunto_A, relaciones)

# Verificar si es relación de orden parcial
es_orden_parcial(es_relacion_reflexiva, es_relacion_antisimetrica, es_relacion_transitiva, conjunto_A, relaciones)

# Generar la matriz de adyacencia
generar_matriz(conjunto_A, relaciones)

