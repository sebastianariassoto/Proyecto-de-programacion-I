"""
cliente.py
Clase Cliente — nombre y estrato.
Adaptado para Flask: sin prints de consola.
"""

DESCUENTOS_ESTRATO = {1: 10, 2: 5, 3: 2}


class Cliente:
    def __init__(self, nombre, estrato):
        self.nombre  = nombre.strip().title()
        self.estrato = int(estrato)

    def descuento_pct(self):
        return DESCUENTOS_ESTRATO.get(self.estrato, 0)

    def to_dict(self):
        return {
            "nombre":       self.nombre,
            "estrato":      self.estrato,
            "descuento_pct": self.descuento_pct(),
        }
