import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from datetime import datetime
import os
from PIL import Image, ImageTk

pedidos = []  # Lista para rastrear los pedidos
inicio_tiempo = datetime.now()  # Variable global para el tiempo
amarillo = "#e6a902"
rojo = "#e60707"
blanco = "#fcebeb"
verde = "#4ab56e"

def ingresar(root):
    root.destroy()
    create_window(0)


def create_window(op):
    if op == 0:
        principal = tk.Tk()
        principal.state('zoomed')
        principal.config(bg= blanco)
        screen_width = principal.winfo_screenwidth()
        bandeja_color = "#FF7C51"

        for row in range(10):
            for column in range(6):
                crear_celda(principal, row, column, all_columns=6 , color=blanco, padx=(10,10), pady=(20,10), height=70)
        title_lab = tk.Label(principal, text="Lomitos X2", font=("Gill Sans MT", 32), bg=blanco)
        title_lab.grid(row=0,column=2,columnspan=2)
        title2_lab = tk.Label(principal, text="HADLER\nSistema de gestión", font=("Gill Sans MT", 20), bg=blanco)
        title2_lab.grid(row=0,column=0,columnspan=2, sticky="n", pady=(30,0))

        bandeja_frame = tk.Frame(principal, bg=bandeja_color, borderwidth=3, relief="solid")
        bandeja_frame.grid(row=1, column=0, rowspan=7, columnspan=2, sticky="nsew", padx=10, pady=(40,80))

        subrayado = ttk.Style()
        subrayado.configure('Subrayado.TLabel', font=("Gill Sans MT", 20, 'underline'))

        bandeja_title = ttk.Label(bandeja_frame, text="Bandeja de pendientes", style='Subrayado.TLabel', background=bandeja_color)
        bandeja_title.grid(row=0, column=0, columnspan=6)

        botones_frame = tk.Frame(principal, bg=bandeja_color, borderwidth=3, relief="solid")

        botones_frame.grid(row=1, column=2, columnspan=2, rowspan=4, sticky="nsew", padx=(40,0), pady=(40,0))

        regPedido_button = tk.Button(botones_frame, text="Registrar pedido",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regPedido_button.grid(row=0,column=0,ipadx=10, padx=20, pady=20)

        regProducto_button = tk.Button(botones_frame, text="Registrar producto",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regProducto_button.grid(row=0,column=1,ipadx=2, padx=20, pady=20)

        regCompra_button = tk.Button(botones_frame, text="Registrar compra",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regCompra_button.grid(row=1,column=0,ipadx=5, padx=20, pady=20)

        regPagos_button = tk.Button(botones_frame, text="Registrar pago",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regPagos_button.grid(row=1,column=1,ipadx=27, padx=20, pady=20)
        
        actPrecio_button = tk.Button(botones_frame, text="Actualizar precio",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        actPrecio_button.grid(row=2,column=0,ipadx=7, padx=20, pady=20)

        actStock_button = tk.Button(botones_frame, text="Actualizar stock",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        actStock_button.grid(row=2,column=1,ipadx=19, padx=20, pady=20)

        verEstad_button = tk.Button(botones_frame, text="Ver estadisticas",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        verEstad_button.grid(row=3,column=0,ipadx=17, padx=20, pady=20) 

        verDatos_button = tk.Button(botones_frame, text="Ver datos",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        verDatos_button.grid(row=3,column=1,ipadx=54, padx=20, pady=20) 

        # Obtén la ruta del directorio actual donde se encuentra tu archivo .py
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        # Combina el directorio actual con el nombre de la imagen
        ruta_imagen = os.path.join(directorio_actual, "avatar-hombre.jpg")

        # Abre una imagen
        image = Image.open(ruta_imagen)

        nuevo_ancho = 250
        nuevo_alto = 250
        image = image.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

        # Convierte la imagen a un formato compatible con tkinter
        photo = ImageTk.PhotoImage(image)

        # Crear un widget Label para mostrar la imagen
        label = tk.Label(principal, image=photo)
        label.grid(row=2, column=4, columnspan=2, rowspan=2)

        cUser_button = tk.Button(principal, text="Cambiar usuario",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        cUser_button.grid(row=1,column=4,ipadx=20, columnspan=2, pady=(40,10))

        userN_label = tk.Label(principal, text="nombre\napellido",font=("Gill Sans MT", 14))
        userN_label.grid(row=4,column=4,sticky="n", columnspan=2, pady=(10,0))
        















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

        """nuevo_pedido_button = tk.Button(principal, text="Nuevo Pedido", relief="flat", command=lambda: crear_pedido(), bg=amarillo)

        nuevo_pedido_button.grid(row=3, column=3, columnspan=2, pady=(20, 10))"""

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





