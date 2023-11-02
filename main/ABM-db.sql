CREATE DATABASE IF NOT EXISTS Lomiteria;
USE Lomiteria;

CREATE TABLE IF NOT EXISTS TipoProducto (
    ID_TIPO INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Producto (
    ID_PRODUCTO INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion VARCHAR(255),
    ID_TIPO INT,
    PrecioUnitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID_TIPO) REFERENCES TipoProducto (ID_TIPO)
);

CREATE TABLE IF NOT EXISTS Promocion (
    ID_PROMOCION INT AUTO_INCREMENT PRIMARY KEY,
    ID_PRODUCTO INT NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID_PRODUCTO) REFERENCES Producto (ID_PRODUCTO)
);

CREATE TABLE IF NOT EXISTS ModoConsumo (
    id_modo_consumo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

INSERT INTO ModoConsumo (nombre) VALUES
    ('Mesa'),
    ('Fuera del local');


CREATE TABLE IF NOT EXISTS TipoEntrada (
    id_tipo_entrada INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

INSERT INTO TipoEntrada (nombre) VALUES
    ('Local'),
    ('Teléfono'),
    ('Whatsapp'),
    ('Pedidos Ya'),
    ('Rappi');

CREATE TABLE IF NOT EXISTS TipoEntrega (
    id_tipo_entrega INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

INSERT INTO TipoEntrega (nombre) VALUES
    ('Delivery'),
    ('Retira en local');

CREATE TABLE IF NOT EXISTS Pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(255),
    descripcion VARCHAR(255),
    total DECIMAL(10, 2) NOT NULL,
    id_modo_consumo INT,
    id_tipo_entrada INT,
    id_tipo_entrega INT,
    telefono VARCHAR(255),
    direccion VARCHAR(255),
    medio_pago VARCHAR(255),
    entregado BOOLEAN DEFAULT 0,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Agregar la columna fecha_registro
    FOREIGN KEY (id_modo_consumo) REFERENCES ModoConsumo(id_modo_consumo),
    FOREIGN KEY (id_tipo_entrada) REFERENCES TipoEntrada(id_tipo_entrada),
    FOREIGN KEY (id_tipo_entrega) REFERENCES TipoEntrega(id_tipo_entrega)
);

CREATE TABLE IF NOT EXISTS PedidoxProducto (
    id_pedido INT,
    id_producto INT,
    cantidad_producto INT NOT NULL,
    PRIMARY KEY (id_pedido, id_producto),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);

CREATE TABLE IF NOT EXISTS Promocion2x1 (
    ID_PROMOCION2X1 INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Producto1 INT NOT NULL,
    Producto2 INT NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Producto1) REFERENCES Producto (ID_PRODUCTO),
    FOREIGN KEY (Producto2) REFERENCES Producto (ID_PRODUCTO)
);

INSERT INTO TipoProducto (Nombre)
VALUES ('Lomos'), ("Milanesa"), ("Hamburguesas"), ("Empanadas"), ("Pizzas"), ("Papas"), ("Otros"), ("Promos");

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Lomo Grande - Carne', 'Con lechuga, tomate, jamón, queso, huevo, mayonesa y papas', 1, 3200);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Lomo Grande - Pollo/Cerdo', 'Con lechuga, tomate, jamón, queso, huevo, mayonesa y papas', 1, 3100);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Lomo Chico', 'Con lechuga, tomate, jamón, queso, huevo, mayonesa y papas', 1, 2800);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Sandwich de milanesa', 'MILANESA: Con lechuga, tomate, jamón, queso, huevo, mayonesa y papas', 2, 3200);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Milanesa', 'Napolitina - A caballo - Fugazza c/Papas Fritas', 2, 2300);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Mila Grosa', 'Milanesa, salsa, muzza, jamón, cebolla a la plancha, orégano, huevo frito, con papas y pan', 2, 2500);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Hamburguesa simple', 'Con papas', 3, 2400);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Hamburguesa doble', 'Con papas', 3, 3100);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Empanadas (unidad)', 'Árabes/Criollas/Jamon y queso/Queso y cebolla/...', 4, 400);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Empanadas (docena)', 'Árabes/Criollas/Jamon y queso/Queso y cebolla/...', 4, 4400);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Pizza Especial/Fugazza/Napolitana', '', 5, 3000);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Media Pizza Especial/Fugazza/Napolitana', '', 5, 2000);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Pizza Muzzarella', '', 5, 2700);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Media Pizza Muzzarella', '', 5, 1800);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Pizza-lomo s/Papas', 'Dos pizzas con carne de lomo al medio, con lechuga, tomate, sin papas', 5, 7700);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Media Pizza-lomo s/Papas', 'A la mitad, dos pizzas con carne de lomo al medio, con lechuga, tomate, sin papas', 5, 4200);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Pizza-lomo c/Papas', 'Dos pizzas con carne de lomo al medio, con lechuga, tomate, con papas', 5, 8000);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Media Pizza-lomo c/Papas', 'A la mitad, dos pizzas con carne de lomo al medio, con lechuga, tomate, con papas', 5, 4600);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Papas chicas', '', 6, 1600);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Papas grandes', '', 6, 1800);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Papas con cheddar', '', 6, 2400);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Papas con huevo', '', 6, 2200);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Papas con huevo y queso', '', 6, 2400);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Fajitas p/2 personas', '', 7, 5500);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Gaseosa o cerveza 1,5L', '', 7, 1400);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('Gaseosa 500ml', '', 7, 700);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('2 lomos + 2 hamburguesas', 'Con papas', 8, 8200);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('2 lomos grandes + 2 lomos chicos', 'Con papas', 8, 8500);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('1 Muzza + 6 Empanadas surtidas', '', 8, 5200);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('1 Muzza + 1 Especial', '', 8, 5500);

INSERT INTO Producto (Nombre, Descripcion, ID_TIPO, PrecioUnitario)
VALUES ('2 pizzas a eleccion', 'Especial-Fugazza-Napo', 8, 5700);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Lomo Grande 2x1 - Carne", 1, 1, 5700);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Lomo Grande 2x1 - Pollo/Cerdo", 2, 2, 5600);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Lomo Chico 2x1", 3, 3, 4400);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Sandwich de mila 2x1", 4, 4, 5600);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Milanesa 2x1", 5, 5, 4400);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Hamburguesa simple 2x1", 7, 7, 4200);

INSERT INTO Promocion2x1 (Nombre, Producto1, Producto2, Precio)
VALUES ("Hamburguesa doble 2x1", 8, 8, 5000);