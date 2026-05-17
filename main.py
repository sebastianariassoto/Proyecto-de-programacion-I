"""
main.py — Estanquillo Gloriana
==============================
Menú principal:
  [1] Soy CLIENTE  → ver catálogo, elegir presentación, comprar, tiquete
  [2] Soy USUARIO  → ver inventario, agregar producto, reabastecer
  [0] Salir (todo se borra, memoria limpia)
"""

from estanquillo import Estanquillo
from cliente     import Cliente
from venta       import Venta
from producto    import (CATEGORIAS, PRESENTACIONES_BEBIDAS,
                         TALLAS_SNACKS, CATEGORIAS_CON_IVA)


# ═══════════════════════════════════════════════════════
#  UTILIDADES DE CONSOLA
# ═══════════════════════════════════════════════════════

def sep(char="=", n=52):
    print(char * n)

def titulo(texto):
    print(f"\n{'='*52}")
    print(f"   {texto}")
    print(f"{'='*52}")

def pausar():
    input("\n  Presione ENTER para continuar...")

def salto():
    print("\n")

def pedir_entero(msg, minimo=None, maximo=None):
    while True:
        try:
            v = int(input(msg))
            if minimo is not None and v < minimo:
                print(f"  ⚠  Mínimo permitido: {minimo}"); continue
            if maximo is not None and v > maximo:
                print(f"  ⚠  Máximo permitido: {maximo}"); continue
            return v
        except ValueError:
            print("  ⚠  Ingrese un número entero válido.")

def pedir_float(msg, minimo=0.01):
    while True:
        try:
            v = float(input(msg))
            if v < minimo:
                print(f"  ⚠  Debe ser mayor a {minimo}"); continue
            return v
        except ValueError:
            print("  ⚠  Ingrese un número válido (ej: 3500).")

def pedir_texto(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("  ⚠  El campo no puede estar vacío.")

def elegir_opcion(opciones_dict, msg="  Opción: "):
    """Muestra un dict {clave: texto} y retorna la clave elegida."""
    while True:
        v = input(msg).strip()
        if v in opciones_dict:
            return v
        print(f"  ⚠  Opción no válida. Elija entre: {', '.join(opciones_dict.keys())}")


# ═══════════════════════════════════════════════════════
#  MENÚ CLIENTE
# ═══════════════════════════════════════════════════════

def menu_cliente(tienda):
    salto()
    titulo("BIENVENIDO — Estanquillo Gloriana")

    # Datos mínimos del cliente
    nombre  = pedir_texto("  Su nombre   : ")
    estrato = pedir_entero("  Su estrato  : ", minimo=1, maximo=6)
    cliente = Cliente(nombre, estrato)

    d_pct = cliente.descuento_pct()
    if d_pct > 0:
        print(f"\n  ✔  Descuento por estrato {estrato}: {d_pct}% sobre el total.")
    else:
        print(f"\n  Sin descuento por estrato (estrato {estrato}).")

    # Mostrar catálogo
    tienda.mostrar_catalogo_cliente()

    disponibles = [p for p in tienda.productos if p.cantidad > 0]
    if not disponibles:
        print("  No hay productos disponibles. Vuelva pronto.")
        pausar()
        return

    venta = Venta(cliente)

    while True:
        print("─" * 52)
        print("  ¿Qué desea hacer?")
        print("  [1] Agregar producto a la compra")
        print("  [2] Ver tiquete y finalizar")
        print("  [0] Cancelar y volver")
        op = input("  Opción: ").strip()

        if op == "1":
            codigo = pedir_entero("  Código del producto: ", minimo=1)
            prod   = tienda.buscar_producto(codigo)
            if prod is None:
                continue
            if prod.cantidad == 0:
                print(f"\n  ⚠  '{prod.nombre_completo}' está AGOTADO o es INEXISTENTE.")
                print("     Consulte al administrador para reabastecerlo.")
                pausar()
                continue
            cantidad = pedir_entero(
                f"  Cantidad (stock: {prod.cantidad}): ",
                minimo=1, maximo=prod.cantidad
            )
            ok = venta.agregar_item(prod, cantidad)
            if ok:
                print(f"  ✔  '{prod.nombre_completo}' x{cantidad} agregado.")

        elif op == "2":
            if not venta.items:
                print("  ⚠  No ha agregado ningún producto.")
                continue
            venta.mostrar_tiquete()
            pausar()
            break

        elif op == "0":
            print("  Compra cancelada.")
            break
        else:
            print("  ⚠  Opción no válida.")


# ═══════════════════════════════════════════════════════
#  MENÚ ADMINISTRADOR
# ═══════════════════════════════════════════════════════

def _pedir_presentacion(categoria):
    """
    Retorna la presentación elegida (str) o None si la categoría
    no usa presentaciones.
    Bebidas y Licores → 200ml / 500ml / 1L / 2L
    Snacks            → Pequeño / Mediano / Grande
    Cigarrillos       → sin presentación
    """
    if categoria in ("Bebidas", "Licores"):
        print("\n  Presentación:")
        for k, v in PRESENTACIONES_BEBIDAS.items():
            print(f"    [{k}] {v}")
        op = elegir_opcion(PRESENTACIONES_BEBIDAS, "  Presentación: ")
        return PRESENTACIONES_BEBIDAS[op]

    elif categoria == "Snacks":
        print("\n  Tamaño:")
        for k, v in TALLAS_SNACKS.items():
            print(f"    [{k}] {v}")
        op = elegir_opcion(TALLAS_SNACKS, "  Tamaño: ")
        return TALLAS_SNACKS[op]

    else:
        return None   # Cigarrillos sin presentación


def menu_admin(tienda):
    while True:
        salto()
        titulo("PANEL DE ADMINISTRADOR — Gloriana")
        print("  [1] Ver inventario completo")
        print("  [2] Agregar nuevo producto")
        print("  [3] Reabastecer producto existente")
        print("  [0] Volver al menú principal")
        sep()
        op = input("  Opción: ").strip()

        if op == "1":
            tienda.mostrar_inventario()
            pausar()

        elif op == "2":
            salto()
            print("─" * 52)
            print("  AGREGAR NUEVO PRODUCTO")
            print("─" * 52)

            nombre = pedir_texto("  Nombre del producto      : ")

            print("\n  Categoría:")
            for k, v in CATEGORIAS.items():
                iva = " (IVA 19%)" if v in CATEGORIAS_CON_IVA else ""
                print(f"    [{k}] {v}{iva}")
            cat_op    = elegir_opcion(CATEGORIAS, "  Categoría: ")
            categoria = CATEGORIAS[cat_op]

            # Presentación según categoría
            presentacion = _pedir_presentacion(categoria)

            precio   = pedir_float("  Precio unitario ($)      : ")
            cantidad = pedir_entero("  Cantidad inicial         : ", minimo=0)

            tienda.agregar_producto(nombre, categoria, precio, cantidad, presentacion)
            pausar()

        elif op == "3":
            salto()
            print("─" * 52)
            print("  REABASTECER PRODUCTO")
            print("─" * 52)
            tienda.mostrar_inventario()
            codigo   = pedir_entero("  Código del producto: ", minimo=1)
            unidades = pedir_entero("  Unidades a agregar : ", minimo=1)
            tienda.reabastecer(codigo, unidades)
            pausar()

        elif op == "0":
            break
        else:
            print("  ⚠  Opción no válida.")


# ═══════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════

def main():
    tienda = Estanquillo()

    while True:
        salto()
        print("=" * 52)
        print("       ESTANQUILLO  'GLORIANA'")
        print("          Doña Gloria — Manizales")
        print("=" * 52)
        print("  [1] Soy CLIENTE   (realizar compra)")
        print("  [2] Soy USUARIO   (administrar tienda)")
        print("  [0] Salir")
        print("=" * 52)
        op = input("  ¿Quién es usted? ").strip()

        if op == "1":
            menu_cliente(tienda)
        elif op == "2":
            menu_admin(tienda)
        elif op == "0":
            print("\n  Hasta luego. ¡Vuelva pronto al Estanquillo Gloriana!\n")
            break
        else:
            print("  ⚠  Opción no válida. Ingrese 1, 2 o 0.")


if __name__ == "__main__":
    main()
