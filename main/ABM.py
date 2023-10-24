import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conexion = mysql.connector.connect(host="localhost", user="root", password="", database="lomiteria")

root = tk.Tk()
root.title("Sistema de gestion")
root.resizable(0,0)

amarillo = "#e6a902"
rojo = "#e60707"
blanco = "#fcebeb"

root.config(bg="")

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
