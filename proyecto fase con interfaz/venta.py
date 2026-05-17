"""
venta.py
Clase Venta: registra ítems y calcula el desglose completo.
Adaptado para Flask: sin prints, retorna dicts para Jinja2.

Orden de cálculo:
  1. Precio base = precio_unitario × cantidad
  2. Descuento especial (chocolatina/papa) = −10% sobre ese ítem
  3. Base estrato = subtotal_bruto − desc_cat_total
  4. Descuento estrato = −X% sobre base_estrato
  5. IVA 19% sobre base_neta de ítems con IVA (Bebidas/Snacks)
  6. Total = (base_estrato − desc_estrato) + IVA
"""

import datetime


class Venta:
    def __init__(self, cliente):
        self.cliente = cliente
        self.fecha   = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M")
        self.items   = []   # lista de (Producto, cantidad)

    def agregar_item(self, producto, cantidad):
        """Agrega ítem y descuenta stock. Retorna (ok, mensaje)."""
        ok, msg = producto.vender(cantidad)
        if ok:
            self.items.append((producto, cantidad))
        return ok, msg

    def desglose(self):
        """
        Calcula y retorna un dict completo con todas las líneas y totales.
        Usado por Flask para renderizar el tiquete.
        """
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
                "categoria": prod.categoria,
                "presentacion": prod.presentacion or "—",
                "precio_unit": prod.precio,
                "cant":      cant,
                "base":      base,
                "d_cat_pct": 10 if prod.tiene_descuento_categoria() else 0,
                "d_cat":     d_cat,
                "tiene_iva": prod.tiene_iva,
                "iva":       iva,
                "tiene_desc": prod.tiene_descuento_categoria(),
            })

        base_estrato = subtotal_bruto - desc_cat_total
        desc_est     = base_estrato * (desc_est_pct / 100)
        base_final   = base_estrato - desc_est
        total        = base_final + iva_total

        return {
            "cliente":      self.cliente.to_dict(),
            "fecha":        self.fecha,
            "lineas":       lineas,
            "subtotal":     subtotal_bruto,
            "desc_cat":     desc_cat_total,
            "base_estrato": base_estrato,
            "desc_est_pct": desc_est_pct,
            "desc_est":     desc_est,
            "iva":          iva_total,
            "total":        total,
        }
