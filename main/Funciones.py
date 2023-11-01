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
# Define una lista vacía para almacenar los productos seleccionados
productos_seleccionados = []

def cargar_productos():
    # Crear una conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Lomiteria"  # Nombre de tu base de datos
    )

    # Crear un cursor para ejecutar consultas SQL
    cursor = conexion.cursor()

        # Consulta para obtener los productos y sus precios x1
    query = "SELECT Id_producto, Nombre, PrecioUnitario FROM Producto"
    cursor.execute(query)
    productos = cursor.fetchall()

    # Crear un diccionario para almacenar los precios x2
    precios_x2 = {}

    # Para cada producto, consulta el precio x2 en Promocion2x1
    for producto in productos:
        id_producto, nombre, precio_x1 = producto
        cursor.execute("SELECT Precio FROM Promocion2x1 WHERE Producto1 = %s", (id_producto,))
        rows = cursor.fetchall()
        if rows:  # Verifica si se encontraron resultados
            precio_x2 = rows[0][0]
        else:
            precio_x2 = ""
        precios_x2[id_producto] = precio_x2  # Usar el ID de producto como clave

    cursor.close()
    conexion.close()

    # Agregar el precio x2 a la lista de productos
    productos_con_precios_x2 = []
    for producto in productos:
        id_producto, nombre, precio_x1 = producto
        precio_x2 = precios_x2.get(id_producto, precio_x1)
        productos_con_precios_x2.append((nombre, precio_x1, precio_x2))

    return productos_con_precios_x2

def actualizar_lista_productos():
    productos_seleccionados_listbox.delete(0, tk.END)
    for producto in productos_seleccionados:
        productos_seleccionados_listbox.insert(tk.END, producto)

def agregar_producto(nombre_producto):
    # Verificar si el producto ya está en la lista
    for i, producto in enumerate(productos_seleccionados):
        if producto.startswith(nombre_producto):
            if producto == nombre_producto:
                productos_seleccionados[i] = f"{nombre_producto} x2"
            else:
                productos_seleccionados.insert(i + 1, nombre_producto)
            break
    else:
        productos_seleccionados.append(nombre_producto)
    
    actualizar_lista_productos()

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
    regresar_button.grid(column=0,row=4, ipady=20)

    continuar_button = tk.Button(ventana, cursor="hand2", width=10, text="Continuar", bg="#a5e872", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:menu_pedido2(ventana))
    continuar_button.grid(column=4,row=4, ipady=20)

def menu_pedido2(ventana):
    global productos_seleccionados_listbox

    def mostrar_campos_local():
        if modo_consumo_combo.get() == "Fuera del local" or tipo_entrada_combo.get() != "Local":
            nombre_cliente_label.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
            nombre_cliente_entry.grid(row=3, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
            modo_entrega_label.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
            modo_entrega_combo.grid(row=2, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
        else:
            nombre_cliente_label.grid_remove()
            nombre_cliente_entry.grid_remove()
            modo_entrega_label.grid_remove()
            modo_entrega_combo.grid_remove()
            modo_entrega_combo.set("")
            telefono_label.grid_remove()
            telefono_entry.grid_remove()
            direccion_label.grid_remove()
            direccion_entry.grid_remove()

        if modo_entrega_combo.get() == "Delivery":
            telefono_label.grid(row=4, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
            telefono_entry.grid(row=4, column=1, sticky="w", padx=(5, 10))
            direccion_label.grid(row=5, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
            direccion_entry.grid(row=5, column=1, sticky="w", padx=(5, 10))
        else:
            telefono_label.grid_remove()
            telefono_entry.grid_remove()
            direccion_label.grid_remove()
            direccion_entry.grid_remove()
        if tipo_entrada_combo.get() != "Local":
            modo_consumo_combo.set("Fuera del local")

        
        


    eliminar_widgets(ventana)
    for row in range(10):
        for column in range(5):
            crear_celda(ventana, row, column, all_columns=5 , color="green", padx=(10,10), pady=(20,10), sticky="ns")
            ventana.rowconfigure(row, weight=1)  # Expande la fila 
            ventana.columnconfigure(column, weight=1)  # Expande la columna 

    form = tk.Frame(ventana, relief="solid", bg=blanco, borderwidth=3)
    form.grid(row=0,column=2,sticky="nsew", columnspan=3, rowspan=10, padx=(150,20), pady=20)

    for row in range(6):
        for column in range(2):
            crear_celda(form, row, column, all_columns=5 , color=blanco, padx=(10,10), pady=(20,10), sticky="ns", op=1, width=300)
            ventana.rowconfigure(row, weight=1)  # Expande la fila 
            ventana.columnconfigure(column, weight=1)  # Expande la columna 

    form_title = tk.Label(form, bg=blanco, text="Pedido", font=("Gill Sans MT", 24))
    form_title.grid(row=0,column=0, sticky="w")

    tipo_entrada_label = tk.Label(form, bg=blanco, text="Tipo de entrada:", font=("Gill Sans MT", 16))
    tipo_entrada_label.grid(row=0, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    tipo_entrada_values = ["Local", "Telefono", "Whatsapp", "Pedidos Ya", "Rappi"]
    tipo_entrada_combo = ttk.Combobox(form, values=tipo_entrada_values, font=("Gill Sans MT", 16))
    tipo_entrada_combo.grid(row=0, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
    tipo_entrada_combo.set(tipo_entrada_values[0])  # Establecer un valor predeterminado

    tipo_entrada_combo.bind("<<ComboboxSelected>>", lambda event: mostrar_campos_local())

    modo_consumo_label = tk.Label(form, bg=blanco, text="Modo de consumo:", font=("Gill Sans MT", 16))
    modo_consumo_label.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    # Usar un ComboBox (ttk.Combobox) para el modo de consumo
    modo_consumo_values = ["Mesa", "Fuera del local"]
    modo_consumo_combo = ttk.Combobox(form, values=modo_consumo_values, font=("Gill Sans MT", 16))
    modo_consumo_combo.grid(row=1, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
    modo_consumo_combo.set(modo_consumo_values[0])  # Establecer un valor predeterminado


    modo_consumo_combo.bind("<<ComboboxSelected>>", lambda event: mostrar_campos_local())

    modo_entrega_label = tk.Label(form, bg=blanco, text="Modo de entrega:", font=("Gill Sans MT", 16))
    
    # Usar un ComboBox (ttk.Combobox) para el modo de entrega
    modo_entrega_values = ["Delivery", "Retira"]
    modo_entrega_combo = ttk.Combobox(form, values=modo_entrega_values, font=("Gill Sans MT", 16))


    modo_entrega_combo.bind("<<ComboboxSelected>>", lambda event: mostrar_campos_local())

    # Resto de los campos de entrada
    nombre_cliente_label = tk.Label(form, bg=blanco, text="Nombre del cliente:", font=("Gill Sans MT", 16))
    nombre_cliente_entry = tk.Entry(form, font=("Gill Sans MT", 16), width=22)

    # Campos de teléfono y dirección (inicialmente ocultos)
    telefono_label = tk.Label(form, bg=blanco, text="Teléfono:", font=("Gill Sans MT", 16))
    telefono_entry = tk.Entry(form, font=("Gill Sans MT", 16), width=22)

    direccion_label = tk.Label(form, bg=blanco, text="Dirección:", font=("Gill Sans MT", 16))
    direccion_entry = tk.Entry(form, font=("Gill Sans MT", 16), width=22)

    producto_label = tk.Label(form, bg=blanco, text="Producto/s:", font=("Gill Sans MT", 16))
    producto_label.grid(row=6, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    productos_seleccionados_listbox = tk.Listbox(form, height=5, width=35, font=("Gill Sans MT", 14))
    productos_seleccionados_listbox.grid(row=6, column=1, sticky="w", padx=(5, 0))

    # Agrega un botón para limpiar la Listbox
    limpiar_button = tk.Button(form, text="Limpiar", cursor="hand2", font=("Gill Sans MT", 12), command=lambda: [productos_seleccionados.clear(), actualizar_lista_productos()])
    limpiar_button.grid(row=7, column=1, sticky="w", padx=(5, 0), pady=10)

    descripcion_label = tk.Label(form, bg=blanco, text="Descripción:", font=("Gill Sans MT", 16))
    descripcion_label.grid(row=8, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    descripcion_text = tk.Text(form, font=("Gill Sans MT", 16), width=35, height=3)
    descripcion_text.grid(row=8, column=1, sticky="w", padx=(5, 10), pady=(10, 0))

    medio_pago_label = tk.Label(form, bg=blanco, text="Medio de pago:", font=("Gill Sans MT", 16))
    medio_pago_label.grid(row=9, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    # Usar un ComboBox (ttk.Combobox) para el medio de pago
    medio_pago_values = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito"]
    medio_pago_combo = ttk.Combobox(form, values=medio_pago_values, font=("Gill Sans MT", 16))
    medio_pago_combo.grid(row=9, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
    medio_pago_combo.set(medio_pago_values[0])  # Establecer un valor predeterminado

    mostrar_campos_local()

    regresar_button = tk.Button(ventana, cursor="hand2", width=10, text="Regresar", bg="#e87e72", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:[ventana.destroy(),create_window(0)])
    regresar_button.grid(column=0,row=9, ipady=20)

    # Crear un Canvas como contenedor
    canvas = tk.Canvas(ventana)
    canvas.grid(row=0,column=0,sticky="nsew", columnspan=3, rowspan=8, padx=(20,230), pady=(20,0))

    # Crear un Scrollbar a la derecha del Canvas
    scrollbar = tk.Scrollbar(ventana, command=canvas.yview)
    scrollbar.grid(row=0, column=2, sticky="nse", rowspan=8, pady=(20,0), padx=(0,230))  # Ajuste la columna para colocarlo a la derecha
    canvas.configure(yscrollcommand=scrollbar.set)
    

    # Crear un Frame dentro del Canvas
    productos_frame = tk.Frame(canvas, bg="#e87e72")
    canvas.create_window((0, 0), window=productos_frame, anchor="nw")

    """for row in range(40):
        for column in range(4):
            crear_celda(productos_frame, row, column, all_columns=4 , color="#e87e72", padx=(10,10), pady=(20,10), sticky="ns", op=1)
            ventana.rowconfigure(row, weight=1)  # Expande la fila 
            ventana.columnconfigure(column, weight=1)  # Expande la columna"""

    productos_title = tk.Label(productos_frame, text="Productos", font=("Gill Sans MT", 20), bg=blanco)
    productos_title.grid(row=0,column=1, sticky="w", padx=(20,0), pady=10)

    preciox1_title = tk.Label(productos_frame, text="x1", font=("Gill Sans MT", 20), bg=blanco)
    preciox1_title.grid(row=0,column=2, padx=(20,0), pady=10)
    
    preciox2_title = tk.Label(productos_frame, text="x2", font=("Gill Sans MT", 20), bg=blanco)
    preciox2_title.grid(row=0,column=3, padx=35, pady=10)


    # Configurar el evento de desplazamiento
    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    productos = cargar_productos()

    # Insertar productos en el frame
    for i, producto in enumerate(productos):
        nombre = producto[0]  # Nombre del producto
        precio_x1 = producto[1]  # Precio x1
        precio_x2 = producto[2]  # Precio x2

        nombre_label = tk.Label(productos_frame, text=nombre, bg="#e87e72", font=("Gill Sans MT", 16))
        nombre_label.grid(row=i+1, column=1, sticky="w", padx=(20,0), pady=(0,10))
        
        precio_x1_label = tk.Label(productos_frame, text=f"${precio_x1}", bg="#e87e72", font=("Gill Sans MT", 16))
        precio_x1_label.grid(row=i+1, column=2, sticky="w", padx=(20,0), pady=(0,10))

        precio_x2_label = tk.Label(productos_frame, text=f"${precio_x2}", bg="#e87e72", font=("Gill Sans MT", 16))
        precio_x2_label.grid(row=i+1, column=3, sticky="w", padx=35, pady=(0,10))

        if precio_x2 == "":
            precio_x2_label.config(text="")
        
        agregar_button = tk.Button(productos_frame, text="+", font=("Gill Sans MT", 12, "bold"), relief="flat", cursor="hand2", command=lambda nombre=nombre: agregar_producto(nombre))
        agregar_button.grid(row=i+1, column=0, sticky="e", padx=(30,0), pady=(0,10))
    
    # Actualiza el tamaño del canvas después de agregar elementos al frame
    productos_frame.update_idletasks()

    # Ajusta el tamaño del canvas al tamaño del frame
    canvas.config(scrollregion=canvas.bbox("all"))

    # Crear un frame para mostrar el total
    total_frame = tk.Frame(ventana, bg="lightblue")
    total_frame.grid(column=1, row=9, sticky="nsew", pady=(0,20))  # Espacio debajo del frame del formulario

    total_frame.rowconfigure(0, weight=1)  # Expande la fila 
    total_frame.columnconfigure(0, weight=1)  # Expande la columna

    # Etiqueta para mostrar el total
    total_label = tk.Label(total_frame, text="Total: $0.00", font=("Gill Sans MT", 30))
    total_label.grid(row=0,column=0)

    # Función para actualizar el total
    def actualizar_total():
        # Calcula el total (puedes personalizar esto según tus necesidades)
        total = 0.00  # Debes calcular el total real en función de los productos y cantidades seleccionados
        total_label.config(text=f"Total: ${total:.2f}")


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