"""
estanquillo.py
Clase Estanquillo Gloriana.

- Todo vive en memoria RAM.
- Al cerrar el programa los datos se borran (no hay archivo).
- El inventario inicial se carga desde _inventario_inicial().
"""

from producto import (Producto, CATEGORIAS, PRESENTACIONES_BEBIDAS,
                      TALLAS_SNACKS, CATEGORIAS_CON_IVA)


class Estanquillo:
    NOMBRE = "Gloriana"
    DUENO  = "Doña Gloria"

    def __init__(self):
        # Reinicia el contador de códigos para que siempre arranque en 1
        Producto._contador = 1
        self.productos = []
        self._cargar_inventario_inicial()

    # ── inventario inicial (en memoria, sin archivos) ─────────────────────
    def _cargar_inventario_inicial(self):
        """
        Carga los productos de ejemplo al arrancar.
        Estructura: (nombre, categoria, precio, cantidad, presentacion)
        """
        inicial = [
            # ── Bebidas ──────────────────────────────────────────────────
            ("Coca-Cola",   "Bebidas", 2000, 30, "200ml"),
            ("Coca-Cola",   "Bebidas", 3500, 20, "500ml"),
            ("Coca-Cola",   "Bebidas", 5500, 15, "1L"),
            ("Coca-Cola",   "Bebidas", 8000, 10, "2L"),
            ("Manzana Postobón", "Bebidas", 1800, 30, "200ml"),
            ("Manzana Postobón", "Bebidas", 3200, 20, "500ml"),
            ("Manzana Postobón", "Bebidas", 5000, 10, "1L"),
            ("Manzana Postobón", "Bebidas", 7500,  8, "2L"),
            ("Sprite",      "Bebidas", 2000, 25, "200ml"),
            ("Sprite",      "Bebidas", 3500, 18, "500ml"),
            ("Sprite",      "Bebidas", 5500, 12, "1L"),
            ("Sprite",      "Bebidas", 8000,  8, "2L"),
            ("Agua Cristal","Bebidas", 1500, 40, "200ml"),
            ("Agua Cristal","Bebidas", 2500, 30, "500ml"),
            ("Agua Cristal","Bebidas", 3800, 20, "1L"),
            ("Agua Cristal","Bebidas", 5500, 12, "2L"),
            # ── Licores ──────────────────────────────────────────────────
            ("Aguardiente Antioqueño", "Licores", 12000, 15, "200ml"),
            ("Aguardiente Antioqueño", "Licores", 22000, 10, "500ml"),
            ("Aguardiente Antioqueño", "Licores", 38000,  8, "1L"),
            ("Aguardiente Néctar",     "Licores", 12000, 12, "200ml"),
            ("Aguardiente Néctar",     "Licores", 22000,  8, "500ml"),
            ("Aguardiente Néctar",     "Licores", 40000,  5, "1L"),
            ("Cerveza Club Colombia",  "Licores",  3500, 48, "200ml"),
            ("Ron Viejo de Caldas",    "Licores", 15000, 10, "200ml"),
            ("Ron Viejo de Caldas",    "Licores", 28000,  6, "500ml"),
            # ── Cigarrillos ──────────────────────────────────────────────
            ("Cigarrillo Marlboro",  "Cigarrillos", 1000, 100, None),
            ("Cigarrillo Pielroja",  "Cigarrillos",  700, 100, None),
            # ── Snacks ───────────────────────────────────────────────────
            ("Chocolatina Jet",   "Snacks", 1200, 40, "Pequeño"),
            ("Chocolatina Jet",   "Snacks", 2500, 30, "Mediano"),
            ("Chocolatina Jet",   "Snacks", 4500, 20, "Grande"),
            ("Chocolatina Corona","Snacks", 1500, 35, "Pequeño"),
            ("Chocolatina Corona","Snacks", 3000, 25, "Mediano"),
            ("Chocolatina Corona","Snacks", 5500, 15, "Grande"),
            ("Papas Margarita",   "Snacks", 1500, 50, "Pequeño"),
            ("Papas Margarita",   "Snacks", 3000, 35, "Mediano"),
            ("Papas Margarita",   "Snacks", 5000, 20, "Grande"),
            ("Papas De Todito",   "Snacks", 1800, 40, "Pequeño"),
            ("Papas De Todito",   "Snacks", 3500, 28, "Mediano"),
            ("Papas De Todito",   "Snacks", 5500, 15, "Grande"),
        ]

        for nombre, cat, precio, cant, pres in inicial:
            p = Producto(nombre, cat, precio, cant, presentacion=pres)
            self.productos.append(p)

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
            print("  ⚠  Código inválido.")
            return None
        for p in self.productos:
            if p.codigo == cod:
                return p
        print(f"\n  ⚠  No existe producto con código [{codigo}].")
        return None

    def reabastecer(self, codigo, unidades):
        p = self.buscar_producto(codigo)
        if p:
            p.reabastecer(unidades)

    def sincronizar(self):
        pass   # no hay archivo → no hace nada

    # ── vistas ────────────────────────────────────────────────────────────
    def _encabezado(self, titulo):
        print(f"\n{'='*52}")
        print(f"   {titulo}")
        print(f"{'='*52}")

    def mostrar_catalogo_cliente(self):
        """Muestra solo productos con stock > 0, agrupados por categoría."""
        self._encabezado(f"CATÁLOGO — Estanquillo {self.NOMBRE}")
        categorias_orden = ["Bebidas", "Licores", "Cigarrillos", "Snacks"]
        alguno = False
        for cat in categorias_orden:
            productos_cat = [p for p in self.productos
                             if p.categoria == cat and p.cantidad > 0]
            if not productos_cat:
                continue
            alguno = True
            print(f"\n  ── {cat.upper()} ──")
            for p in productos_cat:
                iva  = " (+IVA 19%)" if p.tiene_iva else ""
                desc = " [Desc. 10%]" if p.tiene_descuento_categoria() else ""
                pres = f" ({p.presentacion})" if p.presentacion else ""
                print(f"    [{p.codigo:>2}] {p.nombre}{pres}{iva}{desc}")
                print(f"           ${p.precio:,.0f}  —  stock: {p.cantidad}")
        if not alguno:
            print("\n  No hay productos disponibles en este momento.")
        print(f"{'='*52}\n")

    def mostrar_inventario(self):
        """Vista completa para el administrador."""
        self._encabezado(f"INVENTARIO COMPLETO — Estanquillo {self.NOMBRE}")
        if not self.productos:
            print("  Sin productos.")
        else:
            categorias_orden = ["Bebidas", "Licores", "Cigarrillos", "Snacks"]
            for cat in categorias_orden:
                prods = [p for p in self.productos if p.categoria == cat]
                if not prods:
                    continue
                print(f"\n  ── {cat.upper()} ──")
                for p in prods:
                    p.mostrar_info(detalle=True)
                    print()
        print(f"  Total de referencias: {len(self.productos)}")
        print(f"{'='*52}\n")
