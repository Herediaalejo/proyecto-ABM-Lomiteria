productos = ('Lomo Grande - Carne', 'Lomo Grande - Pollo/Cerdo x2', 'Milanesa', 'Mila Grosa')

productos_divididos = []

for producto in productos:
    # Elimina "x2" si está presente en el nombre del producto
    producto_limpio = producto.replace(' x2', '')

    if 'x2' in producto:
        # Divide el producto
        partes = producto_limpio.split(' - ')
        producto1 = partes[0] + ' - ' + partes[1]
        producto2 = partes[0] + ' - ' + partes[1]

        productos_divididos.extend([producto1, producto2])
    else:
        productos_divididos.append(producto_limpio)

print(productos_divididos)