import mysql.connector
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from datetime import datetime
import os
from PIL import Image, ImageTk
import bcrypt

pedidos = {}
pedidos_pendientes = {}
inicio_tiempo = datetime.now()  # Variable global para el tiempo
amarillo = "#e6a902"
rojo = "#e60707"
blanco = "#fcebeb"
verde = "#4ab56e"
entrada_seleccionada = None  # Variable para almacenar el valor seleccionado
entrega_seleccionada = None
# Define una lista vacía para almacenar los productos seleccionados
productos_seleccionados = []
id_pedido_existente = None

directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Combina el directorio actual con el nombre de la imagen
ruta_imagen = os.path.join(directorio_actual, "avatar-hombre2.jpg")

# Abre una imagen
image = Image.open(ruta_imagen)

nuevo_ancho = 250
nuevo_alto = 250
image = image.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

def crear_ventana_secundaria(root):
    ventana_secundaria = tk.Toplevel(root)
    ventana_secundaria.title("Ventana Secundaria")

    blanco = "#fcebeb"
    verde = "#4ab56e"
    amarillo = "#e6a902"

    ventana_secundaria.config(bg=blanco)

    style = ttk.Style()
    style.configure("TFrame", background=verde, width=400, height=600)

    ventana_secundaria.grid_columnconfigure(0, weight=1)

    title_font = ("Gill Sans MT", 20)

    frame = tk.Frame(ventana_secundaria, bg=verde, borderwidth=3, relief="solid")
    frame.grid(row=2, column=0)

    usuario_label = tk.Label(frame, text="Usuario", font=("Gill Sans MT", 16), bg=verde)
    usuario_label.grid(row=1, column=0, pady=(20, 10), columnspan=2)

    usuario_select = ttk.Combobox(frame, font=("Gill Sans MT", 16), state="readonly")
    usuario_select.grid(row=2, column=0, pady=(0, 30), padx=(50, 0))

    add_usuario = tk.Button(frame, text="+", font=("Gill Sans MT", 11, "bold"), relief="flat", cursor="hand2", command=lambda:nuevo_usuario(root, usuario_select))
    add_usuario.grid(row=2, column=1, sticky="NW", ipadx=5, padx=(10, 50))

    password_label = tk.Label(frame, text="Contraseña", font=("Gill Sans MT", 16), bg=verde)
    password_label.grid(row=3, column=0, pady=(0, 10), columnspan=2)

    password_input = tk.Entry(frame, font=("Arial", 18), show="*", width=22)
    password_input.grid(row=4, column=0, pady=(0, 30), columnspan=2, padx=(50, 50))

    ingreso_button = tk.Button(frame, text="INGRESAR", cursor="hand2", relief="flat", font=("Consolas", 14, "bold"), background=amarillo, command=lambda:comprobar_usuario_contraseña(root,usuario_select,password_input))
    ingreso_button.grid(row=5, column=0, pady=(0, 20), columnspan=2)

        # Conecta a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lomiteria"
    )

    # Crea un cursor
    cursor = conexion.cursor()

    # Realiza una consulta SQL para obtener los nombres de usuario
    cursor.execute("SELECT nombre_usuario FROM usuarios")
    nombres_usuarios = [row[0] for row in cursor.fetchall()]

    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    conexion.close()

    # Establece los nombres de usuario en el Combobox
    usuario_select['values'] = nombres_usuarios


    ventana_secundaria.mainloop()


def actualizar_nombres_usuarios(select):
    
    # Conecta a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lomiteria"
    )

    # Crea un cursor
    cursor = conexion.cursor()

    # Realiza una consulta SQL para obtener los nombres de usuario
    cursor.execute("SELECT nombre_usuario FROM usuarios")
    nombres_usuarios = [row[0] for row in cursor.fetchall()]

    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    conexion.close()

    # Establece los nombres de usuario en el Combobox
    select['values'] = nombres_usuarios

def nuevo_usuario(ventana, select):
    global nuevo_usuario_entry, nueva_contraseña_entry, confirmar_contraseña_entry, usuario_select

    usuario_select = select

    crear_usuario_window = tk.Toplevel(ventana, relief="solid", borderwidth=3)
    crear_usuario_window.title("Crear Usuario")
    crear_usuario_window.config(bg=verde)

    nuevo_usuario_label = tk.Label(crear_usuario_window, bg=verde, text="Nuevo Usuario", font=("Gill Sans MT", 16))
    nuevo_usuario_label.grid(row=0, column=0, padx=10, pady=10)

    nuevo_usuario_entry = tk.Entry(crear_usuario_window, font=("Arial", 16), width=24)
    nuevo_usuario_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    nueva_contraseña_label = tk.Label(crear_usuario_window, bg=verde, text="Nueva Contraseña", font=("Gill Sans MT", 16))
    nueva_contraseña_label.grid(row=2, column=0, padx=10, pady=10)
    nueva_contraseña_entry = tk.Entry(crear_usuario_window, font=("Arial", 18), show="*", width=22)
    nueva_contraseña_entry.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    confirmar_contraseña_label = tk.Label(crear_usuario_window, bg=verde, text="Confirmar Contraseña", font=("Gill Sans MT", 16))
    confirmar_contraseña_label.grid(row=4, column=0, padx=10, pady=10)

    confirmar_contraseña_entry = tk.Entry(crear_usuario_window, font=("Arial", 18), show="*", width=22)
    confirmar_contraseña_entry.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    crear_button = tk.Button(crear_usuario_window, text="CREAR", relief="flat", font=("Consolas", 14, "bold"), cursor="hand2", background=amarillo, command=lambda: [crear_usuario_contraseña(crear_usuario_window)])
    crear_button.grid(row=6, column=0, padx=10, pady=20, ipadx=5)

def crear_usuario_contraseña(ventana):
    # Obtén el nombre de usuario y contraseña ingresados en la interfaz gráfica
    nuevo_usuario = nuevo_usuario_entry.get()
    nueva_contraseña = nueva_contraseña_entry.get()
    confirmar_contraseña = confirmar_contraseña_entry.get()

    # Verificar que los campos no estén vacíos
    if not nuevo_usuario or not nueva_contraseña or not confirmar_contraseña:
        messagebox.showerror("Error", "Debes completar todos los campos.")
        return

    # Verificar que las contraseñas coincidan
    if nueva_contraseña == confirmar_contraseña:
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())

        # Conectar a la base de datos y crear el usuario
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lomiteria"
        )
        cursor = conexion.cursor()

        # Insertar el nuevo usuario y su contraseña en la base de datos
        insert_query = "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)"
        values = (nuevo_usuario, hashed_password)
        cursor.execute(insert_query, values)

        # Confirmar los cambios y cerrar la conexión
        conexion.commit()
        cursor.close()
        conexion.close()
        actualizar_nombres_usuarios(usuario_select)
        # Cerrar la ventana de creación de usuario
        ventana.destroy()
    else:
        # Mostrar un mensaje de error si las contraseñas no coinciden
        messagebox.showerror("Error", "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")

def comprobar_usuario_contraseña(root, usuario_entry, contraseña_entry):
    global nombre_usuario
    nombre_usuario = usuario_entry.get()
    contraseña = contraseña_entry.get()

    # Conecta a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lomiteria"
    )
    cursor = conexion.cursor()

    # Busca el usuario en la base de datos
    cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario=%s", (nombre_usuario,))
    resultado = cursor.fetchone()

    if resultado:
        contrasena_almacenada = resultado[0]
        if bcrypt.checkpw(contraseña.encode('utf-8'), contrasena_almacenada.encode('utf-8')):
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
            root.destroy()
            create_window(0)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

    # Cierra la conexión a la base de datos
    conexion.close()



def cargar_pedidos():
    try:
        # Conecta a la base de datos
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lomiteria"
        )
        
        cursor = db.cursor()
        
        # Realiza una consulta para obtener los datos de los pedidos
        cursor.execute("SELECT id_pedido, nombre_cliente, descripcion, total, entregado, cancelado, fecha_registro, direccion, telefono, medio_pago, id_tipo_entrada, id_modo_consumo, id_tipo_entrega FROM Pedido")
        
        # Recupera todos los registros de la consulta
        pedidos = cursor.fetchall()

    except mysql.connector.Error as error:
        print(f"Error al cargar pedidos: {error}")

    finally:
        cursor.close()
        db.close()
        return pedidos

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


def guardar_productos_seleccionados(id_pedido):
    # Convierte la lista de productos seleccionados a una cadena JSON
    productos_json = json.dumps(productos_seleccionados)
    print(productos_json)

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lomiteria"
    )
    cursor = conexion.cursor()

    # Borrar los datos anteriores para el id_pedido en la tabla
    cursor.execute("DELETE FROM ProductosSeleccionados WHERE id_pedido = %s", (id_pedido,))

    # Insertar los productos seleccionados en la tabla
    cursor.execute("INSERT INTO ProductosSeleccionados (id_pedido, Productos) VALUES (%s, %s)", (id_pedido, productos_json))

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()


def cargar_productos_seleccionados(id_pedido):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lomiteria"
    )
    cursor = conexion.cursor()

    # Consulta SQL para obtener la cadena de productos
    cursor.execute("SELECT Productos FROM ProductosSeleccionados WHERE id_pedido = %s", (id_pedido,))
    productos_json = cursor.fetchone()  # Obtiene la cadena JSON

    cursor.close()
    conexion.close()

    if productos_json:
        # Parsea la cadena JSON en una lista de productos
        productos_seleccionados = json.loads(productos_json[0])

        # Llena el ListBox con los productos
        productos_seleccionados_listbox.delete(0, tk.END)
        for producto in productos_seleccionados:
            productos_seleccionados_listbox.insert(tk.END, producto)
    else:
        # Maneja el caso en el que no se encontraron productos para el id_pedido
        productos_seleccionados_listbox.delete(0, tk.END)
        productos_seleccionados_listbox.insert(tk.END, "No se encontraron productos")
    

def actualizar_lista_productos():
    productos_seleccionados_listbox.delete(0, tk.END)
    for producto in productos_seleccionados:
        productos_seleccionados_listbox.insert(tk.END, producto)

def agregar_producto(nombre_producto):
    if nombre_producto in productos_seleccionados:
        # Si el producto ya está en la lista, verifica si tiene precio x2
        for i, producto in enumerate(productos_seleccionados):
            if producto == nombre_producto:
                precio_x1, precio_x2 = productos_precios.get(nombre_producto, (0.0, 0.0))
                cantidad = int(producto.split(" x")[1]) if " x" in producto else 1
                if cantidad < 2 and precio_x2:
                    productos_seleccionados[i] = f"{nombre_producto} x2"
                else:
                    if cantidad == 1 and precio_x2 == "":
                        productos_seleccionados.append(nombre_producto)
                break
    else:
        # Si el producto no está en la lista, verifica si tiene precio x2
        precio_x1, precio_x2 = productos_precios.get(nombre_producto, (0.0, 0.0))
        if precio_x1:
            productos_seleccionados.append(nombre_producto)
        elif precio_x2:
            productos_seleccionados.append(f"{nombre_producto} x2")
        else:
            productos_seleccionados.append(nombre_producto)  # Agregarlo sin "x2"

    actualizar_lista_productos()

def entregar_pedido(id_pedido):
    try:
        # Conectarse a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='Lomiteria'
        )
        
        # Crear un cursor
        cursor = connection.cursor()
        
        # Actualizar el estado del pedido a True
        update_query = "UPDATE Pedido SET entregado = 1 WHERE id_pedido = %s"
        cursor.execute(update_query, (id_pedido,))
        
        # Confirmar la transacción
        connection.commit()
        
        print(f"El pedido con ID {id_pedido} ha sido entregado.")
    
    except mysql.connector.Error as error:
        print(f"Error al entregar el pedido: {error}")
    
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()    

    for pedido in pedidos_pendientes:
        if pedido[0] == id_pedido:
            pedidos_pendientes.remove(pedido)
            print(f"Pedido con ID {id_pedido} ha sido eliminado de la lista de pedidos pendientes.")
            break

def cancelar_pedido(id_pedido):
    try:
        # Conectarse a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='lomiteria'
        )

        # Crear un cursor
        cursor = connection.cursor()

        # Actualizar el estado de cancelación del pedido a True
        update_query = "UPDATE Pedido SET cancelado = 1 WHERE id_pedido = %s"
        cursor.execute(update_query, (id_pedido,))

        # Confirmar la transacción
        connection.commit()

        print(f"El pedido con ID {id_pedido} ha sido cancelado.")

    except mysql.connector.Error as error:
        print(f"Error al cancelar el pedido: {error}")

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    for pedido in pedidos_pendientes:
        if pedido[0] == id_pedido:
            pedidos_pendientes.remove(pedido)
            print(f"Pedido con ID {id_pedido} ha sido eliminado de la lista de pedidos pendientes.")
            break

def traer_tipos(id_pedido):
    try:
        # Conecta a la base de datos
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lomiteria"
        )
        
        cursor = db.cursor()
        
        # Realiza una consulta para obtener los datos de los pedidos
        cursor.execute("SELECT entrada.nombre, consumo.nombre, entrega.nombre FROM pedido p inner join tipoentrada entrada on entrada.id_tipo_entrada = p.id_tipo_entrada inner join modoconsumo consumo on consumo.id_modo_consumo = p.id_modo_consumo inner join tipoentrega entrega on entrega.id_tipo_entrega = p.id_tipo_entrega WHERE p.id_pedido = %s ", (id_pedido,))
        
        # Recupera todos los registros de la consulta
        tipos = cursor.fetchall()

    except mysql.connector.Error as error:
        print(f"Error al cargar pedidos: {error}")

    finally:
        cursor.close()
        db.close()
    return tipos



def llenar_formulario(id_pedido):
    global tipo_entrada, modo_consumo, tipo_entrega, nombre, descripcion, direccion, telefono, medio_pago, id_pedido_existente
    id_pedido_existente = id_pedido
    tipos = traer_tipos(id_pedido)
    for pedido in pedidos:
        if id_pedido == pedido[0]:

            tipo_entrada = tipos[0][0]   # Tipo de entrada
            
            modo_consumo = tipos[0][1] # Modo de consumo

            tipo_entrega = tipos[0][2]  # Modo de entrega


            nombre = pedido[1]  # Nombre del cliente

            descripcion = pedido[2]  # Descripción

            direccion= pedido[7] # Dirección
    
            telefono = pedido[8]  # Teléfono

            medio_pago = pedido[9]  # Medio de pago

def mostrar_campos_local(event=None):
    tipo_entrada = tipo_entrada_combo.get()
    tipo_entrega = modo_entrega_combo.get()
    modo_consumo = modo_consumo_combo.get()

    if tipo_entrada != "Local":
        # Mostrar nombre
        modo_consumo_combo.config(state="normal")
        modo_consumo_combo.set("Fuera del local")
        modo_consumo = modo_consumo_combo.get()
        modo_consumo_combo.config(state="disabled")
        nombre_cliente_label.grid(row=4, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
        nombre_cliente_entry.grid(row=4, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
    else:
        # Ocultar nombre
        nombre_cliente_label.grid_remove()
        nombre_cliente_entry.grid_remove()

    if tipo_entrega == "Delivery":
        # Mostrar dirección y teléfono
        modo_consumo_combo.config(state="normal")
        modo_consumo_combo.set("Fuera del local")
        modo_consumo = modo_consumo_combo.get()
        modo_consumo_combo.config(state="disabled")
        telefono_label.grid(row=5, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
        telefono_entry.grid(row=5, column=1, sticky="w", padx=(5, 10))
        direccion_label.grid(row=6, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
        direccion_entry.grid(row=6, column=1, sticky="w", padx=(5, 10))
    else:
        # Ocultar dirección y teléfono
        telefono_label.grid_remove()
        telefono_entry.grid_remove()
        telefono_entry.delete(0, "end")
        direccion_label.grid_remove()
        direccion_entry.grid_remove()
        direccion_entry.delete(0, "end")
    
    if tipo_entrada != "Local":
        # Mostrar el ComboBox de "Tipo de Entrega"
        modo_entrega_label.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
        modo_entrega_combo.grid(row=3, column=1, sticky="w", padx=(5, 10), pady=(10, 0))

    if modo_consumo == "Mesa":
        modo_entrega_combo.set("")
        modo_entrega_label.grid_remove()
        modo_entrega_combo.grid_remove()
    else:
        modo_entrega_label.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=(10, 0))
        modo_entrega_combo.grid(row=3, column=1, sticky="w", padx=(5, 10), pady=(10, 0))


    if tipo_entrada == "Local":

        modo_consumo_combo.config(state="readonly")
        modo_entrega_combo.set("Retira en local")
        telefono_label.grid_remove()
        telefono_entry.grid_remove()
        telefono_entry.delete(0, "end")
        direccion_label.grid_remove()
        direccion_entry.grid_remove()
        direccion_entry.delete(0, "end")




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
    habilitar_continuar()
    
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
    habilitar_continuar()

def habilitar_continuar():
    if entrega_seleccionada and entrada_seleccionada:
        continuar_button.config(state="normal")
    else:
        continuar_button.config(state="disabled")

def crear_celda(ventana, row, column, all_columns, color, padx, pady, width=200, height=30, op=0, sticky=""):
    if op == 0:
        screen_width = ventana.winfo_screenwidth()
        width = (screen_width-((padx[0] + padx[1])*all_columns))/all_columns
    celda = tk.Frame(ventana, width=width,height=height, bg=color)#,borderwidth=1, relief='solid'
    celda.grid(row=row, column=column, pady=pady, padx=padx, sticky=sticky)
    return celda


def eliminar_widgets(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def limpiar_variables():
    global entrega_seleccionada, entrada_seleccionada
    productos_seleccionados.clear()
    entrega_seleccionada = None
    entrada_seleccionada = None


def menu_pedido(ventana):
    global botones_entrada, botones_entrega, continuar_button
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

    barra_b = tk.Button(entrada_frame, cursor="hand2", text="Local", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(barra_b,"Local"))
    barra_b.grid(column=0,row=0)

    telefono_b = tk.Button(entrada_frame, cursor="hand2", text="Telefono", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(telefono_b,"Teléfono"))
    telefono_b.grid(column=1,row=0)

    whatsapp_b = tk.Button(entrada_frame, cursor="hand2", text="Whatsapp", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(whatsapp_b,"Whatsapp"))
    whatsapp_b.grid(column=2,row=0)

    rappi_b = tk.Button(entrada_frame, cursor="hand2", text="Rappi", width=10, font=("Gill Sans MT", 20), relief="solid", borderwidth=2, command=lambda:seleccionar_entrada(rappi_b,"Rappi"))
    rappi_b.grid(column=3,row=0)
    
    pedidosya_b = tk.Button(entrada_frame, cursor="hand2", text="Pedidos ya", width=10, font=("Gill Sans MT", 20), borderwidth=2, relief="solid", command=lambda:seleccionar_entrada(pedidosya_b,"Pedidos ya"))
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

    local_button = tk.Button(entrega_frame, cursor="hand2", width=10, text="Local", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:seleccionar_entrega(local_button,"Retira en local"))
    local_button.grid(column=1,row=0, columnspan=2)

    delivery_button = tk.Button(entrega_frame, cursor="hand2", width=10, text="Delivery", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:seleccionar_entrega(delivery_button,"Delivery"))
    delivery_button.grid(column=2,row=0, columnspan=2)

    botones_entrega = [local_button, delivery_button]

    regresar_button = tk.Button(ventana, cursor="hand2", width=10, text="Regresar", bg="#e87e72", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:[limpiar_variables(),ventana.destroy(),create_window(0)])
    regresar_button.grid(column=0,row=4, ipady=20)

    continuar_button = tk.Button(ventana, cursor="hand2", state="disabled", width=10, text="Continuar", bg="#a5e872", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda: menu_pedido2(ventana))
    continuar_button.grid(column=4, row=4, ipady=20)

def menu_pedido2(ventana, op=0):
    global productos_seleccionados_listbox, productos_precios, tipo_entrada_combo, modo_consumo_combo, modo_entrega_combo, nombre_cliente_entry, telefono_entry, direccion_entry, descripcion_text, medio_pago_combo, telefono_label, direccion_label, modo_entrega_label, nombre_cliente_label
 
    eliminar_widgets(ventana)
    for row in range(10):
        for column in range(5):
            crear_celda(ventana, row, column, all_columns=5 , color=blanco, padx=(10,10), pady=(20,10), sticky="ns")
            ventana.rowconfigure(row, weight=1)  # Expande la fila 
            ventana.columnconfigure(column, weight=1)  # Expande la columna 

    form = tk.Frame(ventana, relief="solid", bg=blanco, borderwidth=3)
    form.grid(row=0,column=3,sticky="nsew", columnspan=2, rowspan=10, padx=(0,20), pady=20)

    for row in range(12):
        for column in range(3):
            crear_celda(form, row, column, all_columns=3 , color=blanco, padx=(10,10), pady=(20,10), sticky="ns", op=1, width=260)
            ventana.rowconfigure(row, weight=1)  # Expande la fila 
            ventana.columnconfigure(column, weight=1)  # Expande la columna 


    form_title = tk.Label(form, bg=blanco, text="Pedido", font=("Gill Sans MT", 24))
    form_title.grid(row=0,column=0, sticky="w")

    tipo_entrada_label = tk.Label(form, bg=blanco, text="Tipo de entrada:", font=("Gill Sans MT", 16))
    tipo_entrada_label.grid(row=1, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    tipo_entrada_values = ["Local", "Teléfono", "Whatsapp", "Pedidos Ya", "Rappi"]
    tipo_entrada_combo = ttk.Combobox(form, values=tipo_entrada_values, font=("Gill Sans MT", 16))
    tipo_entrada_combo.grid(row=1, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
    tipo_entrada_combo.set(tipo_entrada_values[0])  # Establecer un valor predeterminado
    tipo_entrada_combo.config(state="readonly")

    # Asociar el evento <Configure> al ComboBox
    tipo_entrada_combo.bind("<Configure>", mostrar_campos_local)

    tipo_entrada_combo.bind("<<ComboboxSelected>>", mostrar_campos_local)

    modo_consumo_label = tk.Label(form, bg=blanco, text="Modo de consumo:", font=("Gill Sans MT", 16))
    modo_consumo_label.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    # Usar un ComboBox (ttk.Combobox) para el modo de consumo
    modo_consumo_values = ["Mesa", "Fuera del local"]
    modo_consumo_combo = ttk.Combobox(form, state='disabled', values=modo_consumo_values, font=("Gill Sans MT", 16))
    modo_consumo_combo.grid(row=2, column=1, sticky="w", padx=(5, 10), pady=(10, 0))

    modo_consumo_combo.config(state="readonly")

    modo_consumo_combo.bind("<Configure>", mostrar_campos_local)

    modo_consumo_combo.bind("<<ComboboxSelected>>", mostrar_campos_local)

    modo_entrega_label = tk.Label(form, bg=blanco, text="Modo de entrega:", font=("Gill Sans MT", 16))
    
    # Usar un ComboBox (ttk.Combobox) para el modo de entrega
    modo_entrega_values = ["Delivery", "Retira en local"]
    modo_entrega_combo = ttk.Combobox(form, values=modo_entrega_values, font=("Gill Sans MT", 16))

    modo_entrega_combo.bind("<Configure>", mostrar_campos_local)

    modo_entrega_combo.bind("<<ComboboxSelected>>", mostrar_campos_local)

    modo_entrega_combo.config(state="readonly")

    if op == 0:
        modo_entrega_combo.set(entrega_seleccionada)  # Establece el valor predeterminado (cambia [0] si es otro valor)
        tipo_entrada_combo.set(entrada_seleccionada)  # Establece el valor predeterminado (cambia [1] si es otro valor)

    # Resto de los campos de entrada
    nombre_cliente_label = tk.Label(form, bg=blanco, text="Nombre del cliente:", font=("Gill Sans MT", 16))
    nombre_cliente_entry = tk.Entry(form, font=("Gill Sans MT", 16), width=22)

    # Campos de teléfono y dirección (inicialmente ocultos)
    telefono_label = tk.Label(form, bg=blanco, text="Teléfono:", font=("Gill Sans MT", 16))
    telefono_entry = tk.Entry(form, font=("Gill Sans MT", 16), width=22)

    direccion_label = tk.Label(form, bg=blanco, text="Dirección:", font=("Gill Sans MT", 16))
    direccion_entry = tk.Entry(form, font=("Gill Sans MT", 16), width=22)

    producto_label = tk.Label(form, bg=blanco, text="Producto/s:", font=("Gill Sans MT", 16))
    producto_label.grid(row=7, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    productos_seleccionados_listbox = tk.Listbox(form, height=3, width=35, font=("Gill Sans MT", 14))
    productos_seleccionados_listbox.grid(row=7, column=1, sticky="w", padx=(5, 0))

    # Agrega un botón para limpiar la Listbox
    limpiar_button = tk.Button(form, text="Limpiar", cursor="hand2", font=("Gill Sans MT", 12), command=lambda: [productos_seleccionados.clear(), actualizar_lista_productos(), total_label.config(text="Total: $0.00")])
    limpiar_button.grid(row=8, column=1, sticky="w", padx=(5, 0), pady=10)

    descripcion_label = tk.Label(form, bg=blanco, text="Descripción:", font=("Gill Sans MT", 16))
    descripcion_label.grid(row=9, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    descripcion_text = tk.Text(form, font=("Gill Sans MT", 12), width=35, height=2)
    descripcion_text.grid(row=9, column=1, sticky="w", padx=(5, 10), pady=(10, 0))

    medio_pago_label = tk.Label(form, bg=blanco, text="Medio de pago:", font=("Gill Sans MT", 16))
    medio_pago_label.grid(row=10, column=0, sticky="e", padx=(10, 5), pady=(10, 0))

    # Usar un ComboBox (ttk.Combobox) para el medio de pago
    medio_pago_values = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito"]
    medio_pago_combo = ttk.Combobox(form, values=medio_pago_values, font=("Gill Sans MT", 16))
    medio_pago_combo.grid(row=10, column=1, sticky="w", padx=(5, 10), pady=(10, 0))
    medio_pago_combo.set(medio_pago_values[0])  # Establecer un valor predeterminado

    if op == 1:

        global tipo_entrada, modo_consumo, tipo_entrega, nombre, descripcion, direccion, telefono, medio_pago
            
        tipo_entrada_combo.set(tipo_entrada)  # Tipo de entrada

        modo_consumo_combo.set(modo_consumo)  # Modo de consumo

        modo_entrega_combo.set(tipo_entrega)  # Modo de entrega
        
        nombre_cliente_entry.delete(0, "end")
        nombre_cliente_entry.insert(0, nombre)  # Nombre del cliente

        telefono_entry.delete(0, "end")
        telefono_entry.insert(0, telefono)  # Teléfono

        direccion_entry.delete(0, "end")
        direccion_entry.insert(0, direccion)  # Dirección

        descripcion_text.delete("1.0", "end")
        descripcion_text.insert("1.0", descripcion)  # Descripción

        medio_pago_combo.set(medio_pago)  # Medio de pago

    def guardar_datos(op):
        global id_pedido_existente

        tipo_entrada = tipo_entrada_combo.get()
        modo_consumo = modo_consumo_combo.get()
        modo_entrega = modo_entrega_combo.get()
        nombre_cliente = nombre_cliente_entry.get()
        telefono = telefono_entry.get()
        direccion = direccion_entry.get()
        descripcion = descripcion_text.get("1.0", "end-1c")  # Obtiene el contenido del campo de descripción
        medio_pago = medio_pago_combo.get()

        if op == 0:
            modo_entrega = "Consume en local"
            nombre_cliente = "N/A"
            telefono = "N/A"
            direccion = "N/A"

            # Verificar que los campos no estén vacíos
            if (
                not tipo_entrada
                or not modo_consumo
                or not medio_pago
                or productos_seleccionados_listbox.size() == 0
                or not modo_entrega
            ):
                messagebox.showerror("Error", "Completa todos los campos para registrar el pedido.")
                return
            
        elif op == 1:
            telefono = "N/A"
            direccion = "N/A"
            # Verificar que los campos no estén vacíos
            if (
                not tipo_entrada
                or not modo_consumo
                or not modo_entrega
                or not nombre_cliente
                or productos_seleccionados_listbox.size() == 0
                or not medio_pago
            ):
                messagebox.showerror("Error", "Completa todos los campos para registrar el pedido.")
                return
        elif op == 2:
            # Verificar que los campos no estén vacíos
            if (
                not tipo_entrada
                or not modo_consumo
                or not modo_entrega
                or not nombre_cliente
                or not telefono
                or not direccion
                or productos_seleccionados_listbox.size() == 0
                or not medio_pago
            ):
                messagebox.showerror("Error", "Completa todos los campos para registrar el pedido.")
                return
        else:
            messagebox.showerror("Error", "Completa todos los campos para registrar el pedido.")
            return

        if not descripcion:
            descripcion="N/A"

        productos = productos_seleccionados_listbox.get(0, tk.END)
        productos_divididos = []

        for producto in productos:
            # Elimina "x2" si está presente en el nombre del producto
            if 'x2' in producto:
                producto_limpio = producto.replace(' x2', '')
                productos_divididos.append(producto_limpio)
                productos_divididos.append(producto_limpio)
            else:
                productos_divididos.append(producto)

        # Conecta a la base de datos (asegúrate de configurar los parámetros de conexión correctamente)
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lomiteria"
        )

        # Crea un cursor
        cursor = db.cursor()

        # Consultas SQL para obtener los IDs de las tablas relacionadas
        cursor.execute("SELECT id_modo_consumo FROM ModoConsumo WHERE nombre = %s", (modo_consumo,))
        id_modo_consumo = cursor.fetchone()[0]

        cursor.execute("SELECT id_tipo_entrada FROM TipoEntrada WHERE nombre = %s", (tipo_entrada,))
        id_tipo_entrada = cursor.fetchone()[0]

        cursor.execute("SELECT id_tipo_entrega FROM TipoEntrega WHERE nombre = %s", (modo_entrega,))
        id_tipo_entrega = cursor.fetchone()[0]

        if id_pedido_existente is not None:
        # Sentencia SQL para actualizar los datos del pedido
            update_query = (
                "UPDATE Pedido SET nombre_cliente = %s, total=%s, descripcion = %s, id_modo_consumo = %s, "
                "id_tipo_entrada = %s, id_tipo_entrega = %s, telefono = %s, direccion = %s, medio_pago = %s WHERE id_pedido = %s"
            )
            total, lista = calcular_precio_total()

            # Valores a actualizar en la tabla
            values = (nombre_cliente, total, descripcion, id_modo_consumo, id_tipo_entrada, id_tipo_entrega, telefono, direccion, medio_pago, id_pedido_existente)

            try:
                # Ejecuta la consulta SQL para actualizar el pedido existente
                cursor.execute(update_query, values)
            except Exception as e:
                print("Error al actualizar el pedido en la base de datos:", str(e))
            
            id_pedido_existente = None
        else:


            # Sentencia SQL para insertar los datos en la tabla Pedido
            insert_query = "INSERT INTO Pedido (nombre_cliente, descripcion, total, id_modo_consumo, id_tipo_entrada, id_tipo_entrega, telefono, direccion, medio_pago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            total, lista = calcular_precio_total()

            # Valores a insertar en la tabla
            values = (nombre_cliente, descripcion, total, id_modo_consumo, id_tipo_entrada, id_tipo_entrega, telefono, direccion, medio_pago)

            try:
                # Ejecuta la consulta SQL
                cursor.execute(insert_query, values)

                # Guarda los cambios en la base de datos
                db.commit()

                # Obtén el ID del pedido recién insertado
                id_pedido = cursor.lastrowid

            except Exception as e:
                print("Error al insertar en la base de datos:", str(e))
            
            # Crea un diccionario para rastrear la cantidad de cada producto
            cantidad_productos = {}

            # Recorre la lista de productos
            for producto in productos_divididos:
                # Consulta SQL para obtener el ID del producto por su nombre
                cursor.execute("SELECT id_producto FROM Producto WHERE Nombre = %s", (producto,))
                resultado = cursor.fetchone()

                if resultado:
                    id_producto = resultado[0]

                    # Si el producto ya está en el diccionario, aumenta la cantidad en 1
                    if id_producto in cantidad_productos:
                        cantidad_productos[id_producto] += 1
                    else:
                        cantidad_productos[id_producto] = 1

            # Ahora, inserta los datos en la tabla PedidoxProducto con las cantidades correctas
            for id_producto, cantidad in cantidad_productos.items():
                # Sentencia SQL para insertar los datos en la tabla PedidoxProducto
                insert_query = "INSERT INTO PedidoxProducto (id_pedido, id_producto, cantidad_producto) VALUES (%s, %s, %s)"

                # Valores a insertar en la tabla
                values = (id_pedido, id_producto, cantidad)

                try:
                    # Ejecuta la consulta SQL
                    cursor.execute(insert_query, values)

                    
                except Exception as e:
                    print("Error al insertar en la tabla PedidoxProducto:", str(e))
            
            guardar_productos_seleccionados(id_pedido)
                
    # Guarda los cambios en la base de datos
        db.commit()

        # Cierra la conexión a la base de datos
        db.close()

        ventana.destroy()
        create_window(1)


    registrar_button = tk.Button(form, text="Registrar", bg="#a5e872", cursor="hand2", font=("Gill Sans MT", 16), command=lambda:[guardar_datos(obtener_opcion())])
    registrar_button.grid(row=11, column=1, sticky="e", padx=(10, 5), pady=10)

    # Botón "Imprimir"
    imprimir_button = tk.Button(form, text="Imprimir", bg="#a1c2f7", cursor="hand2", font=("Gill Sans MT", 16), command=lambda:generar_pedido(ventana, obtener_opcion()))
    imprimir_button.grid(row=11, column=2, sticky="w", padx=(5, 10), pady=10)


    regresar_button = tk.Button(ventana, cursor="hand2", width=10, text="Regresar", bg="#e87e72", borderwidth=2, font=("Gill Sans MT", 20), relief="solid", command=lambda:[limpiar_variables(), ventana.destroy(),create_window(0)])
    regresar_button.grid(column=0,row=9)

    # Crear un Canvas como contenedor
    canvas = tk.Canvas(ventana)
    canvas.grid(row=0,column=0,sticky="nsew", columnspan=3, rowspan=8, padx=(20,20), pady=(20,0))

    # Crear un Scrollbar a la derecha del Canvas
    scrollbar = tk.Scrollbar(ventana, command=canvas.yview)
    scrollbar.grid(row=0, column=2, sticky="nse", rowspan=8, pady=(20,0), padx=(0,20))  # Ajuste la columna para colocarlo a la derecha
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
    preciox2_title.grid(row=0,column=3, padx=50, pady=10)


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
        precio_x2_label.grid(row=i+1, column=3, sticky="w", padx=50, pady=(0,10))

        if precio_x2 == "":
            precio_x2_label.config(text="") 
        
        agregar_button = tk.Button(productos_frame, text="+", font=("Gill Sans MT", 12, "bold"), relief="flat", cursor="hand2", command=lambda nombre=nombre: [agregar_producto(nombre), calcular_precio_total()])
        agregar_button.grid(row=i+1, column=0, sticky="e", padx=(30,0), pady=(0,10))
    
    # Actualiza el tamaño del canvas después de agregar elementos al frame
    productos_frame.update_idletasks()

    # Ajusta el tamaño del canvas al tamaño del frame
    canvas.config(scrollregion=canvas.bbox("all"))

    # Crear un frame para mostrar el total
    total_frame = tk.Frame(ventana, bg="lightblue")
    total_frame.grid(column=1, row=9, sticky="nsew", pady=(0,20), columnspan=2, padx=30)  # Espacio debajo del frame del formulario

    total_frame.rowconfigure(0, weight=1)  # Expande la fila 
    total_frame.columnconfigure(0, weight=1)  # Expande la columna

    # Etiqueta para mostrar el total
    total_label = tk.Label(total_frame, text="Total: $0.00", font=("Gill Sans MT", 30))
    total_label.grid(row=0,column=0)

    # Obtén la lista de productos con sus precios desde la función cargar_productos
    productos_con_precios = cargar_productos()

    # Crea un diccionario que asocie los nombres de los productos con sus precios
    productos_precios = {nombre: (precio_x1, precio_x2) for nombre, precio_x1, precio_x2 in productos_con_precios}

    lista_precios = []

    # Función para calcular el precio total
    def calcular_precio_total():
        precio_total = 0.0  # Inicializa como float
        lista_precios.clear()  # Limpia la lista de precios
        for producto in productos_seleccionados_listbox.get(0, tk.END):
            nombre_producto = producto.split(" x")[0]  # Elimina " x2" si está presente
            precio_x1, precio_x2 = productos_precios.get(nombre_producto, (0.0, 0.0))  # Inicializa como float
            cantidad = int(producto.split(" x")[1]) if " x" in producto else 1
            
            # Acumula el precio en cada iteración teniendo en cuenta la cantidad y si tiene precio x2
            if cantidad == 2 and precio_x2:
                precio_total += float(precio_x2)
                lista_precios.append(float(precio_x2))  # Agrega el precio a la lista
            else:
                precio_total += float(precio_x1)
                lista_precios.append(float(precio_x1))

        # Actualiza la etiqueta total_label con el precio total
        total_label.config(text=f"Total: ${precio_total:.2f}")
        return precio_total, lista_precios
    
    def obtener_opcion():
        # Obtén las selecciones de modo de consumo y modo de entrega
        modo_consumo = modo_consumo_combo.get()
        modo_entrega = modo_entrega_combo.get()

        # Establece la variable opcion según las condiciones
        if modo_consumo == "Mesa":
            opcion = 0
        elif modo_entrega == "Retira en local":
            opcion = 1
        elif modo_entrega == "Delivery":
            opcion = 2
        else:
            opcion = 3  # Establece una opción predeterminada en caso de que ninguna de las condiciones coincida

        return opcion
    
    def generar_pedido(form, op):
        # Obtener los valores de los campos
        tipo_entrada = tipo_entrada_combo.get()
        modo_consumo = modo_consumo_combo.get()
        modo_entrega = modo_entrega_combo.get()
        nombre_cliente = nombre_cliente_entry.get()
        telefono = telefono_entry.get()
        direccion = direccion_entry.get()
        descripcion = descripcion_text.get("1.0", "end-1c")  # Obtiene el contenido del campo de descripción
        medio_pago = medio_pago_combo.get()

        if op == 0:
            modo_entrega = "Consume en local"
            nombre_cliente = "N/A"
            telefono = "N/A"
            direccion = "N/A"

            # Verificar que los campos no estén vacíos
            if (
                not tipo_entrada
                or not modo_consumo
                or not medio_pago
                or productos_seleccionados_listbox.size() == 0
                or not modo_entrega
            ):
                messagebox.showerror("Error", "Completa todos los campos para imprimir el pedido.")
                return
            
        elif op == 1:
            telefono = "N/A"
            direccion = "N/A"
            # Verificar que los campos no estén vacíos
            if (
                not tipo_entrada
                or not modo_consumo
                or not modo_entrega
                or not nombre_cliente
                or productos_seleccionados_listbox.size() == 0
                or not medio_pago
            ):
                messagebox.showerror("Error", "Completa todos los campos para imprimir el pedido.")
                return
        elif op == 2:
            # Verificar que los campos no estén vacíos
            if (
                not tipo_entrada
                or not modo_consumo
                or not modo_entrega
                or not nombre_cliente
                or not telefono
                or not direccion
                or productos_seleccionados_listbox.size() == 0
                or not medio_pago
            ):
                messagebox.showerror("Error", "Completa todos los campos para imprimir el pedido.")
                return
        else:
            messagebox.showerror("Error", "Completa todos los campos para imprimir el pedido.")
            return

        if not descripcion:
            descripcion="N/A"

        ticket = tk.Toplevel(form)
        ticket.title("Ticket de Pedido")
        
        # Cambia el tamaño de la ventana antes de agregar elementos
        ticket.geometry("500x800")  # Ajusta las dimensiones según tus necesidades

       # Crea un Canvas que servirá como contenedor
        canvas = tk.Canvas(ticket)
        canvas.pack(side="left", fill="both", expand=True)

        # Agrega una barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(ticket, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configura el Canvas para utilizar la barra de desplazamiento
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crea un Frame que será contenido dentro del Canvas
        ticket_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=ticket_frame, anchor="nw")

        # Agregar los datos del pedido al ticket
        tk.Label(ticket_frame, text="Ticket de Pedido", font=("Gill Sans MT", 18)).grid(row=0, column=0, columnspan=2)

        tk.Label(ticket_frame, text=f"Tipo de entrada:", font=("Gill Sans MT", 14)).grid(row=1, column=0, sticky="w", pady=(0,20))
        tk.Label(ticket_frame, text=tipo_entrada, font=("Gill Sans MT", 14)).grid(row=1, column=1, sticky="w", pady=(0,20))

        tk.Label(ticket_frame, text=f"Modo de consumo:", font=("Gill Sans MT", 14)).grid(row=2, column=0, sticky="w", pady=(0,20))
        tk.Label(ticket_frame, text=modo_consumo, font=("Gill Sans MT", 14)).grid(row=2, column=1, sticky="w", pady=(0,20))

        tk.Label(ticket_frame, text=f"Modo de entrega:", font=("Gill Sans MT", 14)).grid(row=3, column=0, sticky="w", pady=(0,20))
        tk.Label(ticket_frame, text=modo_entrega, font=("Gill Sans MT", 14)).grid(row=3, column=1, sticky="w", pady=(0,20))

        tk.Label(ticket_frame, text=f"Nombre del cliente:", font=("Gill Sans MT", 14)).grid(row=4, column=0, sticky="w", pady=(0,20))
        tk.Label(ticket_frame, text=nombre_cliente, font=("Gill Sans MT", 14)).grid(row=4, column=1, sticky="w", pady=(0,20))

        if telefono:
            tk.Label(ticket_frame, text=f"Teléfono:", font=("Gill Sans MT", 14)).grid(row=5, column=0, sticky="w", pady=(0,20))
            tk.Label(ticket_frame, text=telefono, font=("Gill Sans MT", 14)).grid(row=5, column=1, sticky="w", pady=(0,20))

        if direccion:
            tk.Label(ticket_frame, text=f"Dirección:", font=("Gill Sans MT", 14)).grid(row=6, column=0, sticky="w", pady=(0,20))
            tk.Label(ticket_frame, text=direccion, font=("Gill Sans MT", 14)).grid(row=6, column=1, sticky="w", pady=(0,20))
    
        tk.Label(ticket_frame, text=f"Descripción:", font=("Gill Sans MT", 14)).grid(row=7, column=0, sticky="w", pady=(20,0))
        tk.Label(ticket_frame, text=descripcion, font=("Gill Sans MT", 14)).grid(row=7, column=1, sticky="w", pady=(20,0))

        tk.Label(ticket_frame, text=f"Medio de pago:", font=("Gill Sans MT", 14)).grid(row=8, column=0, sticky="w", pady=(20,20))
        tk.Label(ticket_frame, text=medio_pago, font=("Gill Sans MT", 14)).grid(row=8, column=1, sticky="w", pady=(20,20))

        precio_total,lista_precios = calcular_precio_total()
        tk.Label(ticket_frame, text="Productos:", font=("Gill Sans MT", 14)).grid(row=9, column=0, sticky="w", pady=(0,20))

        row_num = 10
        for producto, precio in zip(productos_seleccionados, lista_precios):
            tk.Label(ticket_frame, text=producto, font=("Gill Sans MT", 14)).grid(row=row_num, column=0, sticky="w")
            tk.Label(ticket_frame, text=f"${precio:.2f}", font=("Gill Sans MT", 14)).grid(row=row_num, column=1, sticky="w", padx=(20,0))
            row_num += 1

        ancho_ticket = ticket.winfo_width()
        linea = "-" * 60

        tk.Label(ticket_frame, text=linea, font=("Gill Sans MT", 14)).grid(row=row_num, column=0, columnspan=2)

        tk.Label(ticket_frame, text="Total:", font=("Gill Sans MT", 14)).grid(row=row_num+1, column=0, sticky="w")

        tk.Label(ticket_frame, text=f"${precio_total}", font=("Gill Sans MT", 14)).grid(row=row_num+1, column=1, sticky="w", padx=(20,0))

        # Agregar un botón para cerrar el ticket
        cerrar_button = tk.Button(ticket_frame, font=("Gill Sans MT", 12), cursor="hand2", text="Cerrar", command=ticket.destroy)
        cerrar_button.grid(row=row_num + 2, column=0, columnspan=2, pady=(0,20))

        # Ajusta el tamaño del Canvas cuando el contenido cambia
        ticket_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        ticket_frame.grid_columnconfigure(0, weight=1)
        ticket_frame.grid_columnconfigure(1, weight=1)

def create_window(op=0):

    global pedidos, pedidos_pendientes
    
    principal = tk.Tk()
    principal.state('zoomed')
    principal.config(bg= blanco)
    screen_width = principal.winfo_screenwidth()
    bandeja_color = "#a1c2f7"
    # Convierte la imagen a un formato compatible con tkinter
    avatar = ImageTk.PhotoImage(image)

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

    # Crear un widget Label para mostrar la imagen
    label = tk.Label(principal, image=avatar, bg="#fcebeb")
    label.grid(row=2, column=4, columnspan=2, rowspan=2)

    cUser_button = tk.Button(principal, cursor="hand2", text="Cambiar usuario",font=("Gill Sans MT", 20), bg=amarillo, relief="solid", borderwidth=2, command = lambda: crear_ventana_secundaria(principal))
    cUser_button.grid(row=5,column=4,ipadx=20, columnspan=2, pady=(40,10))

    userN_label = tk.Label(principal, text=f"{nombre_usuario}",font=("Gill Sans MT", 14), bg="#fcebeb")
    userN_label.grid(row=4,column=4,sticky="n", columnspan=2, pady=(10,0))

    
    pedidos = cargar_pedidos()
    # Filtra los productos con entregado en 0
    pedidos_pendientes = [pedido for pedido in pedidos if pedido[4] == 0 and pedido[5] == 0]

    crear_pedido(principal, bandeja_frame, bandeja_color)

    principal.mainloop()



def crear_pedido(ventana, frame, color):
    global pedidos_pendientes

    def actualizar_tiempo(ventana, label, hora_registro):
        if label.winfo_exists() and ventana.winfo_exists():  # Verifica si el label y la ventana todavía existen
            hora_actual = datetime.now()
            
            # Calcula la diferencia de tiempo
            diferencia = hora_actual - hora_registro

            # Calcula horas, minutos y segundos
            segundos_totales = diferencia.total_seconds()
            horas, segundos_totales = divmod(segundos_totales, 3600)
            minutos, segundos = divmod(segundos_totales, 60)

            # Formatea los valores con dos dígitos
            horas_str = f'{int(horas):02}'
            minutos_str = f'{int(minutos):02}'
            segundos_str = f'{int(segundos):02}'

            # Construye la cadena de tiempo en el formato deseado
            tiempo_transcurrido = f"{horas_str}:{minutos_str}:{segundos_str}"

            # Luego, establece el texto en la etiqueta tiempo_label
            label.config(text=tiempo_transcurrido)

            # Programa la siguiente actualización después de 1000 ms (1 segundo)
            ventana.after(1000, lambda: actualizar_tiempo(ventana, label, hora_registro))

    pedido_font = ("Gill Sans MT", 10)
    eliminar_widgets(frame)
    bandeja_title = ttk.Label(frame, text="Bandeja de pendientes", style='Subrayado.TLabel', background=color)
    bandeja_title.grid(row=0, column=0, columnspan=6)
    frame.columnconfigure(0, weight=1)
    row = 1
    for pedido in pedidos_pendientes:
        nuevo_pedido_frame = tk.Frame(frame, bg=color, padx=10, pady=5, borderwidth=2, relief="solid")
        nuevo_pedido_frame.grid(row=row, column=0, columnspan=6, padx=(5, 5), pady=(5, 5))

        pedido_label = tk.Label(nuevo_pedido_frame, text=f"Pedido # {pedido[0]}", cursor="hand2", background=color, font=("Gill Sans MT", 10, "bold"))
        tiempo_label = tk.Label(nuevo_pedido_frame, text="00:00", background=color, font=("Gill Sans MT", 10, "bold"))
        entregar_button = tk.Button(nuevo_pedido_frame, text="ENTREGAR", cursor="hand2", relief="flat", font=pedido_font, command=lambda id_pedido=pedido[0]: [entregar_pedido(id_pedido), crear_pedido(ventana, frame, color)])
        modificar_button = tk.Button(nuevo_pedido_frame, text="MODIFICAR", cursor="hand2", relief="flat", font=pedido_font,  command=lambda id_pedido=pedido[0]: (llenar_formulario(id_pedido), menu_pedido2(ventana, 1), cargar_productos_seleccionados(id_pedido)))

        cancelar_button = tk.Button(nuevo_pedido_frame, text="CANCELAR", cursor="hand2", relief="flat", font=pedido_font, command=lambda id_pedido=pedido[0]: [cancelar_pedido(id_pedido), crear_pedido(ventana, frame, color)])
        imprimir_button = tk.Button(nuevo_pedido_frame, text="IMPRIMIR", cursor="hand2", relief="flat", font=pedido_font)

        pedido_label.grid(row=row, column=0, padx=(0,10))
        tiempo_label.grid(row=row, column=1, padx=(0,10))
        entregar_button.grid(row=row, column=2, padx=(0,10))
        modificar_button.grid(row=row, column=3, padx=(0,10))
        cancelar_button.grid(row=row, column=4, padx=(0,10))
        imprimir_button.grid(row=row, column=5)
        row += 1

        # Inicializa la actualización de tiempo para esta etiqueta de tiempo
        actualizar_tiempo(ventana, tiempo_label, pedido[6])  # 6 es el índice de la columna de fecha de registro

    