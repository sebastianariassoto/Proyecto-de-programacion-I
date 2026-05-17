# Estanquillo Gloriana — Flask

Aplicación web completa para el Estanquillo Gloriana. Clientes pueden ver el catálogo en tabla horizontal, agregar productos al carrito y generar su tiquete. El administrador puede ver el inventario completo, agregar productos y reabastecer.

## Estructura del proyecto

```
gloriana/
├── app.py              ← Servidor Flask (rutas)
├── cliente.py          ← Clase Cliente
├── estanquillo.py      ← Clase Estanquillo (inventario en RAM)
├── producto.py         ← Clase Producto
├── venta.py            ← Clase Venta (cálculo de tiquete)
├── requirements.txt
├── templates/
│   ├── base.html       ← Layout base con navbar
│   ├── index.html      ← Pantalla de bienvenida
│   ├── cliente_form.html
│   ├── catalogo.html   ← Catálogo en tabla horizontal
│   ├── carrito.html    ← Carrito con resumen de totales
│   ├── tiquete.html    ← Tiquete final
│   └── admin.html      ← Panel administrador
└── static/
    └── style.css
```

## Instalación y ejecución

```bash
# 1. Instalar Flask
pip install -r requirements.txt

# 2. Ejecutar
python app.py
```

Abrir en el navegador: http://127.0.0.1:5000

## Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Pantalla de bienvenida |
| `/cliente` | Formulario datos del cliente |
| `/catalogo` | Catálogo por categoría en tabla horizontal |
| `/carrito` | Carrito con subtotales y total |
| `/tiquete` | Tiquete final de venta |
| `/admin` | Panel administrador (inventario, agregar, reabastecer) |

## Lógica de cálculo (sin cambios respecto al Python original)

1. Precio base = precio_unitario × cantidad
2. Descuento especial (chocolatina/papa) = −10% por ítem
3. Base estrato = subtotal − desc_especial
4. Descuento estrato: estrato 1→10%, 2→5%, 3→2%
5. IVA 19% sobre ítems de Bebidas y Snacks
6. Total = (base_estrato − desc_estrato) + IVA

## Nota

Los datos viven en memoria RAM. Al reiniciar el servidor el inventario vuelve al estado inicial.
