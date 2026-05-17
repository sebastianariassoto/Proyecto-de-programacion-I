"""
producto.py
Clase Producto para Estanquillo Gloriana.
"""

PRESENTACIONES_BEBIDAS = {
    "1": "200ml",
    "2": "500ml",
    "3": "1L",
    "4": "2L",
}

TALLAS_SNACKS = {
    "1": "Pequeño",
    "2": "Mediano",
    "3": "Grande",
}

CATEGORIAS = {
    "1": "Bebidas",
    "2": "Licores",
    "3": "Cigarrillos",
    "4": "Snacks",
}

CATEGORIAS_CON_IVA  = {"Bebidas", "Snacks"}
PALABRAS_DESC_PROD  = ["chocolate", "chocolatina", "papa"]
DESCUENTO_PROD_PCT  = 10


class Producto:
    _contador = 1

    @classmethod
    def _nuevo_codigo(cls):
        cod = cls._contador
        cls._contador += 1
        return cod

    def __init__(self, nombre, categoria, precio, cantidad,
                 presentacion=None, codigo=None):
        self.codigo       = codigo if codigo is not None else Producto._nuevo_codigo()
        self.nombre       = nombre.strip()
        self.categoria    = categoria
        self.precio       = float(precio)
        self.cantidad     = int(cantidad)
        self.presentacion = presentacion
        self.tiene_iva    = categoria in CATEGORIAS_CON_IVA

    @property
    def nombre_completo(self):
        if self.presentacion:
            return f"{self.nombre} ({self.presentacion})"
        return self.nombre

    def tiene_descuento_categoria(self):
        return any(p in self.nombre.lower() for p in PALABRAS_DESC_PROD)

    def vender(self, unidades):
        if self.cantidad <= 0:
            print(f"\n  ⚠  '{self.nombre_completo}' está AGOTADO.")
            return False
        if unidades > self.cantidad:
            print(f"\n  ⚠  Stock insuficiente. Solo hay {self.cantidad} unidad(es).")
            return False
        self.cantidad -= unidades
        return True

    def reabastecer(self, unidades):
        self.cantidad += int(unidades)
        print(f"  ✔  '{self.nombre_completo}' reabastecido → Stock: {self.cantidad}")
