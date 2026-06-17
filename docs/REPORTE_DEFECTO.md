# Reporte de Defecto - LAB10-001

## ID y Título

**LAB10-001:** `aplicar_descuento()` permite total negativo al recibir un valor de entrada
negativo, sin lanzar excepción ni garantizar que el resultado sea ≥ 0.

---

## Pasos para reproducir

1. Instalar dependencias: `pip install pytest pytest-cov`.
2. Crear el entorno del laboratorio con la estructura indicada en la guía (sección 2.1).
3. Copiar el código del SUT original (sin corrección) en `src/carrito.py`.
4. Ejecutar el siguiente script desde la raíz del proyecto:

```python
from src.carrito import agregar_al_carrito, calcular_total, aplicar_descuento

carrito = []
# Producto con precio ya rebajado: $1.990 (precio original $3.980 con 50% off)
agregar_al_carrito(carrito, {'nombre': 'Audífonos', 'precio': 1990, 'cantidad': 1})
total = calcular_total(carrito)        # → 1990
# Simular total negativo producto de un cálculo externo erróneo
total_erroneo = -total                 # → -1990
resultado = aplicar_descuento(total_erroneo, 60)
print(resultado)                       # → -796.0  ← VALOR NEGATIVO
```

5. Observar que la función retorna `-796.0` sin lanzar ninguna excepción.

---

## Resultado esperado

`aplicar_descuento()` debe lanzar un `ValueError` con mensaje descriptivo cuando el
parámetro `total` sea negativo, o en su defecto garantizar que el valor retornado sea
siempre ≥ 0. Según la regla de negocio, ningún total de carrito puede ser negativo.

---

## Resultado obtenido

La función retorna `-796.0` para la llamada `aplicar_descuento(-1990, 60)`, sin lanzar
ninguna excepción. El resultado negativo es incorrecto y viola la invariante de negocio
de que un total de carrito nunca puede ser menor a cero.

---

## Severidad y Prioridad

| Dimensión   | Nivel  | Justificación                                                                                                                                                                               |
|-------------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Severidad** | **Alta** | *Impacto técnico:* el defecto corrompe silenciosamente el estado financiero del carrito. Un total negativo podría propagarse a módulos de pago o contabilidad generando cobros incorrectos o abonos no autorizados al cliente. No produce un crash observable, lo que lo hace más peligroso (falla silenciosa). |
| **Prioridad** | **Alta** | *Urgencia de negocio:* cualquier flujo que encadene un cálculo de descuento con un valor de entrada no validado expone al sistema a emitir órdenes de pago negativas. En un entorno de producción de e-commerce esto representa riesgo financiero directo y debe corregirse antes del siguiente despliegue. |

---

## Entorno

| Campo           | Valor                           |
|-----------------|---------------------------------|
| Python          | 3.12.3 (GCC 13.3.0)             |
| pytest          | 9.1.0                           |
| pytest-cov      | 7.1.0                           |
| Sistema operativo | Linux 6.18.5 (Ubuntu 24.04)   |
| Módulo afectado | `src/carrito.py` — función `aplicar_descuento()` |
| Datos de prueba | `total = -1990`, `porcentaje = 60` |

---

## Evidencia

**Salida de consola — ejecución del script de reproducción (SUT original):**

```
$ python reproduce_bug.py
-796.0
```

**Salida de pytest — ejecución del test parametrizado antes de la corrección:**

```
FAILED tests/test_carrito_defecto.py::test_total_negativo_lanza_error[-1990-60]
AssertionError: DID NOT RAISE <class 'ValueError'>

FAILED tests/test_carrito_defecto.py::test_total_negativo_lanza_error[-500-80]
AssertionError: DID NOT RAISE <class 'ValueError'>

FAILED tests/test_carrito_defecto.py::test_total_negativo_lanza_error[-1000-100]
AssertionError: DID NOT RAISE <class 'ValueError'>

FAILED tests/test_carrito_defecto.py::test_total_negativo_lanza_error[-2000-50]
AssertionError: DID NOT RAISE <class 'ValueError'>

========================= 4 failed, 9 passed in 0.07s =========================
```

---

## Análisis de Causa Raíz (RCA)

### ¿Qué condición no está siendo validada en `aplicar_descuento()`?

La función **no valida que el parámetro `total` sea mayor o igual a cero** antes de
operar sobre él. La precondición `total >= 0` está indicada en el docstring (`debe ser
>= 0`) pero nunca se impone mediante código, por lo que cualquier valor negativo que
llegue a la función se procesa sin control, produciendo un resultado igualmente negativo.

### ¿Por qué la validación `porcentaje > 100` ya existente no es suficiente?

La validación existente únicamente restringe el dominio del parámetro `porcentaje` al
rango `[0, 100]`. Sin embargo, esto **no protege contra un `total` negativo**. La
fórmula `total − (total × porcentaje / 100)` opera correctamente cuando `total ≥ 0`:
para cualquier porcentaje en `[0, 100]` el resultado siempre será ≥ 0. El problema surge
cuando `total < 0`, caso en que la misma fórmula produce un resultado negativo (de menor
módulo que `total`, pero negativo). El rango válido del porcentaje no guarda relación con
el signo del total, por lo que ambas validaciones son independientes y ambas necesarias.

### ¿Qué cambio mínimo en la función resolvería el defecto sin alterar los tests existentes?

Agregar **una validación del parámetro `total`** inmediatamente después de la validación
del porcentaje:

```python
if total < 0:
    raise ValueError('El total debe ser un valor no negativo.')
```

Y adicionalmente aplicar `max(0.0, ...)` al valor de retorno como salvaguarda defensiva:

```python
return max(0.0, total - (total * porcentaje / 100))
```

Ninguno de los tests existentes en `test_carrito.py` pasa un `total` negativo a
`aplicar_descuento()`, por lo que esta adición no afecta su resultado. La excepción
`ValueError` para `porcentaje` fuera de `[0, 100]` se mantiene intacta.

---

## Estado del Defecto

| Campo         | Valor                        |
|---------------|------------------------------|
| Estado actual | **Cerrado**                  |
| Asignado a    | Sebastian (autor del lab)    |
| Commit SHA    | `d2d6274fb9e800417983dd9e10120cb17563f747` |
| Fecha cierre  | 2026-06-16                   |
