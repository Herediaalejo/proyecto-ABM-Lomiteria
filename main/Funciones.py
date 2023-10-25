import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from datetime import datetime

pedidos = []  # Lista para rastrear los pedidos
inicio_tiempo = datetime.now()  # Variable global para el tiempo
amarillo = "#e6a902"
rojo = "#e60707"
blanco = "#fcebeb"
verde = "#4ab56e"

def create_window(root, op):
    if op == 0:
        principal = tk.Toplevel(root)
        principal.state('zoomed')
        principal.config(bg= blanco)
        screen_width = root.winfo_screenwidth()
        bandeja_color = "green"

        for row in range(10):
            for column in range(6):
                crear_celda(principal, row, column, all_columns=6 , color=blanco, padx=(10,10), pady=(20,10), height=70)
        title_lab = tk.Label(principal, text="Lomitos X2", font=("Gill Sans MT", 32), bg=blanco)
        title_lab.grid(row=0,column=2,columnspan=2)
        title2_lab = tk.Label(principal, text="HADLER\nSistema de gestión", font=("Gill Sans MT", 20), bg=blanco)
        title2_lab.grid(row=0,column=0,columnspan=2, sticky="n")

        bandeja_frame = tk.Frame(principal, bg=bandeja_color, borderwidth=3, relief="solid")
        bandeja_frame.grid(row=1, column=0, rowspan=7, columnspan=2, sticky="nsew", padx=10)

        subrayado = ttk.Style()
        subrayado.configure('Subrayado.TLabel', font=("Gill Sans MT", 20, 'underline'))

        bandeja_title = ttk.Label(bandeja_frame, text="Bandeja de pendientes", style='Subrayado.TLabel', background=bandeja_color)
        bandeja_title.grid(row=0, column=0, columnspan=6)

        def crear_pedido():
            nuevo_pedido_frame = tk.Frame(bandeja_frame, bg=bandeja_color, padx=10, pady=5, borderwidth=2, relief="solid")
            nuevo_pedido_frame.grid(row=len(pedidos) + 2, column=0, columnspan=6, padx=(5, 5), pady=(5, 5))

            pedido_font = ("Gill Sans MT", 10)

            pedido_label = tk.Label(nuevo_pedido_frame, text=f"Pedido {len(pedidos) + 1}", cursor="hand2", background=bandeja_color, font=("Gill Sans MT", 10, "bold"))
            tiempo_label = tk.Label(nuevo_pedido_frame, text="00:00", background=bandeja_color, font=("Gill Sans MT", 10, "bold"))
            entregar_button = tk.Button(nuevo_pedido_frame, text="ENTREGAR", relief="flat", font=pedido_font)
            modificar_button = tk.Button(nuevo_pedido_frame, text="MODIFICAR", relief="flat", font=pedido_font)
            cancelar_button = tk.Button(nuevo_pedido_frame, text="CANCELAR", relief="flat", font=pedido_font)
            imprimir_button = tk.Button(nuevo_pedido_frame, text="IMPRIMIR", relief="flat", font=pedido_font)

            #pedido_label.bind("<Button-1>", "Funcion")

            pedido_label.grid(row=0, column=0, padx=(0,20))
            tiempo_label.grid(row=0, column=1, padx=(0,20))
            entregar_button.grid(row=0, column=2, padx=(0,20))
            modificar_button.grid(row=0, column=3, padx=(0,20))
            cancelar_button.grid(row=0, column=4, padx=(0,20))
            imprimir_button.grid(row=0, column=5)

            nuevo_pedido = {
                'frame': nuevo_pedido_frame,
                'tiempo_label': tiempo_label,
                'inicio_tiempo': datetime.now()
            }
            pedidos.append(nuevo_pedido)

        nuevo_pedido_button = tk.Button(principal, text="Nuevo Pedido", relief="flat", command=lambda: crear_pedido(), bg=amarillo)

        nuevo_pedido_button.grid(row=3, column=3, columnspan=2, pady=(20, 10))

        def tiempo_transcurrido(inicio_tiempo):
            tiempo_actual = datetime.now()
            tiempo_transcurrido = tiempo_actual - inicio_tiempo
            segundos_transcurridos = tiempo_transcurrido.total_seconds()
            minutos = int(segundos_transcurridos / 60)
            segundos = int(segundos_transcurridos % 60)
            return f"{minutos:02d}:{segundos:02d}"

        def actualizar_tiempo():
            tiempo_actual = tiempo_transcurrido(inicio_tiempo)

            # Actualiza el tiempo para cada pedido en la lista de pedidos
            for pedido in pedidos:
                pedido['tiempo_label'].config(text=tiempo_transcurrido(pedido['inicio_tiempo']))

            principal.after(1000, actualizar_tiempo)

        # Asegúrate de llamar a esta función después de agregar el primer pedido
        actualizar_tiempo()

        principal.mainloop()



def crear_celda(ventana, row, column, all_columns, color, padx, pady, width=200, height=30, op=0):
    if op == 0:
        screen_width = ventana.winfo_screenwidth()
        width = (screen_width-((padx[0] + padx[1])*all_columns))/all_columns
    celda = tk.Frame(ventana, width=width,height=height, bg=color)#,borderwidth=1, relief='solid'
    celda.grid(row=row, column=column, pady=pady, padx=padx)
    return celda





