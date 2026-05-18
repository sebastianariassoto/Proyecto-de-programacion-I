"""
main.py — Estanquillo Gloriana
==============================
  [1] Soy CLIENTE  -> catalogo, carrito, tiquete
  [2] Soy ADMIN    -> inventario, agregar, reabastecer
  [0] Salir
"""

from estanquillo import Estanquillo
from cliente     import Cliente
from venta       import Venta
from producto    import CATEGORIAS, PRESENTACIONES_BEBIDAS, TALLAS_SNACKS, CATEGORIAS_CON_IVA


# ═══════════════════════════════════════════════════════
#  UTILIDADES
# ═══════════════════════════════════════════════════════

def sep(n=68, char="="):
    print(char * n)

def titulo(texto, char="=", n=68):
    print(f"\n{char*n}")
    print(f"   {texto}")
    print(f"{char*n}")

def pausar(msg="  Presione ENTER para continuar..."):
    input(msg)

def pedir_entero(msg, minimo=None, maximo=None):
    while True:
        try:
            v = int(input(msg))
            if minimo is not None and v < minimo:
                print(f"  [!] Minimo permitido: {minimo}")
                continue
            if maximo is not None and v > maximo:
                print(f"  [!] Maximo permitido: {maximo}")
                continue
            return v
        except ValueError:
            print("  [!] Ingrese un numero entero valido.")

def pedir_float(msg, minimo=0.01):
    while True:
        raw = input(msg).strip().replace(",", ".")
        try:
            v = float(raw)
            if v < minimo:
                print(f"  [!] Debe ser mayor a {minimo}")
                continue
            return v
        except ValueError:
            print("  [!] Ingrese un numero valido (ej: 3500).")

def pedir_texto(msg):
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("  [!] El campo no puede estar vacio.")

def elegir_opcion(opciones_dict, msg="  Opcion: "):
    while True:
        v = input(msg).strip()
        if v in opciones_dict:
            return v
        claves = ", ".join(opciones_dict.keys())
        print(f"  [!] Opcion no valida. Elija entre: {claves}")


# ═══════════════════════════════════════════════════════
#  BUSQUEDA DE PRODUCTO — codigo directo o por tabla
# ═══════════════════════════════════════════════════════

def seleccionar_producto(tienda, solo_con_stock=True):
    """
    Permite elegir un producto:
      [1] Ingresar codigo directamente (sin mostrar inventario)
      [2] Ver tabla completa y luego ingresar codigo
    Devuelve objeto Producto o None.
    """
    while True:
        print("\n  Como desea seleccionar el producto?")
        print("  [1] Ingresar el codigo directamente")
        print("  [2] Ver tabla y luego ingresar codigo")
        print("  [0] Cancelar")
        op = input("  Opcion: ").strip()

        if op == "1":
            codigo = pedir_entero("  Codigo del producto: ", minimo=1)
            prod = tienda.buscar_producto(codigo)
            if prod is None:
                print(f"  [!] No existe producto con codigo [{codigo}].")
                continue
            if solo_con_stock and prod.cantidad == 0:
                print(f"  [!] '{prod.nombre_completo}' esta AGOTADO.")
                continue
            return prod

        elif op == "2":
            if solo_con_stock:
                tienda.mostrar_catalogo_cliente()
            else:
                tienda.mostrar_tabla_compacta()
            # Aqui ya se vio toda la tabla; ahora el usuario ingresa el codigo
            codigo = pedir_entero("  Ingrese el codigo del producto: ", minimo=1)
            prod = tienda.buscar_producto(codigo)
            if prod is None:
                print(f"  [!] No existe producto con codigo [{codigo}].")
                continue
            if solo_con_stock and prod.cantidad == 0:
                print(f"  [!] '{prod.nombre_completo}' esta AGOTADO.")
                continue
            return prod

        elif op == "0":
            return None
        else:
            print("  [!] Opcion no valida.")


# ═══════════════════════════════════════════════════════
#  MENU CLIENTE
# ═══════════════════════════════════════════════════════

def _mostrar_carrito(venta):
    if not venta.items:
        print("\n  (carrito vacio)\n")
        return
    W = 62
    print(f"\n  {'─'*W}")
    print(f"  {'PRODUCTO':<30}  {'CANT':>4}  {'P.UNIT':>9}  {'SUBTOTAL':>10}")
    print(f"  {'─'*W}")
    total = 0
    for prod, cant in venta.items:
        sub = prod.precio * cant
        total += sub
        nom = prod.nombre_completo
        nom = nom[:30] if len(nom) <= 30 else nom[:28] + ".."
        print(f"  {nom:<30}  x{cant:<3}  ${prod.precio:>8,.0f}  ${sub:>9,.0f}")
    print(f"  {'─'*W}")
    print(f"  {'Aprox. bruto (sin IVA ni descuentos)':<48}  ${total:>9,.0f}\n")


def menu_cliente(tienda):
    titulo("BIENVENIDO — Estanquillo Gloriana")

    nombre  = pedir_texto("  Su nombre   : ")
    estrato = pedir_entero("  Su estrato  : ", minimo=1, maximo=6)
    cliente = Cliente(nombre, estrato)

    d_pct = cliente.descuento_pct()
    if d_pct > 0:
        print(f"\n  Hola {cliente.nombre}! Descuento por estrato {estrato}: {d_pct}%")
    else:
        print(f"\n  Hola {cliente.nombre}! Sin descuento adicional (estrato {estrato}).")

    disponibles = [p for p in tienda.productos if p.cantidad > 0]
    if not disponibles:
        print("\n  No hay productos disponibles. Vuelva pronto.")
        pausar()
        return

    venta = Venta(cliente)

    while True:
        print(f"\n{'─'*68}")
        print(f"  COMPRA — {cliente.nombre}  |  Estrato {estrato}  |  Items en carrito: {len(venta.items)}")
        print(f"{'─'*68}")
        print("  [1] Agregar producto al carrito")
        print("  [2] Ver carrito actual")
        print("  [3] Ver catalogo completo")
        print("  [4] Finalizar y ver tiquete")
        print("  [0] Cancelar y volver")
        op = input("  Opcion: ").strip()

        if op == "1":
            prod = seleccionar_producto(tienda, solo_con_stock=True)
            if prod is None:
                continue
            print(f"\n  Seleccionado: [{prod.codigo}] {prod.nombre_completo}")
            print(f"  Precio: ${prod.precio:,.0f}  |  Stock disponible: {prod.cantidad}", end="")
            extras = []
            if prod.tiene_iva:
                extras.append("+IVA 19%")
            if prod.tiene_descuento_categoria():
                extras.append("DESC especial 10%")
            if extras:
                print(f"  |  {' | '.join(extras)}", end="")
            print()
            cantidad = pedir_entero(
                f"  Cantidad (1-{prod.cantidad}): ",
                minimo=1, maximo=prod.cantidad
            )
            ok = venta.agregar_item(prod, cantidad)
            if ok:
                print(f"  [OK] '{prod.nombre_completo}' x{cantidad} agregado al carrito.")

        elif op == "2":
            _mostrar_carrito(venta)
            pausar()

        elif op == "3":
            tienda.mostrar_catalogo_cliente()
            pausar()

        elif op == "4":
            if not venta.items:
                print("  [!] El carrito esta vacio. Agregue al menos un producto.")
                continue
            venta.mostrar_tiquete()
            pausar()
            break

        elif op == "0":
            print("  Compra cancelada.")
            break
        else:
            print("  [!] Opcion no valida.")


# ═══════════════════════════════════════════════════════
#  MENU ADMINISTRADOR
# ═══════════════════════════════════════════════════════

def _pedir_presentacion(categoria):
    if categoria in ("Gaseosas", "Licores"):
        print("\n  Presentacion:")
        for k, v in PRESENTACIONES_BEBIDAS.items():
            print(f"    [{k}] {v}")
        op = elegir_opcion(PRESENTACIONES_BEBIDAS, "  Presentacion: ")
        return PRESENTACIONES_BEBIDAS[op]
    elif categoria == "Snacks":
        print("\n  Tamano:")
        for k, v in TALLAS_SNACKS.items():
            print(f"    [{k}] {v}")
        op = elegir_opcion(TALLAS_SNACKS, "  Tamano: ")
        return TALLAS_SNACKS[op]
    else:
        return None   # Cigarrillos sin presentacion


def menu_admin(tienda):
    while True:
        titulo("PANEL ADMINISTRADOR — Gloriana")
        print("  [1] Ver inventario completo")
        print("  [2] Agregar nuevo producto")
        print("  [3] Reabastecer producto existente")
        print("  [0] Volver al menu principal")
        sep()
        op = input("  Opcion: ").strip()

        if op == "1":
            tienda.mostrar_inventario()
            # El inventario ya incluye pausa por paginas; al terminar pregunta si reabastecer
            r = input("  Desea reabastecer algun producto ahora? (s/n): ").strip().lower()
            if r == "s":
                _flujo_reabastecer(tienda)

        elif op == "2":
            titulo("AGREGAR NUEVO PRODUCTO", char="-", n=68)
            nombre = pedir_texto("  Nombre del producto       : ")

            print("\n  Categoria:")
            for k, v in CATEGORIAS.items():
                iva = " (IVA 19%)" if v in CATEGORIAS_CON_IVA else ""
                print(f"    [{k}] {v}{iva}")
            cat_op    = elegir_opcion(CATEGORIAS, "  Categoria: ")
            categoria = CATEGORIAS[cat_op]

            presentacion = _pedir_presentacion(categoria)
            precio       = pedir_float("  Precio unitario ($)        : ")
            cantidad     = pedir_entero("  Cantidad inicial (stock)   : ", minimo=0)

            nuevo = tienda.agregar_producto(nombre, categoria, precio, cantidad, presentacion)
            print(f"\n  Producto registrado:")
            print(f"  {'COD':>4}  {'PRODUCTO':<26}  {'CATEGORIA':<12}  "
                  f"{'PRES.':<8}  {'PRECIO':>10}  {'STOCK':>6}")
            print(f"  {'─'*4}  {'─'*26}  {'─'*12}  {'─'*8}  {'─'*10}  {'─'*6}")
            tienda._fila(nuevo, admin=True)
            pausar()

        elif op == "3":
            _flujo_reabastecer(tienda)

        elif op == "0":
            break
        else:
            print("  [!] Opcion no valida.")


def _flujo_reabastecer(tienda):
    """Flujo independiente: muestra tabla, pide codigo, agrega unidades. Repetible."""
    while True:
        titulo("REABASTECER PRODUCTO", char="-", n=68)
        prod = seleccionar_producto(tienda, solo_con_stock=False)
        if prod is None:
            break
        print(f"\n  Producto : [{prod.codigo}] {prod.nombre_completo}")
        print(f"  Categoria: {prod.categoria}   Presentacion: {prod.presentacion or '---'}")
        print(f"  Precio   : ${prod.precio:,.0f}")
        print(f"  Stock actual: {prod.cantidad}")
        unidades = pedir_entero("  Unidades a agregar (0 = cancelar): ", minimo=0)
        if unidades == 0:
            print("  Operacion cancelada.")
        else:
            tienda.reabastecer(prod.codigo, unidades)

        r = input("\n  Reabastecer otro producto? (s/n): ").strip().lower()
        if r != "s":
            break


# ═══════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ═══════════════════════════════════════════════════════

def main():
    tienda = Estanquillo()

    while True:
        print("\n")
        print("=" * 68)
        print(f"{'ESTANQUILLO  GLORIANA':^68}")
        
        print("=" * 68)
        print("  [1]  Soy CLIENTE   -> realizar compra")
        print("  [2]  Soy ADMIN     -> administrar inventario")
        print("  [0]  Salir")
        print("=" * 68)
        op = input("  Quien es usted? ").strip()

        if op == "1":
            menu_cliente(tienda)
        elif op == "2":
            menu_admin(tienda)
        elif op == "0":
            print("\n  Hasta luego. Vuelva pronto al Estanquillo Gloriana!\n")
            break
        else:
            print("  [!] Opcion no valida. Ingrese 1, 2 o 0.")


if __name__ == "__main__":
    main()
