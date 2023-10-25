import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def create_window(root, op):
    if op == 0:
        
        principal = tk.Toplevel(root)
        principal.state('zoomed')
        screen_width = root.winfo_screenwidth()
        for row in range(10):
            for column in range(6):
                crear_celda(principal, row, column, all_columns=6 , color="white", padx=(10,10), pady=(20,10), height=70)
        title_lab = tk.Label(principal, text="Lomitos X2", font=("Gill Sans MT", 32))
        title_lab.grid(row=0,column=2,columnspan=2)
        title2_lab = tk.Label(principal, text="HADLER\nSistema de gestión", font=("Gill Sans MT", 20))
        title2_lab.grid(row=0,column=0, sticky="n")

        bandeja_frame = tk.Frame(principal,bg="green", borderwidth=3, relief="solid")
        bandeja_frame.grid(row=1,column=0, rowspan=8, columnspan=2, padx=20, pady=20, sticky="nsew")

        for row in range(11):
            for column in range(6):
                crear_celda(bandeja_frame, row, column, all_columns=6 , color="red", padx=(10,10), pady=(20,10), height=40, width=85, op=1)
        
        pedido = tk.Label(bandeja_frame, text="Pedido 2314")
        pedido.grid(row=0,column=0)

        tiempo = tk.Label(bandeja_frame, text="00:09")
        tiempo.grid(row=0,column=1)

        entregar = tk.Button(bandeja_frame, text="ENTREGAR", relief="flat")
        entregar.grid(row=0,column=2)

        modificar = tk.Button(bandeja_frame, text="MODIFICAR", relief="flat")
        modificar.grid(row=0,column=3)

        cancelar = tk.Button(bandeja_frame, text="CANCELAR", relief="flat")
        cancelar.grid(row=0,column=4)

        imprimir = tk.Button(bandeja_frame, text="IMPRIMIR", relief="flat")
        imprimir.grid(row=0,column=5)

        """bandeja_title = tk.Label(bandeja_frame, text="Bandeja de pendientes", font= ("Gill Sans MT", 20, "bold"), bg="green")
        bandeja_title.grid(row=0, column=0)"""


        """pedido_label = tk.Label(bandeja_frame, text="Pedido 1", font= ("Gill Sans MT", 12, "bold"), bg="green")
        pedido_label.grid(row=1,column=0)"""

        principal.mainloop()

def crear_celda(ventana, row, column, all_columns, color, padx, pady, width=200, height=30, op=0):
    if op == 0:
        screen_width = ventana.winfo_screenwidth()
        width = (screen_width-((padx[0] + padx[1])*all_columns))/all_columns
    celda = tk.Frame(ventana, width=width,height=height, bg=color)#,borderwidth=1, relief='solid'
    celda.grid(row=row, column=column, pady=pady, padx=padx)
    return celda
    (1080 - (20*9))/9
