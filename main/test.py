import tkinter as tk
from tkinter import ttk

def verificar_valor(event):
    if combobox.get() == "Valor 3":
        ventana.destroy()

ventana = tk.Tk()
ventana.title("Ejemplo ComboBox con Verificación")

combobox = ttk.Combobox(ventana, values=["Valor 1", "Valor 2", "Valor 3"])
combobox.pack(padx=10, pady=10)

entry = tk.Entry(ventana)
entry.pack(padx=10, pady=10)

boton_insertar = tk.Button(ventana, text="Insertar valor", command=lambda: combobox.set(entry.get()))
boton_insertar.pack(padx=10, pady=10)

# Asociar el evento <FocusOut> al ComboBox
combobox.bind("<FocusOut>", verificar_valor)

ventana.mainloop()