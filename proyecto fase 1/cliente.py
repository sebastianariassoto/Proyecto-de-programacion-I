"""
cliente.py — Estanquillo Gloriana

Descuento por estrato:
  Estrato 1 -> 10%
  Estrato 2 ->  5%
  Estrato 3 ->  2%
  Estrato 4+ ->  0%
"""

DESCUENTOS_ESTRATO = {1: 10, 2: 5, 3: 2}


class Cliente:
    def __init__(self, nombre, estrato):
        self.nombre  = nombre.strip().title()
        self.estrato = int(estrato)

    def descuento_pct(self):
        return DESCUENTOS_ESTRATO.get(self.estrato, 0)
