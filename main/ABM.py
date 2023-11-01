import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Funciones as f

#conexion = mysql.connector.connect(host="localhost", user="root", password="", database="lomiteria")

root = tk.Tk()
root.title("Sistema de gestion")

amarillo = "#e6a902"
rojo = "#e60707"
blanco = "#fcebeb"
verde = "#4ab56e"

empresa = "Lomitos X2"
title_font = ("Gill Sans MT", 20)

root.state('zoomed')

root.config(bg=blanco)

style = ttk.Style()

style.configure("TFrame", background=verde, width=400, height=600)

root.grid_columnconfigure(0, weight=1)  # Configura la columna 0 para que ocupe todo el espacio disponible

title1 = tk.Label(root, text="Bienvenido al sistema de gestion HADLER", font=title_font, bg=blanco)
title1.grid(row=0, column=0, sticky="ew", pady=(30,80))

frame = tk.Frame(root, bg=verde, borderwidth=3, relief="solid")
frame.grid(row=2, column=0)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

title2 = tk.Label(frame, text=empresa, font= ("Gill Sans MT", 20, "bold"), bg=verde)
title2.grid(row=0,column=0, sticky="ew", pady=(20,0), columnspan=2)

usuario_label = tk.Label(frame, text="Usuario", font=("Gill Sans MT", 16), bg=verde)
usuario_label.grid(row=1,column=0, pady=(20,10), columnspan=2)

usuario_select = ttk.Combobox(frame, font=("Gill Sans MT", 16), state="readonly")
usuario_select.grid(row=2,column=0, pady=(0,30), padx=(50,0))

add_usuario = tk.Button(frame, text="+", font=("Gill Sans MT", 11, "bold"), relief="flat")
add_usuario.grid(row=2,column=1,sticky="NW", ipadx=5, padx=(10,50))

password_label = tk.Label(frame, text="Contraseña", font=("Gill Sans MT", 16), bg=verde)
password_label.grid(row=3, column=0, pady=(0, 10), columnspan=2)

password_input = tk.Entry(frame, font=("Arial", 18), show="*", width=22)
password_input.grid(row=4,column=0,pady=(0, 30), columnspan=2, padx=(50,50))

usuario_select['values'] = ('Guillermo', 'Agostina', 'Franco', 'Lucas')

ingreso_button = tk.Button(frame, text="INGRESAR", cursor="hand2", relief="flat", font=("Consolas", 14, "bold"), background=amarillo, command=lambda:f.ingresar(root))
ingreso_button.grid(row=5,column=0, pady=(0,20), columnspan=2)


root.mainloop()


"""
SQL

Create database LOMITERIA; 

Use LOMITERIA; 

Create table cliente ( 

Codcliente int auto_incremente; 

Nombre varchar (150) not null, 

Apellido varchar (150) not null, 

Dirección varchar (150) not null, 

Teléfono int not null, 

Primary key (Codcliente)); 

  

Create table empleado ( 

Codempleado int auto_increment, 

Nombre varchar (150) not null, 

Apellido varchar (150) not null, 

DNI int not null, 

Dirección varchar (150) not null, 

Teléfono int not null, 

Primary key (Codempleado)); 



Create table producto ( 

Codproducto int auto_incremente; 

Nombre varchar (150) not null, 

Precio int not null, 

Stock int not null, 

Primary key (Codproducto)); 

  

Create table pedido ( 

Codpedido int auto_incremente, 

Nombre varchar (150) not null, 

Descripción varchar (150) not null, 

Cantidad int not null, 

Monto int not null, 

Modo de consumo varchar (150),

Modo de entrada varchar (150),

Modo de entrega varchar (150),

Primary key (Codpedido)); 

  

Create table proveedores ( 

Codproveedores int auto_increment, 

Nombre varchar (150) not null, 

Apellido varchar (150) not null, 

Dirección varchar (150) not null, (DEL LOCAL) 

Teléfono int not null, 

Primary key (Codproveedores)); 

  

Create table pagos ( 

Codpagos int auto_increment, 

Nombre varchar (150) not null, 

Monto int not null, 

Primary key (Codpagos)); 


Create table compra ( 

Codcompra int auto_increment, 

Nombre varchar (150) not null, 

Precio int not null, 

Stock int not null,  

Codproveedores int not null,  

Codproducto int not null,  

Primary key (Codpagos) 

Foreign key (codproveedores) referecences Proveedores (Codproveedores) 

Foreign key (codproducto) references Producto (Codproducto)); 

  

Create table comanda ( 

CodComanda int auto_increment, 

Precio varchar (150) not null, 

Subtotal int not null,  

Total int not null, 

Medio de pago int not null,  

Detalle varchar (150) not null,  

Codproducto int, 

Codcliente int, 

Primary key (Codpagos), 

Foreign key (Codproducto) references producto (Codproducto), 

Foreign key (Codcliente) references cliente (Codcliente)); 

  
Create table venta ( 

CodVenta int auto_increment, 

Fecha date varchar (150) not null, 

Total int not null, 

CodCliente int, 

Primary key (Codventa), 

Foreign key (Codcliente) references cliente (Codcliente)); 

  

Create table detalle de venta ( 

Coddetalledeventa int auto_increment, 

Precio varchar (150) not null, 

Cantidad int not null,  

Subtotal int not null, 

Codproducto int, 

Codventa int, 

Primary key (Coddetalledeventa), 

Foreign key (Codproducto) references producto (Codproducto), 

Foreign key (Codventa) references venta(Codventa)); 

"""
