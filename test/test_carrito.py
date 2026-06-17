# tests/test_carrito.py
import pytest
from src.carrito import agregar_al_carrito, calcular_total, aplicar_descuento

# ── agregar_al_carrito ────────────────────────────────────────────────
def test_agregar_producto_valido():
    carrito = []
    resultado = agregar_al_carrito(carrito, {'nombre': 'Laptop', 'precio': 999.99, 'cantidad': 1})
    assert len(resultado) == 1
    assert resultado[0]['nombre'] == 'Laptop'

def test_agregar_precio_negativo_lanza_error():
    with pytest.raises(ValueError):
        agregar_al_carrito([], {'nombre': 'X', 'precio': -10, 'cantidad': 1})

def test_agregar_cantidad_cero_lanza_error():
    with pytest.raises(ValueError):
        agregar_al_carrito([], {'nombre': 'X', 'precio': 10, 'cantidad': 0})

# ── calcular_total ────────────────────────────────────────────────────
def test_calcular_total_multiples_productos():
    carrito = [
        {'nombre': 'A', 'precio': 100.0, 'cantidad': 2},
        {'nombre': 'B', 'precio': 50.0,  'cantidad': 3},
    ]
    assert calcular_total(carrito) == 350.0

def test_calcular_total_carrito_vacio():
    assert calcular_total([]) == 0.0

# ── aplicar_descuento ────────────────────────────────────────────────
def test_descuento_estandar():
    assert aplicar_descuento(10000, 10) == 9000.0

def test_descuento_cero():
    assert aplicar_descuento(10000, 0) == 10000.0

def test_descuento_total_100():
    assert aplicar_descuento(10000, 100) == 0.0

def test_porcentaje_invalido_lanza_error():
    with pytest.raises(ValueError):
        aplicar_descuento(10000, 110)
