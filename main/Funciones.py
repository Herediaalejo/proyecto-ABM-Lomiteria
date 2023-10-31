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
entrada_seleccionada = None  # Variable para almacenar el valor seleccionado
entrega_seleccionada = None

# Función para manejar la selección del botón
def seleccionar_entrada(button, seleccion):
    global entrada_seleccionada
    if button["bg"] != "orange":
        for btn in botones_entrada:
            btn.config(bg="white")
        button.config(bg="orange")
        entrada_seleccionada = seleccion
    else:
        button.config(bg="white")
        entrada_seleccionada = None
    print(entrada_seleccionada)
    
def seleccionar_entrega(button, seleccion):
    global entrega_seleccionada
    if button["bg"] != "orange":
        for btn in botones_entrega:
            btn.config(bg="white")
        button.config(bg="orange")
        entrega_seleccionada = seleccion
    else:
        button.config(bg="white")
        entrega_seleccionada = None
    print(entrega_seleccionada)

def crear_celda(ventana, row, column, all_columns, color, padx, pady, width=200, height=30, op=0, sticky=""):
    if op == 0:
        screen_width = ventana.winfo_screenwidth()
        width = (screen_width-((padx[0] + padx[1])*all_columns))/all_columns
    celda = tk.Frame(ventana, width=width,height=height, bg=color)#,borderwidth=1, relief='solid'
    celda.grid(row=row, column=column, pady=pady, padx=padx, sticky=sticky)
    return celda

def ingresar(root):
    root.destroy()
    create_window(0)

def eliminar_widgets(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def menu_pedido(ventana):
    global botones_entrada, botones_entrega
    ventana.config(bg= blanco)
    eliminar_widgets(ventana)
    screen_width = ventana.winfo_screenwidth()

    for row in range(6):
        for column in range(5):
            crear_celda(ventana, row, column, all_columns=5 , color=blanco, padx=(10,10), pady=(20,10), sticky="ns")
            ventana.rowconfigure(row, weight=1)  # Expande la fila 
            ventana.columnconfigure(column, weight=1)  # Expande la columna 

    title_lab = tk.Label(ventana, text="Tipo de entrada", font=("Gill Sans MT", 32), bg=blanco)
    title_lab.grid(row=0,column=0,columnspan=5, pady=(0,10), ipady=30)

    entrada_frame = tk.Frame(ventana, bg="#a1c2f7")
    entrada_frame.grid(row=1, column=0,columnspan=5, sticky="nsew", padx=20, pady=50, ipady=100)

    entrada_frame.grid_rowconfigure(0, weight=1)
    entrada_frame.grid_columnconfigure(0, weight=1)
    entrada_frame.grid_columnconfigure(1, weight=1)
    entrada_frame.grid_columnconfigure(2, weight=1)
    entrada_frame.grid_columnconfigure(3, weight=1)
    entrada_frame.grid_columnconfigure(4, weight=1)

    barra_b = tk.Button(entrada_frame, cursor="hand2", text="Local", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(barra_b,"lc"))
    barra_b.grid(column=0,row=0)

    telefono_b = tk.Button(entrada_frame, cursor="hand2", text="Telefono", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(telefono_b,"tel"))
    telefono_b.grid(column=1,row=0)

    whatsapp_b = tk.Button(entrada_frame, cursor="hand2", text="Whatsapp", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(whatsapp_b,"wp"))
    whatsapp_b.grid(column=2,row=0)

    rappi_b = tk.Button(entrada_frame, cursor="hand2", text="Rappi", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(rappi_b,"rp"))
    rappi_b.grid(column=3,row=0)
    
    pedidosya_b = tk.Button(entrada_frame, cursor="hand2", text="Pedidos ya", width=10, font=("Gill Sans MT", 20), borderwidth=2, relief="solid", command=lambda:seleccionar_entrada(pedidosya_b,"py"))
    pedidosya_b.grid(column=4,row=0)

    botones_entrada = [barra_b,telefono_b,whatsapp_b,rappi_b,pedidosya_b]

    title_lab2 = tk.Label(ventana, text="Tipo de entrega", font=("Gill Sans MT", 32), bg=blanco)
    title_lab2.grid(row=2,column=0,columnspan=5, pady=(0,10), ipady=30)

    entrega_frame = tk.Frame(ventana, bg="#a1c2f7")
    entrega_frame.grid(row=3, column=0,columnspan=5, sticky="nsew", padx=20, pady=50, ipady=100)

    entrega_frame.grid_rowconfigure(0, weight=1)
    entrega_frame.grid_columnconfigure(0, weight=1)
    entrega_frame.grid_columnconfigure(1, weight=1)
    entrega_frame.grid_columnconfigure(2, weight=1)
    entrega_frame.grid_columnconfigure(3, weight=1)
    entrega_frame.grid_columnconfigure(4, weight=1)

    local_button = tk.Button(entrega_frame, cursor="hand2", width=10, text="Local", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:seleccionar_entrega(local_button,"lc"))
    local_button.grid(column=1,row=0, columnspan=2)

    delivery_button = tk.Button(entrega_frame, cursor="hand2", width=10, text="Delivery", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:seleccionar_entrega(delivery_button,"dl"))
    delivery_button.grid(column=2,row=0, columnspan=2)

    botones_entrega = [local_button, delivery_button]

    regresar_button = tk.Button(ventana, cursor="hand2", width=10, text="Regresar", bg="#e87e72", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:[ventana.destroy(),create_window(0)])
    regresar_button.grid(column=0,row=4, ipady=10)

    continuar_button = tk.Button(ventana, cursor="hand2", width=10, text="Continuar", bg="#a5e872", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:"")
    continuar_button.grid(column=4,row=4, ipady=10)



def create_window(op):
    if op == 0:
        principal = tk.Tk()
        principal.state('zoomed')
        principal.config(bg= blanco)
        screen_width = principal.winfo_screenwidth()
        bandeja_color = "#a1c2f7"

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

        botones_frame.grid(row=1, column=2, columnspan=2, rowspan=4, padx=(40,0), pady=(40,0))

        regPedido_button = tk.Button(botones_frame, cursor="hand2", text="Registrar pedido",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2, command=lambda:menu_pedido(principal))
        regPedido_button.grid(row=0,column=0,ipadx=10, padx=20, pady=20)

        regProducto_button = tk.Button(botones_frame, cursor="hand2", text="Registrar producto",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regProducto_button.grid(row=0,column=1,ipadx=2, padx=20, pady=20)

        regCompra_button = tk.Button(botones_frame, cursor="hand2", text="Registrar compra",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regCompra_button.grid(row=1,column=0,ipadx=5, padx=20, pady=20)

        regPagos_button = tk.Button(botones_frame, cursor="hand2", text="Registrar pago",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        regPagos_button.grid(row=1,column=1,ipadx=27, padx=20, pady=20)
        
        actPrecio_button = tk.Button(botones_frame, cursor="hand2", text="Actualizar precio",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        actPrecio_button.grid(row=2,column=0,ipadx=7, padx=20, pady=20)

        actStock_button = tk.Button(botones_frame, cursor="hand2", text="Actualizar stock",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        actStock_button.grid(row=2,column=1,ipadx=19, padx=20, pady=20)

        verEstad_button = tk.Button(botones_frame, cursor="hand2", text="Ver estadisticas",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        verEstad_button.grid(row=3,column=0,ipadx=17, padx=20, pady=20) 

        verDatos_button = tk.Button(botones_frame, cursor="hand2", text="Ver datos",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        verDatos_button.grid(row=3,column=1,ipadx=54, padx=20, pady=20) 

        # Obtén la ruta del directorio actual donde se encuentra tu archivo .py
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        # Combina el directorio actual con el nombre de la imagen
        ruta_imagen = os.path.join(directorio_actual, "avatar-hombre2.jpg")

        # Abre una imagen
        image = Image.open(ruta_imagen)

        nuevo_ancho = 250
        nuevo_alto = 250
        image = image.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

        # Convierte la imagen a un formato compatible con tkinter
        photo = ImageTk.PhotoImage(image)

        # Crear un widget Label para mostrar la imagen
        label = tk.Label(principal, image=photo, bg="#fcebeb")
        label.grid(row=2, column=4, columnspan=2, rowspan=2)

        cUser_button = tk.Button(principal, cursor="hand2", text="Cambiar usuario",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2)
        cUser_button.grid(row=1,column=4,ipadx=20, columnspan=2, pady=(40,10))

        userN_label = tk.Label(principal, text="nombre\napellido",font=("Gill Sans MT", 14), bg="#fcebeb")
        userN_label.grid(row=4,column=4,sticky="n", columnspan=2, pady=(10,0))


        def crear_pedido():
            nuevo_pedido_frame = tk.Frame(bandeja_frame, bg=bandeja_color, padx=10, pady=5, borderwidth=2, relief="solid")
            nuevo_pedido_frame.grid(row=len(pedidos) + 2, column=0, columnspan=6, padx=(5, 5), pady=(5, 5))

            pedido_font = ("Gill Sans MT", 10)

            pedido_label = tk.Label(nuevo_pedido_frame, text=f"Pedido {len(pedidos) + 1}", cursor="hand2", background=bandeja_color, font=("Gill Sans MT", 10, "bold"))
            tiempo_label = tk.Label(nuevo_pedido_frame, text="00:00", background=bandeja_color, font=("Gill Sans MT", 10, "bold"))
            entregar_button = tk.Button(nuevo_pedido_frame, text="ENTREGAR", cursor="hand2", relief="flat", font=pedido_font)
            modificar_button = tk.Button(nuevo_pedido_frame, text="MODIFICAR", cursor="hand2", relief="flat", font=pedido_font)
            cancelar_button = tk.Button(nuevo_pedido_frame, text="CANCELAR", cursor="hand2", relief="flat", font=pedido_font)
            imprimir_button = tk.Button(nuevo_pedido_frame, text="IMPRIMIR", cursor="hand2", relief="flat", font=pedido_font)

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