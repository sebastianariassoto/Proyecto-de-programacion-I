"""
estanquillo.py — Estanquillo Gloriana
Inventario en memoria RAM con gaseosas, snacks, licores y cigarrillos.
"""

import os
import shutil

from producto import (Producto, CATEGORIAS, PRESENTACIONES_BEBIDAS,
                      TALLAS_SNACKS, CATEGORIAS_CON_IVA)


def _ancho_terminal():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 120


class Estanquillo:
    NOMBRE = "Gloriana"
    DUENO  = "Carlos"

    # Filas por pagina al mostrar inventario (0 = sin paginacion)
    FILAS_POR_PAGINA = 20

    def __init__(self):
        Producto._contador = 1
        self.productos = []
        self._cargar_inventario_inicial()

    # ── inventario inicial ────────────────────────────────────────────────
    def _cargar_inventario_inicial(self):
        inicial = [
            # nombre, categoria, precio, cantidad, presentacion
            # ── GASEOSAS ─────────────────────────────────────────────────
            ("Coca-Cola",           "Gaseosas",  2000,  35, "200ml"),
            ("Coca-Cola",           "Gaseosas",  3500,  25, "500ml"),
            ("Coca-Cola",           "Gaseosas",  5500,  18, "1L"),
            ("Coca-Cola",           "Gaseosas",  8000,  10, "2L"),
            ("Pepsi",               "Gaseosas",  1900,  30, "200ml"),
            ("Pepsi",               "Gaseosas",  3200,  22, "500ml"),
            ("Pepsi",               "Gaseosas",  5200,  15, "1L"),
            ("Pepsi",               "Gaseosas",  7800,   8, "2L"),
            ("7Up",                 "Gaseosas",  1900,  28, "200ml"),
            ("7Up",                 "Gaseosas",  3200,  20, "500ml"),
            ("7Up",                 "Gaseosas",  5200,  12, "1L"),
            ("Sprite",              "Gaseosas",  2000,  25, "200ml"),
            ("Sprite",              "Gaseosas",  3500,  18, "500ml"),
            ("Sprite",              "Gaseosas",  5500,  10, "1L"),
            ("Manzana Postobon",    "Gaseosas",  1800,  30, "200ml"),
            ("Manzana Postobon",    "Gaseosas",  3200,  22, "500ml"),
            ("Manzana Postobon",    "Gaseosas",  5000,  14, "1L"),
            ("Colombiana",          "Gaseosas",  1800,  28, "200ml"),
            ("Colombiana",          "Gaseosas",  3200,  20, "500ml"),
            ("Colombiana",          "Gaseosas",  5000,  12, "1L"),
            ("Limonada Postobon",   "Gaseosas",  2000,  20, "500ml"),
            ("Limonada Postobon",   "Gaseosas",  5500,  10, "1L"),
            ("Agua Cristal",        "Gaseosas",  1500,  50, "200ml"),
            ("Agua Cristal",        "Gaseosas",  2500,  35, "500ml"),
            ("Agua Cristal",        "Gaseosas",  3800,  20, "1L"),
            ("Agua Cristal",        "Gaseosas",  5500,  12, "2L"),
            ("Jugo Hit Naranja",    "Gaseosas",  2200,  25, "200ml"),
            ("Jugo Hit Naranja",    "Gaseosas",  4000,  18, "500ml"),
            ("Jugo Hit Mango",      "Gaseosas",  2200,  22, "200ml"),
            ("Jugo Hit Mango",      "Gaseosas",  4000,  15, "500ml"),
            ("Gatorade Naranja",    "Gaseosas",  4500,  20, "500ml"),
            ("Gatorade Mora",       "Gaseosas",  4500,  18, "500ml"),
            ("Monster Original",    "Gaseosas",  6500,  15, "500ml"),
            ("Red Bull",            "Gaseosas",  7000,  12, "200ml"),
            # ── SNACKS ───────────────────────────────────────────────────
            ("Chocolatina Jet",     "Snacks",    1200,  45, "Pequeno"),
            ("Chocolatina Jet",     "Snacks",    2500,  30, "Mediano"),
            ("Chocolatina Jet",     "Snacks",    4500,  20, "Grande"),
            ("Chocolatina Corona",  "Snacks",    1500,  40, "Pequeno"),
            ("Chocolatina Corona",  "Snacks",    3000,  25, "Mediano"),
            ("Chocolatina Corona",  "Snacks",    5500,  15, "Grande"),
            ("Papas Margarita",     "Snacks",    1500,  55, "Pequeno"),
            ("Papas Margarita",     "Snacks",    3000,  38, "Mediano"),
            ("Papas Margarita",     "Snacks",    5000,  22, "Grande"),
            ("Papas De Todito",     "Snacks",    1800,  45, "Pequeno"),
            ("Papas De Todito",     "Snacks",    3500,  30, "Mediano"),
            ("Papas De Todito",     "Snacks",    5500,  18, "Grande"),
            ("Chito",               "Snacks",    1000,  60, "Pequeno"),
            ("Chito",               "Snacks",    2000,  40, "Mediano"),
            ("Mani con Sal",        "Snacks",    1200,  50, "Pequeno"),
            ("Mani con Sal",        "Snacks",    2500,  30, "Mediano"),
            ("Gomas Trululu",       "Snacks",     800,  70,  None),
            ("Bom Bom Bum",         "Snacks",     500,  90,  None),
            ("Nucita",              "Snacks",    1500,  35,  None),
            ("Platanitos",          "Snacks",    1500,  45, "Pequeno"),
            ("Platanitos",          "Snacks",    3000,  28, "Mediano"),
            # ── LICORES ──────────────────────────────────────────────────
            ("Aguardiente Antioq.", "Licores",  12000,  15, "200ml"),
            ("Aguardiente Antioq.", "Licores",  22000,  10, "500ml"),
            ("Aguardiente Antioq.", "Licores",  38000,   6, "1L"),
            ("Aguardiente Nectar",  "Licores",  12000,  12, "200ml"),
            ("Aguardiente Nectar",  "Licores",  22000,   8, "500ml"),
            ("Aguardiente Nectar",  "Licores",  40000,   4, "1L"),
            ("Ron Viejo de Caldas", "Licores",  15000,  12, "200ml"),
            ("Ron Viejo de Caldas", "Licores",  28000,   8, "500ml"),
            ("Ron Viejo de Caldas", "Licores",  48000,   4, "1L"),
            ("Cerveza Club Colom.", "Licores",   3500,  60, "200ml"),
            ("Cerveza Poker",       "Licores",   3000,  72, "200ml"),
            ("Cerveza Aguila",      "Licores",   2800,  80, "200ml"),
            ("Cerveza Costena",     "Licores",   2500,  60, "200ml"),
            ("Cerveza Heineken",    "Licores",   5500,  24, "200ml"),
            ("Whisky Old Parr",     "Licores", 120000,   4, "500ml"),
            ("Whisky Old Parr",     "Licores", 220000,   2, "1L"),
            ("Vodka Smirnoff",      "Licores",  28000,   6, "500ml"),
            ("Vino Gato Blanco",    "Licores",  22000,   8, "500ml"),
            ("Vino Gato Tinto",     "Licores",  22000,   6, "500ml"),
            # ── CIGARRILLOS ──────────────────────────────────────────────
            ("Marlboro Rojo",       "Cigarrillos", 1200, 80, None),
            ("Marlboro Gold",       "Cigarrillos", 1200, 60, None),
            ("Pielroja",            "Cigarrillos",  700, 100, None),
            ("Delta",               "Cigarrillos",  600, 120, None),
            ("Mustang",             "Cigarrillos",  800,  90, None),
        ]

        for nombre, cat, precio, cant, pres in inicial:
            self.productos.append(
                Producto(nombre, cat, precio, cant, presentacion=pres)
            )

    # ── gestión ───────────────────────────────────────────────────────────
    def agregar_producto(self, nombre, categoria, precio, cantidad, presentacion=None):
        p = Producto(nombre, categoria, float(precio), int(cantidad),
                     presentacion=presentacion)
        self.productos.append(p)
        print(f"\n  [OK] '{p.nombre_completo}' agregado con codigo [{p.codigo}].")
        return p

    def buscar_producto(self, codigo):
        try:
            cod = int(codigo)
        except (ValueError, TypeError):
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
            print(f"  [!] No existe producto con codigo [{codigo}].")

    # ── helpers de tabla horizontal ───────────────────────────────────────
    @staticmethod
    def _encabezado(titulo):
        ancho = min(_ancho_terminal(), 110)
        print(f"\n{'=' * ancho}")
        print(f"   {titulo}")
        print(f"{'=' * ancho}")

    @staticmethod
    def _cabecera_tabla(admin=False):
        if admin:
            print(f"  {'COD':>4}  {'PRODUCTO':<26}  {'CAT':<12}  "
                  f"{'PRES':<8}  {'PRECIO':>10}  {'IVA':<5}  {'DESC':<6}  {'STOCK':>6}")
            print(f"  {'─'*4}  {'─'*26}  {'─'*12}  {'─'*8}  {'─'*10}  {'─'*5}  {'─'*6}  {'─'*6}")
        else:
            print(f"  {'COD':>4}  {'PRODUCTO':<26}  {'PRES':<8}  "
                  f"{'PRECIO':>10}  {'STOCK':>6}  {'NOTAS'}")
            print(f"  {'─'*4}  {'─'*26}  {'─'*8}  {'─'*10}  {'─'*6}  {'─'*16}")

    @staticmethod
    def _fila(p, admin=False):
        pres    = p.presentacion if p.presentacion else "  ---"
        stock_s = f"{p.cantidad:>6}" if p.cantidad > 0 else " AGOT."
        nom     = p.nombre[:26] if len(p.nombre) <= 26 else p.nombre[:24] + ".."
        precio_s = f"${p.precio:,.0f}"
        if admin:
            iva_s  = "Si" if p.tiene_iva else "No"
            desc_s = "10%" if p.tiene_descuento_categoria() else " ---"
            print(f"  {p.codigo:>4}  {nom:<26}  {p.categoria:<12}  "
                  f"{pres:<8}  {precio_s:>10}  {iva_s:<5}  {desc_s:<6}  {stock_s}")
        else:
            notas = []
            if p.tiene_iva:
                notas.append("+IVA19%")
            if p.tiene_descuento_categoria():
                notas.append("DESC10%")
            notas_s = " ".join(notas)
            print(f"  {p.codigo:>4}  {nom:<26}  {pres:<8}  {precio_s:>10}  {stock_s}  {notas_s}")

    # ── paginacion interna ────────────────────────────────────────────────
    def _paginar(self, filas_fn, prods, admin=False):
        """
        Llama filas_fn(p, admin) para cada producto.
        Cada FILAS_POR_PAGINA filas pregunta si continuar.
        Devuelve False si el usuario cancela, True si termino.
        """
        n = self.FILAS_POR_PAGINA
        for i, p in enumerate(prods):
            filas_fn(p, admin)
            if n > 0 and (i + 1) % n == 0 and (i + 1) < len(prods):
                r = input(f"\n  --- Mostrando {i+1}/{len(prods)}. "
                          f"ENTER = continuar  |  'q' = salir --- ").strip().lower()
                if r == "q":
                    return False
                self._cabecera_tabla(admin)   # repite encabezado tras pausa
        return True

    # ── vistas ────────────────────────────────────────────────────────────
    def mostrar_catalogo_cliente(self):
        """Catalogo para el cliente: solo productos con stock > 0."""
        self._encabezado(f"CATALOGO — Estanquillo {self.NOMBRE}")
        orden = ["Gaseosas", "Snacks", "Licores", "Cigarrillos"]
        alguno = False
        for cat in orden:
            prods = [p for p in self.productos if p.categoria == cat and p.cantidad > 0]
            if not prods:
                continue
            alguno = True
            print(f"\n  >> {cat.upper()}")
            self._cabecera_tabla(admin=False)
            if not self._paginar(self._fila, prods, admin=False):
                break
            print()
        if not alguno:
            print("\n  No hay productos disponibles en este momento.")
        ancho = min(_ancho_terminal(), 110)
        print("=" * ancho + "\n")

    def mostrar_inventario(self):
        """Inventario completo para el administrador."""
        self._encabezado(f"INVENTARIO COMPLETO — Estanquillo {self.NOMBRE}")
        orden = ["Gaseosas", "Snacks", "Licores", "Cigarrillos"]
        total_refs = 0
        total_uds  = 0
        for cat in orden:
            prods = [p for p in self.productos if p.categoria == cat]
            if not prods:
                continue
            print(f"\n  >> {cat.upper()}")
            self._cabecera_tabla(admin=True)
            if not self._paginar(self._fila, prods, admin=True):
                break
            for p in prods:
                total_refs += 1
                total_uds  += p.cantidad
            print()
        print(f"  Referencias totales: {total_refs}   |   Unidades en stock: {total_uds}")
        ancho = min(_ancho_terminal(), 110)
        print("=" * ancho + "\n")

    def mostrar_tabla_compacta(self):
        """Tabla compacta (admin selecciona para reabastecer)."""
        orden = ["Gaseosas", "Snacks", "Licores", "Cigarrillos"]
        self._cabecera_tabla(admin=True)
        for cat in orden:
            prods = [p for p in self.productos if p.categoria == cat]
            if prods:
                print(f"  ── {cat.upper()} ──")
                if not self._paginar(self._fila, prods, admin=True):
                    break
        print()
