import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Variables globales
conexiones = []
nodo_inicial = None
nodo_final = None
mapa_filas = 0
mapa_columnas = 0

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
            # Dibujar nodos como rectángulos
            ax.add_patch(plt.Rectangle(
                (j + 0.2, mapa_filas - i - 1 + 0.1),
                0.6, 0.8,
                color="#D0EFFF", ec="black", linewidth=1.5
            ))
            # Etiqueta de la cuadra
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

def seleccionar_nodo(event):
    """Función para manejar la selección de nodos."""
    global nodo_inicial, nodo_final

    # Obtener el texto del nodo seleccionado
    texto = event.artist.get_text()

    # Seleccionar nodos inicial y final
    if nodo_inicial is None:
        nodo_inicial = texto
        messagebox.showinfo("Nodo Seleccionado", f"Nodo inicial seleccionado: {nodo_inicial}")
    elif nodo_final is None:
        nodo_final = texto
        messagebox.showinfo("Nodo Seleccionado", f"Nodo final seleccionado: {nodo_final}")
        solicitar_peso()  # Solicitar peso entre los nodos

def solicitar_peso():
    """Solicitar el peso entre los nodos seleccionados."""
    global nodo_inicial, nodo_final, conexiones

    peso = simpledialog.askfloat("Peso de la conexión", f"Ingrese el peso entre {nodo_inicial} y {nodo_final}:")
    if peso is not None:
        conexiones.append((nodo_inicial, nodo_final, peso))
        messagebox.showinfo("Conexión Creada", f"Conexión creada entre {nodo_inicial} y {nodo_final} con peso {peso}")
        dibujar_camino(nodo_inicial, nodo_final, peso)  # Dibujar el camino en el mapa

    # Resetear la selección de nodos
    nodo_inicial = None
    nodo_final = None

def dibujar_camino(nodo1, nodo2, peso):
    """Dibuja un camino entre dos nodos sin atravesar otros nodos."""
    global ax, canvas

    # Extraer las coordenadas de los nodos
    fila1, col1 = map(int, nodo1.strip("N()").split(","))
    fila2, col2 = map(int, nodo2.strip("N()").split(","))

    # Coordenadas ajustadas para estar en las "calles" (centradas)
    x1, y1 = col1 + 0.5, mapa_filas - fila1 - 0.5  # Nodo de inicio
    x2, y2 = col2 + 0.5, mapa_filas - fila2 - 0.5  # Nodo de final

    # Dibujar camino: evitar atravesar nodos
    if fila1 == fila2:  # Mismo nivel horizontal (misma fila)
        ax.plot([x1, x2], [y1, y1], color="red", linewidth=2)
    elif col1 == col2:  # Misma columna (vertical)
        ax.plot([x1, x1], [y1, y2], color="red", linewidth=2)
    else:  # Camino en "L" (diferente fila y columna)
        # Vertical primero, luego horizontal
        ax.plot([x1, x1], [y1, y2], color="red", linewidth=2)  # Vertical
        ax.plot([x1, x2], [y2, y2], color="red", linewidth=2)  # Horizontal

    # Agregar distintivos en el inicio y final
    ax.scatter(x1, y1, color="green", s=100, label="Inicio")  # Nodo inicial
    ax.scatter(x2, y2, color="blue", s=100, label="Final")    # Nodo final

    # Mostrar el peso en el punto medio del camino
    peso_x = x1 if fila1 != fila2 else (x1 + x2) / 2
    peso_y = y2 if fila1 != fila2 else y1
    ax.text(peso_x, peso_y, f"{peso:.1f}", color="red", fontsize=10, fontweight="bold", ha="center")

    canvas.draw()



# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Mapa de Calles y Cuadras")

# Marco superior para las entradas
frame_inputs = tk.Frame(root)
frame_inputs.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Label(frame_inputs, text="Número de filas (Norte-Sur):").pack(side=tk.LEFT)
filas_entry = tk.Entry(frame_inputs, width=5)
filas_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame_inputs, text="Número de columnas (Este-Oeste):").pack(side=tk.LEFT)
columnas_entry = tk.Entry(frame_inputs, width=5)
columnas_entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame_inputs, text="Generar Mapa", command=generar_mapa_cuadras).pack(side=tk.LEFT, padx=10)

# Marco inferior para el gráfico
frame_canvas = tk.Frame(root)
frame_canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

root.mainloop()
