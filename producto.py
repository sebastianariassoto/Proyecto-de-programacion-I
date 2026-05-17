"""
producto.py
Clase Producto para Estanquillo Gloriana.

Presentaciones para BEBIDAS (Licores incluidos):
    200ml | 500ml | 1L | 2L

Tallas para SNACKS:
    Pequeño | Mediano | Grande

Categorías y su IVA:
    Bebidas     → IVA 19%
    Licores     → sin IVA
    Cigarrillos → sin IVA
    Snacks      → IVA 19%

Descuento especial de categoría (10% sobre el ítem):
    Aplica si el nombre contiene: "chocolate", "chocolatina", "papa"
"""

# ── Constantes de presentación ──────────────────────────────────────────
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

# ── Categorías disponibles ───────────────────────────────────────────────
CATEGORIAS = {
    "1": "Bebidas",
    "2": "Licores",
    "3": "Cigarrillos",
    "4": "Snacks",
}

CATEGORIAS_CON_IVA   = {"Bebidas", "Snacks"}
PALABRAS_DESC_PROD   = ["chocolate", "chocolatina", "papa"]
DESCUENTO_PROD_PCT   = 10   # % de descuento sobre ese producto


class Producto:
    """Representa un producto del estanquillo."""

    _contador = 1   # autoincremento de código (reinicia al arrancar)

    @classmethod
    def _nuevo_codigo(cls):
        cod = cls._contador
        cls._contador += 1
        return cod

    def __init__(self, nombre, categoria, precio, cantidad,
                 presentacion=None, codigo=None):
        """
        presentacion : str  →  ej. '200ml', 'Pequeño'  (None si no aplica)
        codigo       : int  →  asignado automáticamente si no se pasa
        """
        self.codigo       = codigo if codigo is not None else Producto._nuevo_codigo()
        self.nombre       = nombre.strip()
        self.categoria    = categoria          # "Bebidas", "Snacks", etc.
        self.precio       = float(precio)
        self.cantidad     = int(cantidad)
        self.presentacion = presentacion       # "200ml" | "Pequeño" | None
        self.tiene_iva    = categoria in CATEGORIAS_CON_IVA

    # ── nombre completo para mostrar (incluye presentación si existe) ────
    @property
    def nombre_completo(self):
        if self.presentacion:
            return f"{self.nombre} ({self.presentacion})"
        return self.nombre

    # ── lógica de descuento especial ─────────────────────────────────────
    def tiene_descuento_categoria(self):
        n = self.nombre.lower()
        return any(p in n for p in PALABRAS_DESC_PROD)

    # ── stock ─────────────────────────────────────────────────────────────
    def vender(self, unidades):
        """Descuenta stock. Retorna True si OK, False si sin stock."""
        if self.cantidad <= 0:
            print(f"\n  ⚠  '{self.nombre_completo}' está AGOTADO o es INEXISTENTE.")
            return False
        if unidades > self.cantidad:
            print(f"\n  ⚠  Stock insuficiente. Solo hay {self.cantidad} "
                  f"unidad(es) de '{self.nombre_completo}'.")
            return False
        self.cantidad -= unidades
        return True

    def reabastecer(self, unidades):
        self.cantidad += int(unidades)
        print(f"  ✔  '{self.nombre_completo}' reabastecido. "
              f"Stock: {self.cantidad} unidad(es).")

    # ── vista ─────────────────────────────────────────────────────────────
    def mostrar_info(self, detalle=False):
        iva_txt  = "Sí (19%)" if self.tiene_iva else "No"
        desc_txt = "Sí (10%)" if self.tiene_descuento_categoria() else "No"
        stk_txt  = str(self.cantidad) if self.cantidad > 0 else "⚠ AGOTADO"
        pres_txt = self.presentacion if self.presentacion else "—"
        print(f"  [{self.codigo:>2}] {self.nombre_completo}")
        print(f"        Categoría   : {self.categoria}")
        print(f"        Presentación: {pres_txt}")
        print(f"        Precio      : ${self.precio:,.0f}")
        print(f"        IVA         : {iva_txt}")
        if detalle:
            print(f"        Desc. esp.  : {desc_txt}")
        print(f"        Stock       : {stk_txt}")
