import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq

# Algoritmo de Dijkstra
def dijkstra(grafo, inicio, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    padres = {nodo: None for nodo in grafo}
    cola = [(0, inicio)]

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual == destino:
            break

        for vecino, peso in grafo[nodo_actual]:
            distancia_nueva = distancia_actual + peso
            if distancia_nueva < distancias[vecino]:
                distancias[vecino] = distancia_nueva
                padres[vecino] = nodo_actual
                heapq.heappush(cola, (distancia_nueva, vecino))

    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = padres[nodo]
    camino.reverse()

    return distancias[destino], camino

# Función para agregar nodos y aristas
def agregar_arista():
    nodo1 = nodo1_entry.get()
    nodo2 = nodo2_entry.get()
    peso = peso_entry.get()

    if not (nodo1 and nodo2 and peso):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        peso = float(peso)
    except ValueError:
        messagebox.showerror("Error", "El peso debe ser un número.")
        return

    if nodo1 not in grafo:
        grafo[nodo1] = []
    if nodo2 not in grafo:
        grafo[nodo2] = []

    grafo[nodo1].append((nodo2, peso))
    grafo[nodo2].append((nodo1, peso))  # Para grafos no dirigidos

    dibujar_grafo()
    nodo1_entry.delete(0, tk.END)
    nodo2_entry.delete(0, tk.END)
    peso_entry.delete(0, tk.END)

# Dibujar el grafo
def dibujar_grafo():
    G.clear()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', node_size=1500)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    canvas.draw()

# Calcular el camino más corto
def finalizar():
    inicio = inicio_entry.get()
    destino = destino_entry.get()

    if inicio not in grafo or destino not in grafo:
        messagebox.showerror("Error", "Ambos nodos deben existir en el grafo.")
        return

    costo, camino = dijkstra(grafo, inicio, destino)
    dibujar_camino(camino)
    messagebox.showinfo("Resultado", f"Costo mínimo: {costo}\nCamino: {' -> '.join(camino)}")

# Dibujar el camino más corto
def dibujar_camino(camino):
    pos = nx.spring_layout(G)
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='lightgrey', font_weight='bold', node_size=1500)
    nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='green', node_size=1500)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    edges_in_path = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=2)
    canvas.draw()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Dijkstra en Vivo")

grafo = {}
G = nx.Graph()

frame = tk.Frame(root)
frame.pack()

# Entradas para agregar aristas
tk.Label(frame, text="Nodo 1:").grid(row=0, column=0)
nodo1_entry = tk.Entry(frame)
nodo1_entry.grid(row=0, column=1)

tk.Label(frame, text="Nodo 2:").grid(row=1, column=0)
nodo2_entry = tk.Entry(frame)
nodo2_entry.grid(row=1, column=1)

tk.Label(frame, text="Peso:").grid(row=2, column=0)
peso_entry = tk.Entry(frame)
peso_entry.grid(row=2, column=1)

tk.Button(frame, text="Agregar Arista", command=agregar_arista).grid(row=3, column=0, columnspan=2)

# Entradas para calcular el camino más corto
tk.Label(frame, text="Nodo Inicio:").grid(row=4, column=0)
inicio_entry = tk.Entry(frame)
inicio_entry.grid(row=4, column=1)

tk.Label(frame, text="Nodo Destino:").grid(row=5, column=0)
destino_entry = tk.Entry(frame)
destino_entry.grid(row=5, column=1)

tk.Button(frame, text="Finalizar", command=finalizar).grid(row=6, column=0, columnspan=2)

# Área para graficar
fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
