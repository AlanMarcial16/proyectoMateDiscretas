import os

# Función para limpiar la consola
def limpiar_consola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Función para verificar reflexividad
def es_reflexiva(conjunto, relaciones):
    for elemento in conjunto:
        if (elemento, elemento) not in relaciones:
            return False
    return True

# Función para verificar simetría
def es_simetrica(conjunto, relaciones):
    for (a, b) in relaciones:
        if (b, a) not in relaciones:
            return False
    return True

# Función para verificar antisimetría
def es_antisimetrica(conjunto, relaciones):
    for (a, b) in relaciones:
        if (a != b) and (b, a) in relaciones:
            return False
    return True

# Función para verificar transitividad
def es_transitiva(conjunto, relaciones):
    for (a, b) in relaciones:
        for (c, d) in relaciones:
            if b == c and (a, d) not in relaciones:
                return False
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
if es_reflexiva(conjunto_A, relaciones):
    print("La relación es reflexiva")
else:
    print("La relación NO es reflexiva")

if es_simetrica(conjunto_A, relaciones):
    print("La relación es simétrica")
else:
    print("La relación NO es simétrica")

if es_antisimetrica(conjunto_A, relaciones):
    print("La relación es antisimétrica")
else:
    print("La relación NO es antisimétrica")

if es_transitiva(conjunto_A, relaciones):
    print("La relación es transitiva")
else:
    print("La relación NO es transitiva")
