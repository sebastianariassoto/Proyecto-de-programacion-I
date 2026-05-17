"""
venta.py
Clase Venta: registra ítems y genera el tiquete con desglose completo.

Orden de cálculo:
  1. Precio base = precio_unitario × cantidad
  2. Descuento especial (chocolatina/papa) = −10% sobre ese ítem
  3. base_estrato = suma de bases netas
  4. Descuento de estrato = −X% sobre base_estrato
  5. IVA 19% sobre ítems de Bebidas/Snacks (después de descuentos)
  6. Total = base_estrato − desc_estrato + IVA
"""

import datetime


class Venta:
    def __init__(self, cliente):
        self.cliente = cliente
        self.fecha   = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M")
        self.items   = []

    def agregar_item(self, producto, cantidad):
        ok = producto.vender(cantidad)
        if ok:
            # Si ya existe el mismo producto en el carrito, sumar
            for i, (p, c) in enumerate(self.items):
                if p.codigo == producto.codigo:
                    self.items[i] = (p, c + cantidad)
                    return ok
            self.items.append((producto, cantidad))
        return ok

    def _desglose(self):
        lineas         = []
        subtotal_bruto = 0.0
        desc_cat_total = 0.0
        iva_total      = 0.0
        desc_est_pct   = self.cliente.descuento_pct()

        for prod, cant in self.items:
            base  = prod.precio * cant
            d_cat = base * 0.10 if prod.tiene_descuento_categoria() else 0.0
            base_neta = base - d_cat
            iva   = base_neta * 0.19 if prod.tiene_iva else 0.0

            subtotal_bruto += base
            desc_cat_total += d_cat
            iva_total      += iva

            lineas.append({
                "nombre":    prod.nombre_completo,
                "cant":      cant,
                "base":      base,
                "d_cat_pct": 10 if prod.tiene_descuento_categoria() else 0,
                "d_cat":     d_cat,
                "tiene_iva": prod.tiene_iva,
                "iva":       iva,
            })

        base_estrato = subtotal_bruto - desc_cat_total
        desc_est     = base_estrato * (desc_est_pct / 100)
        base_final   = base_estrato - desc_est
        total        = base_final + iva_total

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

    def mostrar_tiquete(self):
        if not self.items:
            print("  La venta no tiene productos.")
            return

        d   = self._desglose()
        W   = 58
        SEP = "=" * W
        LIN = "-" * W

        print(f"\n{SEP}")
        print(f"{'ESTANQUILLO  GLORIANA':^{W}}")
        print(f"{'Doña Gloria — Manizales':^{W}}")
        print(f"{'TIQUETE DE VENTA':^{W}}")
        print(SEP)
        print(f"  Cliente : {self.cliente.nombre}")
        print(f"  Estrato : {self.cliente.estrato}  |  Descuento estrato: {d['desc_est_pct']}%")
        print(f"  Fecha   : {self.fecha}")
        print(LIN)
        # Encabezado columnas
        print(f"  {'PRODUCTO':<30} {'CANT':>5}  {'P.UNIT':>10}  {'VALOR':>10}")
        print(LIN)

        for l in d["lineas"]:
            precio_unit = l["base"] / l["cant"]
            print(f"  {l['nombre']:<30} x{l['cant']:<4}  ${precio_unit:>9,.0f}  ${l['base']:>9,.0f}")
            if l["d_cat_pct"] > 0:
                print(f"    {'└ Desc. especial ' + str(l['d_cat_pct']) + '%':<44}  -${l['d_cat']:>8,.0f}")
            if l["tiene_iva"]:
                print(f"    {'└ IVA 19%':<44}  +${l['iva']:>8,.0f}")

        print(LIN)
        print(f"  {'Subtotal bruto':<50}  ${d['subtotal']:>9,.0f}")
        if d["desc_cat"] > 0:
            print(f"  {'Desc. especial (chocolatina / papa)':<50}  -${d['desc_cat']:>8,.0f}")
        if d["desc_est_pct"] > 0:
            lbl = f"Desc. estrato {d['desc_est_pct']}%"
            print(f"  {lbl:<50}  -${d['desc_est']:>8,.0f}")
        print(f"  {'IVA 19% (Bebidas y Snacks)':<50}  +${d['iva']:>8,.0f}")
        print(SEP)
        print(f"  {'TOTAL A PAGAR':<50}  ${d['total']:>9,.0f}")
        print(f"{SEP}\n")
