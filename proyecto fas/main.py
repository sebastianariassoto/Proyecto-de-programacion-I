"""
main.py — Estanquillo Gloriana
==============================
Menú principal:
  [1] Soy CLIENTE  → catálogo horizontal, selección por código, tiquete
  [2] Soy ADMIN    → inventario, agregar producto, reabastecer
  [0] Salir
"""

from estanquillo import Estanquillo
from cliente     import Cliente
from venta       import Venta
from producto    import (CATEGORIAS, PRESENTACIONES_BEBIDAS,
                         TALLAS_SNACKS, CATEGORIAS_CON_IVA)


# ═══════════════════════════════════════════════════════
#  UTILIDADES
# ═══════════════════════════════════════════════════════

def sep(n=64, char="═"):
    print(char * n)

def titulo(texto, char="═", n=64):
    print(f"\n{char*n}")
    print(f"   {texto}")
    print(f"{char*n}")

def pausar():
    input("\n  Presione ENTER para continuar...")

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
        raw = input(msg).strip().replace(",", ".")
        try:
            v = float(raw)
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
    while True:
        v = input(msg).strip()
        if v in opciones_dict:
            return v
        print(f"  ⚠  Opción no válida. Elija entre: {', '.join(opciones_dict.keys())}")


# ═══════════════════════════════════════════════════════
#  SELECCIÓN DE PRODUCTO (por código o buscando en tabla)
# ═══════════════════════════════════════════════════════

def seleccionar_producto(tienda, solo_con_stock=True):
    """
    Permite al usuario elegir un producto:
      - Ingresando directamente el código
      - Viendo la tabla y luego ingresando el código
    Retorna el objeto Producto o None.
    """
    while True:
        print("\n  ¿Cómo desea seleccionar el producto?")
        print("  [1] Ingresar el código directamente")
        print("  [2] Ver tabla y luego ingresar código")
        print("  [0] Cancelar")
        op = input("  Opción: ").strip()

        if op == "1":
            codigo = pedir_entero("  Código del producto: ", minimo=1)
            prod = tienda.buscar_producto(codigo)
            if prod is None:
                print(f"  ⚠  No existe producto con código [{codigo}].")
                continue
            if solo_con_stock and prod.cantidad == 0:
                print(f"  ⚠  '{prod.nombre_completo}' está AGOTADO.")
                continue
            return prod

        elif op == "2":
            if solo_con_stock:
                tienda.mostrar_catalogo_cliente()
            else:
                tienda.mostrar_inventario_compacto()
            codigo = pedir_entero("  Ingrese el código: ", minimo=1)
            prod = tienda.buscar_producto(codigo)
            if prod is None:
                print(f"  ⚠  No existe producto con código [{codigo}].")
                continue
            if solo_con_stock and prod.cantidad == 0:
                print(f"  ⚠  '{prod.nombre_completo}' está AGOTADO.")
                continue
            return prod

        elif op == "0":
            return None
        else:
            print("  ⚠  Opción no válida.")


# ═══════════════════════════════════════════════════════
#  MENÚ CLIENTE
# ═══════════════════════════════════════════════════════

def _mostrar_carrito(venta):
    """Muestra el carrito actual en formato tabla horizontal."""
    if not venta.items:
        print("  (carrito vacío)")
        return
    print(f"\n  {'─'*60}")
    print(f"  {'PRODUCTO':<34}  {'CANT':>5}  {'P.UNIT':>10}  {'SUBTOTAL':>10}")
    print(f"  {'─'*60}")
    total_bruto = 0
    for prod, cant in venta.items:
        sub = prod.precio * cant
        total_bruto += sub
        nombre_d = prod.nombre_completo[:34] if len(prod.nombre_completo) <= 34 else prod.nombre_completo[:32] + ".."
        print(f"  {nombre_d:<34}  x{cant:<4}  ${prod.precio:>9,.0f}  ${sub:>9,.0f}")
    print(f"  {'─'*60}")
    print(f"  {'Aprox. bruto (sin IVA ni descuentos)':<52}  ${total_bruto:>9,.0f}")
    print()


def menu_cliente(tienda):
    titulo("BIENVENIDO — Estanquillo Gloriana")

    nombre  = pedir_texto("  Su nombre   : ")
    estrato = pedir_entero("  Su estrato  : ", minimo=1, maximo=6)
    cliente = Cliente(nombre, estrato)

    d_pct = cliente.descuento_pct()
    if d_pct > 0:
        print(f"\n  ✔  Hola {cliente.nombre}. Descuento por estrato {estrato}: {d_pct}%")
    else:
        print(f"\n  Hola {cliente.nombre}. Sin descuento adicional (estrato {estrato}).")

    disponibles = [p for p in tienda.productos if p.cantidad > 0]
    if not disponibles:
        print("\n  No hay productos disponibles. Vuelva pronto.")
        pausar()
        return

    venta = Venta(cliente)

    while True:
        print("\n" + "─" * 64)
        print(f"  COMPRA — {cliente.nombre}   |   Estrato {estrato}   |   Items en carrito: {len(venta.items)}")
        print("─" * 64)
        print("  [1] Agregar producto al carrito")
        print("  [2] Ver carrito actual")
        print("  [3] Ver catálogo completo")
        print("  [4] Finalizar y ver tiquete")
        print("  [0] Cancelar y volver")
        op = input("  Opción: ").strip()

        if op == "1":
            prod = seleccionar_producto(tienda, solo_con_stock=True)
            if prod is None:
                continue
            print(f"\n  Producto seleccionado: [{prod.codigo}] {prod.nombre_completo}")
            print(f"  Precio: ${prod.precio:,.0f}  |  Stock disponible: {prod.cantidad}")
            if prod.tiene_iva:
                print(f"  (+ IVA 19%)")
            if prod.tiene_descuento_categoria():
                print(f"  (+ Descuento especial 10%)")
            cantidad = pedir_entero(
                f"  Cantidad (1–{prod.cantidad}): ",
                minimo=1, maximo=prod.cantidad
            )
            ok = venta.agregar_item(prod, cantidad)
            if ok:
                print(f"  ✔  '{prod.nombre_completo}' x{cantidad} agregado al carrito.")

        elif op == "2":
            _mostrar_carrito(venta)

        elif op == "3":
            tienda.mostrar_catalogo_cliente()

        elif op == "4":
            if not venta.items:
                print("  ⚠  El carrito está vacío. Agregue al menos un producto.")
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
    if categoria in ("Bebidas", "Licores"):
        print("\n  Presentación disponible:")
        for k, v in PRESENTACIONES_BEBIDAS.items():
            print(f"    [{k}] {v}")
        op = elegir_opcion(PRESENTACIONES_BEBIDAS, "  Presentación: ")
        return PRESENTACIONES_BEBIDAS[op]
    elif categoria == "Snacks":
        print("\n  Tamaño disponible:")
        for k, v in TALLAS_SNACKS.items():
            print(f"    [{k}] {v}")
        op = elegir_opcion(TALLAS_SNACKS, "  Tamaño: ")
        return TALLAS_SNACKS[op]
    else:
        return None


def menu_admin(tienda):
    while True:
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
            titulo("AGREGAR NUEVO PRODUCTO", char="─", n=64)

            nombre = pedir_texto("  Nombre del producto       : ")

            print("\n  Categoría:")
            for k, v in CATEGORIAS.items():
                iva = " (IVA 19%)" if v in CATEGORIAS_CON_IVA else ""
                print(f"    [{k}] {v}{iva}")
            cat_op    = elegir_opcion(CATEGORIAS, "  Categoría: ")
            categoria = CATEGORIAS[cat_op]

            presentacion = _pedir_presentacion(categoria)

            precio   = pedir_float("  Precio unitario ($)        : ")
            cantidad = pedir_entero("  Cantidad inicial (stock)   : ", minimo=0)

            tienda.agregar_producto(nombre, categoria, precio, cantidad, presentacion)
            # Mostrar la fila recién agregada
            nuevo = tienda.productos[-1]
            print(f"\n  Producto registrado:")
            print(f"  {'CÓD':>4}  {'PRODUCTO':<32}  {'CATEGORÍA':<12}  {'PRES.':<8}  {'PRECIO':>10}  {'STOCK':>6}")
            print(f"  {'─'*4}  {'─'*32}  {'─'*12}  {'─'*8}  {'─'*10}  {'─'*6}")
            tienda._fila_producto(nuevo, solo_stock=True)
            pausar()

        elif op == "3":
            titulo("REABASTECER PRODUCTO", char="─", n=64)
            prod = seleccionar_producto(tienda, solo_con_stock=False)
            if prod is None:
                continue
            print(f"\n  Producto: [{prod.codigo}] {prod.nombre_completo}")
            print(f"  Stock actual: {prod.cantidad}")
            unidades = pedir_entero("  Unidades a agregar: ", minimo=1)
            tienda.reabastecer(prod.codigo, unidades)
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
        print("\n")
        print("═" * 64)
        print(f"{'ESTANQUILLO  GLORIANA':^64}")
        print(f"{'Doña Gloria — Manizales':^64}")
        print("═" * 64)
        print("  [1]  Soy CLIENTE   → realizar compra")
        print("  [2]  Soy ADMIN     → administrar inventario")
        print("  [0]  Salir")
        print("═" * 64)
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
