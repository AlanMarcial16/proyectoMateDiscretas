# Pedir al usuario que introduzca los elementos del conjunto
conjunto_A = set(map(int, input("Introduce los elementos del conjunto A, separados por espacios: ").split()))

# Pedir al usuario que introduzca las relaciones
num_relaciones = int(input("¿Cuántas relaciones quieres introducir?: "))
relaciones = []
for _ in range(num_relaciones):
    a, b = map(int, input("Introduce una relación como 'a b': ").split())
    relaciones.append((a, b))

print("Conjunto A:", conjunto_A)
print("Relaciones:", relaciones)
