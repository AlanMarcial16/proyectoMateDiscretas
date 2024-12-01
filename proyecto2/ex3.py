import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def generar_mapa_cuadras():
    try:
        filas = int(filas_entry.get())  # Número de filas (Norte-Sur)
        columnas = int(columnas_entry.get())  # Número de columnas (Este-Oeste)
    except ValueError:
        tk.messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
        return

    # Crear una figura para el mapa
    fig = Figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    # Dibujar calles (azul claro muy tenue)
    for i in range(filas + 1):  # Calles horizontales
        ax.plot([0, columnas], [i, i], color="#d8dbb7", linewidth=5)  # Color azul claro (RGB: 208, 239, 255)

    for j in range(columnas + 1):  # Calles verticales
        ax.plot([j, j], [0, filas], color="#d8dbb7", linewidth=5)

    # Dibujar nodos (rectángulos en azul rey)
    for i in range(filas):
        for j in range(columnas):
            # Nodos con forma rectangular y color azul rey (vertical)
            ax.add_patch(plt.Rectangle(
                (j + 0.2, filas - i - 1 + 0.1),  # Coordenadas ajustadas para centrado
                0.6, 0.8,  # Dimensiones del rectángulo (ancho x alto) -> Vertical
                color="#D0EFFF", ec="black", linewidth=1.5  # Azul rey (RGB: 0, 51, 153)
            ))
            # Etiqueta de la cuadra
            ax.text(j + 0.5, filas - i - 0.5, f"N({i},{j})", 
                    ha="center", va="center", fontsize=8, color="black")

    # Ajustar límites y ocultar ejes
    ax.set_xlim(0, columnas)
    ax.set_ylim(0, filas)
    ax.axis("off")

    # Mostrar el gráfico en el lienzo
    canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
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
