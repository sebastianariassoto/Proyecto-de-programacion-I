"""
estanquillo.py
Clase Estanquillo Gloriana.
Adaptado para Flask: sin prints, métodos retornan datos.
Todo en memoria RAM.
"""

from producto import (Producto, CATEGORIAS, PRESENTACIONES_BEBIDAS,
                      TALLAS_SNACKS, CATEGORIAS_CON_IVA)

CATEGORIAS_ORDEN = ["Bebidas", "Licores", "Cigarrillos", "Snacks"]


class Estanquillo:
    NOMBRE = "Gloriana"
    

    def __init__(self):
        Producto._contador = 1
        self.productos = []
        self._cargar_inventario_inicial()

    def _cargar_inventario_inicial(self):
        inicial = [
            ("Coca-Cola",               "Bebidas",     2000, 30, "200ml"),
            ("Coca-Cola",               "Bebidas",     3500, 20, "500ml"),
            ("Coca-Cola",               "Bebidas",     5500, 15, "1L"),
            ("Coca-Cola",               "Bebidas",     8000, 10, "2L"),
            ("Manzana Postobón",        "Bebidas",     1800, 30, "200ml"),
            ("Manzana Postobón",        "Bebidas",     3200, 20, "500ml"),
            ("Manzana Postobón",        "Bebidas",     5000, 10, "1L"),
            ("Manzana Postobón",        "Bebidas",     7500,  8, "2L"),
            ("Sprite",                  "Bebidas",     2000, 25, "200ml"),
            ("Sprite",                  "Bebidas",     3500, 18, "500ml"),
            ("Sprite",                  "Bebidas",     5500, 12, "1L"),
            ("Sprite",                  "Bebidas",     8000,  8, "2L"),
            ("Agua Cristal",            "Bebidas",     1500, 40, "200ml"),
            ("Agua Cristal",            "Bebidas",     2500, 30, "500ml"),
            ("Agua Cristal",            "Bebidas",     3800, 20, "1L"),
            ("Agua Cristal",            "Bebidas",     5500, 12, "2L"),
            ("Aguardiente Antioqueño",  "Licores",    12000, 15, "200ml"),
            ("Aguardiente Antioqueño",  "Licores",    22000, 10, "500ml"),
            ("Aguardiente Antioqueño",  "Licores",    38000,  8, "1L"),
            ("Aguardiente Néctar",      "Licores",    12000, 12, "200ml"),
            ("Aguardiente Néctar",      "Licores",    22000,  8, "500ml"),
            ("Aguardiente Néctar",      "Licores",    40000,  5, "1L"),
            ("Cerveza Club Colombia",   "Licores",     3500, 48, "200ml"),
            ("Ron Viejo de Caldas",     "Licores",    15000, 10, "200ml"),
            ("Ron Viejo de Caldas",     "Licores",    28000,  6, "500ml"),
            ("Cigarrillo Marlboro",     "Cigarrillos", 1000,100, None),
            ("Cigarrillo Pielroja",     "Cigarrillos",  700,100, None),
            ("Chocolatina Jet",         "Snacks",      1200, 40, "Pequeño"),
            ("Chocolatina Jet",         "Snacks",      2500, 30, "Mediano"),
            ("Chocolatina Jet",         "Snacks",      4500, 20, "Grande"),
            ("Chocolatina Corona",      "Snacks",      1500, 35, "Pequeño"),
            ("Chocolatina Corona",      "Snacks",      3000, 25, "Mediano"),
            ("Chocolatina Corona",      "Snacks",      5500, 15, "Grande"),
            ("Papas Margarita",         "Snacks",      1500, 50, "Pequeño"),
            ("Papas Margarita",         "Snacks",      3000, 35, "Mediano"),
            ("Papas Margarita",         "Snacks",      5000, 20, "Grande"),
            ("Papas De Todito",         "Snacks",      1800, 40, "Pequeño"),
            ("Papas De Todito",         "Snacks",      3500, 28, "Mediano"),
            ("Papas De Todito",         "Snacks",      5500, 15, "Grande"),
        ]
        for nombre, cat, precio, cant, pres in inicial:
            p = Producto(nombre, cat, precio, cant, presentacion=pres)
            self.productos.append(p)

    # ── búsqueda ──────────────────────────────────────────────────────────
    def buscar_producto(self, codigo):
        try:
            cod = int(codigo)
        except (ValueError, TypeError):
            return None
        for p in self.productos:
            if p.codigo == cod:
                return p
        return None

    # ── gestión ───────────────────────────────────────────────────────────
    def agregar_producto(self, nombre, categoria, precio, cantidad, presentacion=None):
        p = Producto(nombre, categoria, float(precio), int(cantidad),
                     presentacion=presentacion)
        self.productos.append(p)
        return p

    def reabastecer(self, codigo, unidades):
        p = self.buscar_producto(codigo)
        if p:
            nuevo_stock = p.reabastecer(unidades)
            return p, nuevo_stock
        return None, None

    # ── vistas como listas de dicts (para Jinja2) ─────────────────────────
    def catalogo_por_categoria(self):
        """Retorna dict {categoria: [producto.to_dict(), ...]} solo con stock > 0."""
        resultado = {}
        for cat in CATEGORIAS_ORDEN:
            prods = [p.to_dict() for p in self.productos
                     if p.categoria == cat and p.cantidad > 0]
            if prods:
                resultado[cat] = prods
        return resultado

    def inventario_por_categoria(self):
        """Retorna dict {categoria: [producto.to_dict(), ...]} completo."""
        resultado = {}
        for cat in CATEGORIAS_ORDEN:
            prods = [p.to_dict() for p in self.productos if p.categoria == cat]
            if prods:
                resultado[cat] = prods
        return resultado

    def todos_los_productos(self):
        return [p.to_dict() for p in self.productos]

    def total_referencias(self):
        return len(self.productos)
