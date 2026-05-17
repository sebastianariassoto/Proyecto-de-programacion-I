"""
app.py — Estanquillo Gloriana (Flask)
======================================
Rutas:
  GET  /                  → pantalla bienvenida (elegir cliente o admin)
  GET  /cliente           → formulario datos cliente
  POST /cliente           → guardar cliente en sesión → redirige a catálogo
  GET  /catalogo          → catálogo en tabla horizontal por categoría
  POST /carrito/agregar   → agregar producto al carrito
  POST /carrito/cambiar   → cambiar cantidad en carrito
  POST /carrito/eliminar  → eliminar ítem del carrito
  GET  /carrito           → ver carrito con resumen de totales
  POST /tiquete           → generar y mostrar tiquete final
  GET  /admin             → panel admin (inventario completo)
  POST /admin/agregar     → agregar nuevo producto
  POST /admin/reabastecer → reabastecer producto existente
"""

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from estanquillo import Estanquillo
from cliente     import Cliente
from venta       import Venta
from producto    import CATEGORIAS, PRESENTACIONES_BEBIDAS, TALLAS_SNACKS, CATEGORIAS_CON_IVA

app = Flask(__name__)
app.secret_key = "gloriana-secret-2024"

# ── instancia global de la tienda (memoria RAM) ───────────────────────────
tienda = Estanquillo()


# ══════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════

def get_carrito():
    """Retorna el carrito de la sesión: {codigo_str: {nombre, precio, cant, ...}}"""
    return session.get("carrito", {})

def guardar_carrito(carrito):
    session["carrito"] = carrito
    session.modified = True

def calcular_resumen(carrito_dict, cliente_dict):
    """Calcula subtotales y total a partir de los dicts de sesión."""
    from cliente import DESCUENTOS_ESTRATO
    from producto import CATEGORIAS_CON_IVA, PALABRAS_DESC_PROD

    subtotal_bruto = 0.0
    desc_cat_total = 0.0
    iva_total      = 0.0
    desc_est_pct   = DESCUENTOS_ESTRATO.get(int(cliente_dict["estrato"]), 0)
    lineas         = []

    for cod, item in carrito_dict.items():
        base  = item["precio"] * item["cant"]
        n     = item["nombre"].lower()
        tiene_desc = any(p in n for p in PALABRAS_DESC_PROD)
        tiene_iva  = item["categoria"] in CATEGORIAS_CON_IVA
        d_cat      = base * 0.10 if tiene_desc else 0.0
        base_neta  = base - d_cat
        iva        = base_neta * 0.19 if tiene_iva else 0.0

        subtotal_bruto += base
        desc_cat_total += d_cat
        iva_total      += iva

        lineas.append({
            **item,
            "base":      base,
            "d_cat":     d_cat,
            "d_cat_pct": 10 if tiene_desc else 0,
            "tiene_iva": tiene_iva,
            "iva":       iva,
            "tiene_desc": tiene_desc,
        })

    base_estrato = subtotal_bruto - desc_cat_total
    desc_est     = base_estrato * (desc_est_pct / 100)
    total        = (base_estrato - desc_est) + iva_total

    return {
        "lineas":       lineas,
        "subtotal":     subtotal_bruto,
        "desc_cat":     desc_cat_total,
        "base_estrato": base_estrato,
        "desc_est_pct": desc_est_pct,
        "desc_est":     desc_est,
        "iva":          iva_total,
        "total":        total,
    }


# ══════════════════════════════════════════════════════════════
#  RUTAS PRINCIPALES
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


# ── CLIENTE ───────────────────────────────────────────────────

@app.route("/cliente", methods=["GET", "POST"])
def cliente_form():
    if request.method == "POST":
        nombre  = request.form.get("nombre", "").strip()
        estrato = request.form.get("estrato", "4")
        if not nombre:
            flash("Por favor ingrese su nombre.", "danger")
            return redirect(url_for("cliente_form"))
        c = Cliente(nombre, estrato)
        session["cliente"] = c.to_dict()
        session["carrito"] = {}
        return redirect(url_for("catalogo"))
    return render_template("cliente_form.html")


@app.route("/catalogo")
def catalogo():
    if "cliente" not in session:
        return redirect(url_for("cliente_form"))
    cliente   = session["cliente"]
    catalogo  = tienda.catalogo_por_categoria()
    carrito   = get_carrito()
    n_items   = sum(i["cant"] for i in carrito.values())
    cat_activa = request.args.get("cat", list(catalogo.keys())[0] if catalogo else "Bebidas")
    return render_template("catalogo.html",
                           cliente=cliente,
                           catalogo=catalogo,
                           carrito=carrito,
                           n_items=n_items,
                           cat_activa=cat_activa)


@app.route("/carrito/agregar", methods=["POST"])
def carrito_agregar():
    if "cliente" not in session:
        return redirect(url_for("cliente_form"))
    codigo = request.form.get("codigo")
    cant   = int(request.form.get("cantidad", 1))
    cat_activa = request.form.get("cat_activa", "Bebidas")

    prod = tienda.buscar_producto(codigo)
    if not prod:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("catalogo", cat=cat_activa))

    if cant < 1 or cant > prod.cantidad:
        flash(f"Cantidad inválida. Stock disponible: {prod.cantidad}", "danger")
        return redirect(url_for("catalogo", cat=cat_activa))

    carrito = get_carrito()
    cod_str = str(prod.codigo)
    if cod_str in carrito:
        nueva = carrito[cod_str]["cant"] + cant
        if nueva > prod.cantidad:
            flash(f"No hay suficiente stock. Máximo: {prod.cantidad}", "warning")
            nueva = prod.cantidad
        carrito[cod_str]["cant"] = nueva
    else:
        carrito[cod_str] = {
            "codigo":     prod.codigo,
            "nombre":     prod.nombre_completo,
            "nombre_base": prod.nombre,
            "categoria":  prod.categoria,
            "presentacion": prod.presentacion or "—",
            "precio":     prod.precio,
            "cant":       cant,
            "stock_max":  prod.cantidad,
        }

    guardar_carrito(carrito)
    flash(f"'{prod.nombre_completo}' agregado al carrito.", "success")
    return redirect(url_for("catalogo", cat=cat_activa))


@app.route("/carrito/cambiar", methods=["POST"])
def carrito_cambiar():
    codigo = request.form.get("codigo")
    delta  = int(request.form.get("delta", 0))
    carrito = get_carrito()
    if codigo in carrito:
        prod = tienda.buscar_producto(int(codigo))
        nueva = carrito[codigo]["cant"] + delta
        if nueva <= 0:
            del carrito[codigo]
        else:
            max_stock = prod.cantidad + carrito[codigo]["cant"] if prod else carrito[codigo]["cant"]
            carrito[codigo]["cant"] = min(nueva, max_stock)
    guardar_carrito(carrito)
    return redirect(url_for("carrito_ver"))


@app.route("/carrito/eliminar", methods=["POST"])
def carrito_eliminar():
    codigo  = request.form.get("codigo")
    carrito = get_carrito()
    if codigo in carrito:
        del carrito[codigo]
    guardar_carrito(carrito)
    return redirect(url_for("carrito_ver"))


@app.route("/carrito")
def carrito_ver():
    if "cliente" not in session:
        return redirect(url_for("cliente_form"))
    cliente = session["cliente"]
    carrito = get_carrito()
    resumen = calcular_resumen(carrito, cliente) if carrito else None
    return render_template("carrito.html",
                           cliente=cliente,
                           carrito=carrito,
                           resumen=resumen)


@app.route("/tiquete", methods=["POST"])
def tiquete():
    if "cliente" not in session:
        return redirect(url_for("cliente_form"))
    carrito = get_carrito()
    if not carrito:
        flash("El carrito está vacío.", "warning")
        return redirect(url_for("carrito_ver"))

    cliente_dict = session["cliente"]
    c = Cliente(cliente_dict["nombre"], cliente_dict["estrato"])
    v = Venta(c)

    errores = []
    for cod, item in carrito.items():
        prod = tienda.buscar_producto(int(cod))
        if prod:
            ok, msg = v.agregar_item(prod, item["cant"])
            if not ok:
                errores.append(msg)

    if errores:
        for e in errores:
            flash(e, "danger")
        return redirect(url_for("carrito_ver"))

    desglose = v.desglose()
    session["carrito"] = {}
    return render_template("tiquete.html", desglose=desglose)


# ── ADMIN ─────────────────────────────────────────────────────

@app.route("/admin")
def admin():
    inventario = tienda.inventario_por_categoria()
    total_ref  = tienda.total_referencias()
    return render_template("admin.html",
                           inventario=inventario,
                           total_ref=total_ref,
                           categorias=CATEGORIAS,
                           presentaciones=PRESENTACIONES_BEBIDAS,
                           tallas=TALLAS_SNACKS,
                           cats_iva=CATEGORIAS_CON_IVA)


@app.route("/admin/agregar", methods=["POST"])
def admin_agregar():
    nombre    = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "")
    precio    = request.form.get("precio", 0)
    cantidad  = request.form.get("cantidad", 0)
    pres_raw  = request.form.get("presentacion", "").strip()
    presentacion = pres_raw if pres_raw else None

    if not nombre or not categoria:
        flash("Nombre y categoría son obligatorios.", "danger")
        return redirect(url_for("admin"))

    try:
        precio   = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        flash("Precio y cantidad deben ser numéricos.", "danger")
        return redirect(url_for("admin"))

    p = tienda.agregar_producto(nombre, categoria, precio, cantidad, presentacion)
    flash(f"Producto '{p.nombre_completo}' agregado con código [{p.codigo}].", "success")
    return redirect(url_for("admin"))


@app.route("/admin/reabastecer", methods=["POST"])
def admin_reabastecer():
    codigo   = request.form.get("codigo")
    unidades = request.form.get("unidades", 0)
    try:
        unidades = int(unidades)
    except ValueError:
        flash("Las unidades deben ser un número entero.", "danger")
        return redirect(url_for("admin"))

    prod, nuevo_stock = tienda.reabastecer(codigo, unidades)
    if prod:
        flash(f"'{prod.nombre_completo}' reabastecido. Stock actual: {nuevo_stock}.", "success")
    else:
        flash(f"No existe producto con código [{codigo}].", "danger")
    return redirect(url_for("admin"))


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app.run(debug=True)
