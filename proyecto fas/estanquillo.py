"""
estanquillo.py
Clase Estanquillo Gloriana — inventario en memoria RAM.
"""

from producto import (Producto, CATEGORIAS, PRESENTACIONES_BEBIDAS,
                      TALLAS_SNACKS, CATEGORIAS_CON_IVA)

# Ancho de columnas para las tablas horizontales
COL = {"cod": 5, "nombre": 28, "cat": 12, "pres": 8,
       "precio": 11, "iva": 6, "desc": 6, "stock": 7}


def _fila(*vals):
    """Imprime una fila de tabla dado un iterable de (valor, ancho, alineacion)."""
    partes = []
    for val, ancho, aln in vals:
        s = str(val)
        if aln == "r":
            partes.append(s.rjust(ancho))
        elif aln == "c":
            partes.append(s.center(ancho))
        else:
            partes.append(s.ljust(ancho))
    print("  " + "  ".join(partes))


def _sep_tabla(anchos, char="─"):
    print("  " + ("─" * (sum(anchos) + 2 * (len(anchos) - 1))))


class Estanquillo:
    NOMBRE = "Gloriana"
    DUENO  = "Doña Gloria"

    def __init__(self):
        Producto._contador = 1
        self.productos = []
        self._cargar_inventario_inicial()

    # ── inventario inicial ────────────────────────────────────────────────
    def _cargar_inventario_inicial(self):
        inicial = [
            # Bebidas
            ("Coca-Cola",            "Bebidas",     2000, 30, "200ml"),
            ("Coca-Cola",            "Bebidas",     3500, 20, "500ml"),
            ("Coca-Cola",            "Bebidas",     5500, 15, "1L"),
            ("Coca-Cola",            "Bebidas",     8000, 10, "2L"),
            ("Manzana Postobón",     "Bebidas",     1800, 30, "200ml"),
            ("Manzana Postobón",     "Bebidas",     3200, 20, "500ml"),
            ("Manzana Postobón",     "Bebidas",     5000, 10, "1L"),
            ("Manzana Postobón",     "Bebidas",     7500,  8, "2L"),
            ("Sprite",               "Bebidas",     2000, 25, "200ml"),
            ("Sprite",               "Bebidas",     3500, 18, "500ml"),
            ("Sprite",               "Bebidas",     5500, 12, "1L"),
            ("Sprite",               "Bebidas",     8000,  8, "2L"),
            ("Agua Cristal",         "Bebidas",     1500, 40, "200ml"),
            ("Agua Cristal",         "Bebidas",     2500, 30, "500ml"),
            ("Agua Cristal",         "Bebidas",     3800, 20, "1L"),
            ("Agua Cristal",         "Bebidas",     5500, 12, "2L"),
            # Licores
            ("Aguardiente Antioqueño", "Licores",  12000, 15, "200ml"),
            ("Aguardiente Antioqueño", "Licores",  22000, 10, "500ml"),
            ("Aguardiente Antioqueño", "Licores",  38000,  8, "1L"),
            ("Aguardiente Néctar",    "Licores",   12000, 12, "200ml"),
            ("Aguardiente Néctar",    "Licores",   22000,  8, "500ml"),
            ("Aguardiente Néctar",    "Licores",   40000,  5, "1L"),
            ("Cerveza Club Colombia", "Licores",    3500, 48, "200ml"),
            ("Ron Viejo de Caldas",   "Licores",   15000, 10, "200ml"),
            ("Ron Viejo de Caldas",   "Licores",   28000,  6, "500ml"),
            # Cigarrillos
            ("Cigarrillo Marlboro",  "Cigarrillos", 1000, 100, None),
            ("Cigarrillo Pielroja",  "Cigarrillos",  700, 100, None),
            # Snacks
            ("Chocolatina Jet",      "Snacks",      1200, 40, "Pequeño"),
            ("Chocolatina Jet",      "Snacks",      2500, 30, "Mediano"),
            ("Chocolatina Jet",      "Snacks",      4500, 20, "Grande"),
            ("Chocolatina Corona",   "Snacks",      1500, 35, "Pequeño"),
            ("Chocolatina Corona",   "Snacks",      3000, 25, "Mediano"),
            ("Chocolatina Corona",   "Snacks",      5500, 15, "Grande"),
            ("Papas Margarita",      "Snacks",      1500, 50, "Pequeño"),
            ("Papas Margarita",      "Snacks",      3000, 35, "Mediano"),
            ("Papas Margarita",      "Snacks",      5000, 20, "Grande"),
            ("Papas De Todito",      "Snacks",      1800, 40, "Pequeño"),
            ("Papas De Todito",      "Snacks",      3500, 28, "Mediano"),
            ("Papas De Todito",      "Snacks",      5500, 15, "Grande"),
        ]
        for nombre, cat, precio, cant, pres in inicial:
            self.productos.append(Producto(nombre, cat, precio, cant, presentacion=pres))

    # ── gestión ───────────────────────────────────────────────────────────
    def agregar_producto(self, nombre, categoria, precio, cantidad, presentacion=None):
        p = Producto(nombre, categoria, float(precio), int(cantidad),
                     presentacion=presentacion)
        self.productos.append(p)
        print(f"\n  ✔  '{p.nombre_completo}' agregado con código [{p.codigo}].")
        return p

    def buscar_producto(self, codigo):
        try:
            cod = int(codigo)
        except ValueError:
            return None
        for p in self.productos:
            if p.codigo == cod:
                return p
        return None

    def reabastecer(self, codigo, unidades):
        p = self.buscar_producto(codigo)
        if p:
            p.reabastecer(unidades)
        else:
            print(f"  ⚠  No existe producto con código [{codigo}].")

    # ── vistas horizontales ───────────────────────────────────────────────
    def _encabezado(self, titulo):
        print(f"\n{'═'*64}")
        print(f"   {titulo}")
        print(f"{'═'*64}")

    def _encabezado_tabla(self, solo_stock=False):
        """Imprime la cabecera de columnas."""
        if solo_stock:
            print(f"  {'CÓD':>4}  {'PRODUCTO':<32}  {'CATEGORÍA':<12}  {'PRES.':<8}  {'PRECIO':>10}  {'STOCK':>6}")
            print(f"  {'─'*4}  {'─'*32}  {'─'*12}  {'─'*8}  {'─'*10}  {'─'*6}")
        else:
            print(f"  {'CÓD':>4}  {'PRODUCTO':<32}  {'CATEGORÍA':<12}  {'PRES.':<8}  {'PRECIO':>10}  {'IVA':<6}  {'DESC':<6}  {'STOCK':>6}")
            print(f"  {'─'*4}  {'─'*32}  {'─'*12}  {'─'*8}  {'─'*10}  {'─'*6}  {'─'*6}  {'─'*6}")

    def _fila_producto(self, p, solo_stock=False):
        pres  = p.presentacion if p.presentacion else "—"
        stock = str(p.cantidad) if p.cantidad > 0 else "⚠AGO"
        precio_str = f"${p.precio:,.0f}"
        nombre_display = (p.nombre[:32]) if len(p.nombre) <= 32 else p.nombre[:30] + ".."
        if solo_stock:
            print(f"  {p.codigo:>4}  {nombre_display:<32}  {p.categoria:<12}  {pres:<8}  {precio_str:>10}  {stock:>6}")
        else:
            iva_txt  = "Sí" if p.tiene_iva else "No"
            desc_txt = "10%" if p.tiene_descuento_categoria() else "—"
            print(f"  {p.codigo:>4}  {nombre_display:<32}  {p.categoria:<12}  {pres:<8}  {precio_str:>10}  {iva_txt:<6}  {desc_txt:<6}  {stock:>6}")

    def mostrar_catalogo_cliente(self):
        """Catálogo para el cliente: tabla horizontal, solo con stock > 0."""
        self._encabezado(f"CATÁLOGO — Estanquillo {self.NOMBRE}")
        categorias_orden = ["Bebidas", "Licores", "Cigarrillos", "Snacks"]
        alguno = False
        for cat in categorias_orden:
            prods = [p for p in self.productos if p.categoria == cat and p.cantidad > 0]
            if not prods:
                continue
            alguno = True
            print(f"\n  ▸ {cat.upper()}")
            self._encabezado_tabla(solo_stock=True)
            for p in prods:
                extras = []
                if p.tiene_iva:
                    extras.append("+IVA19%")
                if p.tiene_descuento_categoria():
                    extras.append("DESC10%")
                pres  = p.presentacion if p.presentacion else "—"
                precio_str = f"${p.precio:,.0f}"
                nota  = " ".join(extras)
                nombre_display = p.nombre if len(p.nombre) <= 32 else p.nombre[:30] + ".."
                print(f"  {p.codigo:>4}  {nombre_display:<32}  {p.categoria:<12}  {pres:<8}  {precio_str:>10}  {p.cantidad:>6}  {nota}")
            print()
        if not alguno:
            print("\n  No hay productos disponibles en este momento.")
        print(f"{'═'*64}\n")

    def mostrar_inventario(self):
        """Inventario completo para el administrador."""
        self._encabezado(f"INVENTARIO COMPLETO — Estanquillo {self.NOMBRE}")
        categorias_orden = ["Bebidas", "Licores", "Cigarrillos", "Snacks"]
        total_refs = 0
        total_stock = 0
        for cat in categorias_orden:
            prods = [p for p in self.productos if p.categoria == cat]
            if not prods:
                continue
            print(f"\n  ▸ {cat.upper()}")
            self._encabezado_tabla(solo_stock=False)
            for p in prods:
                self._fila_producto(p, solo_stock=False)
                total_refs  += 1
                total_stock += p.cantidad
            print()
        print(f"  Referencias: {total_refs}   |   Unidades en stock: {total_stock}")
        print(f"{'═'*64}\n")

    def mostrar_inventario_compacto(self):
        """Tabla compacta para cuando el admin va a seleccionar un producto."""
        categorias_orden = ["Bebidas", "Licores", "Cigarrillos", "Snacks"]
        self._encabezado_tabla(solo_stock=True)
        for cat in categorias_orden:
            prods = [p for p in self.productos if p.categoria == cat]
            if prods:
                print(f"  ── {cat.upper()} ──")
                for p in prods:
                    self._fila_producto(p, solo_stock=True)
        print()
