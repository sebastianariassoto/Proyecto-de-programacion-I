"""
cliente.py
Clase Cliente — solo pide nombre y estrato.
El estrato determina el descuento sobre el total de la venta.

Estrato 1 → 10%
Estrato 2 →  5%
Estrato 3 →  2%
Estrato 4+ →  0%
"""

DESCUENTOS_ESTRATO = {1: 10, 2: 5, 3: 2}


class Cliente:
    def __init__(self, nombre, estrato):
        self.nombre  = nombre.strip().title()
        self.estrato = int(estrato)

    def descuento_pct(self):
        return DESCUENTOS_ESTRATO.get(self.estrato, 0)

    def mostrar_datos(self):
        d = self.descuento_pct()
        print(f"  Cliente : {self.nombre}")
        print(f"  Estrato : {self.estrato}  →  Descuento total: {d}%")
