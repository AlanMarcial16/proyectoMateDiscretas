import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from heapq import heappop, heappush
import math

# Variables globales
conexiones = []
nodo_inicial = None
nodo_final = None
mapa_filas = 0
mapa_columnas = 0
ax = None
canvas = None

def reiniciar():
    """Reinicia el programa limpiando el gráfico."""
    global ax, canvas, conexiones, nodo_inicial, nodo_final
    conexiones = []
    nodo_inicial = None
    nodo_final = None
    if ax:
        ax.cla()  # Limpia el gráfico
        inicializar_grafico()  # Redibuja la estructura base
        canvas.draw()  # Actualiza el canvas

def inicializar_grafico():
    """Configura la estructura base del gráfico."""
    global ax
    ax.set_xlim(0, mapa_columnas)
    ax.set_ylim(0, mapa_filas)
    ax.set_xticks(range(mapa_columnas + 1))
    ax.set_yticks(range(mapa_filas + 1))
    ax.grid(color="lightgray", linestyle="-", linewidth=0.5)
    ax.set_aspect("equal")

def generar_mapa_cuadras():
    """Genera el mapa de nodos y calles."""
    global ax, canvas, mapa_filas, mapa_columnas

    try:
        mapa_filas = int(filas_entry.get())  # Número de filas
        mapa_columnas = int(columnas_entry.get())  # Número de columnas
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
        return

    fig = Figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    for i in range(mapa_filas + 1):
        ax.plot([0, mapa_columnas], [i, i], color="#d8dbb7", linewidth=5)

    for j in range(mapa_columnas + 1):
        ax.plot([j, j], [0, mapa_filas], color="#d8dbb7", linewidth=5)

    for i in range(mapa_filas):
        for j in range(mapa_columnas):
            ax.add_patch(plt.Rectangle(
                (j + 0.2, mapa_filas - i - 1 + 0.1),
                0.6, 0.8,
                color="#D0EFFF", ec="black", linewidth=1.5
            ))
            etiqueta = f"N({i},{j})"
            ax.text(j + 0.5, mapa_filas - i - 0.5, etiqueta,
                    ha="center", va="center", fontsize=8, color="black", picker=True)

    ax.set_xlim(0, mapa_columnas)
    ax.set_ylim(0, mapa_filas)
    ax.axis("off")

    canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect("pick_event", seleccionar_nodo)
    canvas.draw()

def seleccionar_nodo(event):
    """Selecciona un nodo al hacer clic en él."""
    global nodo_inicial, nodo_final

    texto = event.artist.get_text()
    if nodo_inicial is None:
        nodo_inicial = texto
        messagebox.showinfo("Nodo Seleccionado", f"Nodo inicial seleccionado: {nodo_inicial}")
    elif nodo_final is None:
        nodo_final = texto
        messagebox.showinfo("Nodo Seleccionado", f"Nodo final seleccionado: {nodo_final}")
        solicitar_peso()

def solicitar_peso():
    """Solicita al usuario ingresar el peso de la conexión entre dos nodos."""
    global nodo_inicial, nodo_final, conexiones

    peso = simpledialog.askfloat("Peso de la conexión", f"Ingrese el peso entre {nodo_inicial} y {nodo_final}:")
    if peso is not None:
        conexiones.append((nodo_inicial, nodo_final, peso))
        messagebox.showinfo("Conexión Creada", f"Conexión creada entre {nodo_inicial} y {nodo_final} con peso {peso}")
        dibujar_camino(nodo_inicial, nodo_final, peso)

    nodo_inicial = None
    nodo_final = None

def dibujar_camino(nodo1, nodo2, peso):
    """Dibuja una conexión entre dos nodos con su peso."""
    global ax, canvas

    fila1, col1 = map(int, nodo1.strip("N()").split(","))
    fila2, col2 = map(int, nodo2.strip("N()").split(","))

    x1, y1 = col1 + 0.5, mapa_filas - fila1 - 0.5
    x2, y2 = col2 + 0.5, mapa_filas - fila2 - 0.5

    ax.plot([x1, x2], [y1, y2], color="red", linewidth=2, zorder=2)
    dibujar_peso((x1 + x2) / 2, (y1 + y2) / 2, peso)
    canvas.draw()

def dibujar_peso(x, y, peso):
    """Dibuja un cuadro con el peso de la conexión."""
    global ax
    ax.add_patch(plt.Rectangle((x - 0.2, y - 0.1), 0.4, 0.2, color="white", ec="black", lw=1, zorder=3))
    ax.text(x, y, f"{peso:.1f}", color="black", fontsize=10, ha="center", va="center", zorder=4)

def encontrar_camino_mas_corto():
    """Calcula y muestra el camino más corto usando el algoritmo de Dijkstra."""
    global nodo_inicial, nodo_final, conexiones

    if nodo_inicial is None or nodo_final is None:
        messagebox.showerror("Error", "Debe seleccionar un nodo inicial y un nodo final.")
        return

    grafo = {}
    for nodo1, nodo2, peso in conexiones:
        if nodo1 not in grafo:
            grafo[nodo1] = []
        if nodo2 not in grafo:
            grafo[nodo2] = []
        grafo[nodo1].append((peso, nodo2))
        grafo[nodo2].append((peso, nodo1))

    distancias = {nodo: math.inf for nodo in grafo}
    distancias[nodo_inicial] = 0
    predecesores = {}
    pq = [(0, nodo_inicial)]

    while pq:
        peso_actual, nodo_actual = heappop(pq)

        if peso_actual > distancias[nodo_actual]:
            continue

        for peso_conexion, vecino in grafo[nodo_actual]:
            distancia = peso_actual + peso_conexion
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                predecesores[vecino] = nodo_actual
                heappush(pq, (distancia, vecino))

    camino = []
    nodo = nodo_final
    while nodo in predecesores:
        camino.append(nodo)
        nodo = predecesores[nodo]
    camino.append(nodo_inicial)
    camino.reverse()

    for i in range(len(camino) - 1):
        nodo1 = camino[i]
        nodo2 = camino[i + 1]
        dibujar_camino_resaltado(nodo1, nodo2)

    peso_total = distancias[nodo_final]
    messagebox.showinfo("Camino Más Corto", f"El peso total del camino más corto es: {peso_total:.2f}")

def dibujar_camino_resaltado(nodo1, nodo2):
    """Dibuja el camino resaltado entre dos nodos."""
    global ax, canvas

    fila1, col1 = map(int, nodo1.strip("N()").split(","))
    fila2, col2 = map(int, nodo2.strip("N()").split(","))

    x1, y1 = col1 + 0.5, mapa_filas - fila1 - 0.5
    x2, y2 = col2 + 0.5, mapa_filas - fila2 - 0.5

    ax.plot([x1, x2], [y1, y2], color="yellow", linewidth=3, zorder=3)
    canvas.draw()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Mapa de Nodos y Caminos")
root.geometry("800x600")

frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_controls, text="Filas (Norte-Sur):").pack()
filas_entry = tk.Entry(frame_controls)
filas_entry.pack()

tk.Label(frame_controls, text="Columnas (Este-Oeste):").pack()
columnas_entry = tk.Entry(frame_controls)
columnas_entry.pack()

tk.Button(frame_controls, text="Generar Mapa", command=generar_mapa_cuadras).pack(pady=5)
tk.Button(frame_controls, text="Reiniciar", command=reiniciar).pack(pady=5)
tk.Button(frame_controls, text="Encontrar Camino Más Corto", command=encontrar_camino_mas_corto).pack(pady=5)

frame_canvas = tk.Frame(root)
frame_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()
