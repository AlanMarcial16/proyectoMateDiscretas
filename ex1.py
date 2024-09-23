import os

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

# Verificar las propiedades
es_reflexiva(conjunto_A, relaciones)
es_irreflexiva(conjunto_A, relaciones)
es_simetrica(conjunto_A, relaciones)
es_asimetrica(conjunto_A, relaciones)
es_antisimetrica(conjunto_A, relaciones)
es_transitiva(conjunto_A, relaciones)
