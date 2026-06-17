# tests/test_carrito_defecto.py
import pytest
from src.carrito import aplicar_descuento

# ---------------------------------------------------------------------------
# DEFECTO LAB10-001
# aplicar_descuento() no valida que 'total' sea >= 0 como entrada.
# Si un total negativo llega (p. ej. resultado de un cálculo externo erróneo),
# la función retorna un valor aún más negativo sin lanzar excepción.
#
# Escenario de la guía:
#   Audífonos con precio ya rebajado $1.990 (original $3.980 − 50% off).
#   Representado internamente como −1990 por error externo de cálculo.
#   aplicar_descuento(−1990, 60) → −796.0  ← VALOR NEGATIVO no controlado.
#
# Corrección esperada: lanzar ValueError si total < 0.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('total,porcentaje,esperado_minimo', [
    # (total original positivo, % descuento, valor mínimo aceptable = 0)
    (1990,  60, 0),   # escenario guía: $1990 con cupón 60% → $796 (debe ser >= 0)
    (500,   80, 0),   # caso límite: alto porcentaje
    (1000, 100, 0),   # descuento total → resultado debe ser exactamente 0
    (2000,  50, 0),   # 50% exacto → frontera, resultado = 1000
])
def test_descuento_no_genera_total_negativo(total, porcentaje, esperado_minimo):
    """El resultado de aplicar_descuento() NUNCA debe ser menor a 0."""
    # Arrange  (parámetros definidos arriba)

    # Act
    resultado = aplicar_descuento(total, porcentaje)

    # Assert
    assert resultado >= esperado_minimo, (
        f'Total con descuento {porcentaje}% sobre {total} fue {resultado}, '
        f'se esperaba >= {esperado_minimo}'
    )


@pytest.mark.parametrize('total_negativo,porcentaje', [
    (-1990,  60),   # escenario guía con total negativo
    (-500,   80),   # caso límite
    (-1000, 100),   # descuento total sobre negativo
    (-2000,  50),   # 50% sobre total negativo
])
def test_total_negativo_lanza_error(total_negativo, porcentaje):
    """La función debe lanzar ValueError si 'total' es negativo (defecto LAB10-001)."""
    # Arrange  (parámetros definidos arriba)

    # Act / Assert
    with pytest.raises(ValueError, match='no negativo'):
        aplicar_descuento(total_negativo, porcentaje)
