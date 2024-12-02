import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Variables globales
conexiones = []
nodos_letras = {}  # Mapeo de nodos a letras
alfabeto = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
nodo_inicial = None
nodo_final = None
mapa_filas = 0
mapa_columnas = 0
ax = None
canvas = None

def reiniciar():
    """Reinicia el programa limpiando el gráfico."""
    global ax, canvas, conexiones, nodo_inicial, nodo_final, nodos_letras, alfabeto
    conexiones.clear()
    nodo_inicial = None
    nodo_final = None
    nodos_letras.clear()
    alfabeto = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
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
    global ax, canvas, mapa_filas, mapa_columnas

    try:
        mapa_filas = int(filas_entry.get())  # Número de filas (Norte-Sur)
        mapa_columnas = int(columnas_entry.get())  # Número de columnas (Este-Oeste)
    except ValueError:
        tk.messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
        return

    # Crear una figura para el mapa
    fig = Figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    # Dibujar calles (azul claro muy tenue)
    for i in range(mapa_filas + 1):  # Calles horizontales
        ax.plot([0, mapa_columnas], [i, i], color="#d8dbb7", linewidth=5)

    for j in range(mapa_columnas + 1):  # Calles verticales
        ax.plot([j, j], [0, mapa_filas], color="#d8dbb7", linewidth=5)

    # Dibujar nodos (rectángulos en azul rey)
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

    # Ajustar límites y ocultar ejes
    ax.set_xlim(0, mapa_columnas)
    ax.set_ylim(0, mapa_filas)
    ax.axis("off")

    # Mostrar el gráfico en el lienzo
    canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.mpl_connect("pick_event", seleccionar_nodo)  # Evento de selección de nodo
    canvas.draw()

def asignar_letra(nodo):
    """Asigna una letra a un nodo si aún no la tiene."""
    global nodos_letras, alfabeto
    if nodo not in nodos_letras:
        nodos_letras[nodo] = next(alfabeto)
    return nodos_letras[nodo]

def seleccionar_nodo(event):
    global nodo_inicial, nodo_final

    texto = event.artist.get_text()
    letra = asignar_letra(texto)

    if nodo_inicial is None:
        nodo_inicial = texto
        resaltar_nodo(texto, "green", letra)
        messagebox.showinfo("Nodo Seleccionado", f"Nodo inicial seleccionado: {letra}")
    elif nodo_final is None:
        nodo_final = texto
        resaltar_nodo(texto, "blue", letra)
        messagebox.showinfo("Nodo Seleccionado", f"Nodo final seleccionado: {letra}")
        solicitar_peso()

def solicitar_peso():
    global nodo_inicial, nodo_final, conexiones

    peso = simpledialog.askfloat("Peso de la conexión", f"Ingrese el peso entre {nodos_letras[nodo_inicial]} y {nodos_letras[nodo_final]}:")
    if peso is not None:
        conexiones.append((nodo_inicial, nodo_final, peso))
        messagebox.showinfo("Conexión Creada", f"Conexión creada entre {nodos_letras[nodo_inicial]} y {nodos_letras[nodo_final]} con peso {peso}")
        dibujar_camino(nodo_inicial, nodo_final, peso)

    nodo_inicial = None
    nodo_final = None

def dibujar_camino(nodo1, nodo2, peso):
    global ax, canvas

    fila1, col1 = map(int, nodo1.strip("N()").split(","))
    fila2, col2 = map(int, nodo2.strip("N()").split(","))

    x1, y1 = col1 + 0.5, mapa_filas - fila1 - 0.5
    x2, y2 = col2 + 0.5, mapa_filas - fila2 - 0.5

    # Dibujar línea y flecha
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor="red", arrowstyle="-|>", lw=2))

    # Dibujar nodos resaltados
    ax.scatter(x1, y1, color="green", s=100, zorder=3, label="Inicio")
    ax.scatter(x2, y2, color="blue", s=100, zorder=3, label="Final")

    peso_x = (x1 + x2) / 2
    peso_y = (y1 + y2) / 2

    dibujar_peso(peso_x, peso_y, peso)
    canvas.draw()

def dibujar_peso(x, y, peso):
    global ax
    ancho, alto = 0.5, 0.3
    ax.add_patch(plt.Rectangle((x - ancho / 2, y - alto / 2), ancho, alto, color="white", ec="black", lw=1, zorder=3))
    ax.text(x, y, f"{peso:.1f}", color="black", fontsize=10, fontweight="bold", ha="center", va="center", zorder=4)

def resaltar_nodo(nodo, color, letra):
    global ax
    fila, col = map(int, nodo.strip("N()").split(","))
    x, y = col + 0.5, mapa_filas - fila - 0.5
    ax.add_patch(plt.Rectangle((col + 0.2, mapa_filas - fila - 1 + 0.1),
                                0.6, 0.8, color=color, ec="black", lw=2, zorder=3))
    ax.text(x, y, letra, color="white", fontsize=12, fontweight="bold", ha="center", va="center", zorder=4)


def encontrar_camino_mas_corto():
    """Abre una ventana para seleccionar nodos y encuentra el camino más corto."""
    global conexiones, ax, canvas

    if not conexiones:
        messagebox.showinfo("Sin conexiones", "Por favor, agregue conexiones antes de encontrar el camino más corto.")
        return

    # Pedir nodo inicial y final
    nodo_inicial = simpledialog.askstring("Nodo inicial", "Ingrese el nodo inicial (ej: A):")
    nodo_final = simpledialog.askstring("Nodo final", "Ingrese el nodo final (ej: K):")

    if not nodo_inicial or not nodo_final:
        messagebox.showerror("Error", "Debe especificar ambos nodos.")
        return

    # Convertir letras a nodos
    nodo_inicial_real = next((nodo for nodo, letra in nodos_letras.items() if letra == nodo_inicial), None)
    nodo_final_real = next((nodo for nodo, letra in nodos_letras.items() if letra == nodo_final), None)

    if not nodo_inicial_real or not nodo_final_real:
        messagebox.showerror("Error", "Los nodos especificados no existen.")
        return

    # Implementar algoritmo de Dijkstra
    grafo = construir_grafo()
    peso_total, camino = dijkstra(grafo, nodo_inicial_real, nodo_final_real)

    if camino is None:
        messagebox.showinfo("Sin camino", f"No existe un camino entre {nodo_inicial} y {nodo_final}.")
        return

    # Mostrar resultados
    messagebox.showinfo("Camino más corto", f"Peso total: {peso_total}\nRecorrido: {' -> '.join(camino)}")

    # Resaltar camino en el gráfico
    resaltar_camino(camino)


def construir_grafo():
    """Convierte las conexiones a un formato de grafo."""
    grafo = {}
    for nodo1, nodo2, peso in conexiones:
        if nodo1 not in grafo:
            grafo[nodo1] = []
        if nodo2 not in grafo:
            grafo[nodo2] = []
        grafo[nodo1].append((nodo2, peso))
        grafo[nodo2].append((nodo1, peso))  # Grafo no dirigido
    return grafo


def dijkstra(grafo, inicio, destino):
    """Algoritmo de Dijkstra para encontrar el camino más corto."""
    import heapq

    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[inicio] = 0
    prioridad = [(0, inicio)]
    predecesores = {}

    while prioridad:
        distancia_actual, nodo_actual = heapq.heappop(prioridad)

        if nodo_actual == destino:
            camino = []
            while nodo_actual:
                camino.append(nodos_letras[nodo_actual])
                nodo_actual = predecesores.get(nodo_actual)
            return distancia_actual, camino[::-1]

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(prioridad, (distancia, vecino))

    return float("inf"), None


def resaltar_camino(camino):
    """Resalta el camino más corto en el gráfico."""
    global ax, canvas

    # Atenuar todos los caminos
    ax.lines = [linea for linea in ax.lines if not hasattr(linea, "color_original")]
    for nodo1, nodo2, peso in conexiones:
        fila1, col1 = map(int, nodo1.strip("N()").split(","))
        fila2, col2 = map(int, nodo2.strip("N()").split(","))

        x1, y1 = col1 + 0.5, mapa_filas - fila1 - 0.5
        x2, y2 = col2 + 0.5, mapa_filas - fila2 - 0.5

        linea, = ax.plot([x1, x2], [y1, y2], color="#cccccc", linestyle="--", lw=1)
        linea.color_original = "gray"  # Guardar color original

    # Resaltar el camino más corto
    for i in range(len(camino) - 1):
        nodo1 = next((nodo for nodo, letra in nodos_letras.items() if letra == camino[i]), None)
        nodo2 = next((nodo for nodo, letra in nodos_letras.items() if letra == camino[i + 1]), None)

        if nodo1 and nodo2:
            fila1, col1 = map(int, nodo1.strip("N()").split(","))
            fila2, col2 = map(int, nodo2.strip("N()").split(","))

            x1, y1 = col1 + 0.5, mapa_filas - fila1 - 0.5
            x2, y2 = col2 + 0.5, mapa_filas - fila2 - 0.5

            ax.plot([x1, x2], [y1, y2], color="green", lw=2)

    canvas.draw()




# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Mapa de Calles y Cuadras")

frame_inputs = tk.Frame(root)
frame_inputs.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Label(frame_inputs, text="Número de filas (Norte-Sur):").pack(side=tk.LEFT)
filas_entry = tk.Entry(frame_inputs, width=5)
filas_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame_inputs, text="Número de columnas (Oriente-Poniente):").pack(side=tk.LEFT)
columnas_entry = tk.Entry(frame_inputs, width=5)
columnas_entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame_inputs, text="Generar Mapa", command=generar_mapa_cuadras).pack(side=tk.LEFT, padx=10)
tk.Button(frame_inputs, text="Reiniciar", command=reiniciar).pack(side=tk.LEFT, padx=10)

# Agregar el botón en la interfaz principal
tk.Button(frame_inputs, text="Encontrar el camino más corto", command=encontrar_camino_mas_corto).pack(side=tk.LEFT, padx=10)

frame_canvas = tk.Frame(root)
frame_canvas.pack(fill=tk.BOTH, expand=1)

root.mainloop()
