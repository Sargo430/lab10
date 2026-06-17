# Lab10 — Gestión de Defectos, Corrección y Elaboración de Informes de Prueba

**Asignatura:** Especialidad I: Calidad de Software  
**Carrera:** Ingeniería Civil Informática — Universidad Autónoma de Chile  

## Estructura del repositorio

```
lab10-defectos/
├── src/
│   └── carrito.py          # SUT corregido (v1.0.1)
├── tests/
│   ├── test_carrito.py          # Suite base (9 tests)
│   └── test_carrito_defecto.py  # Tests de verificación del defecto (8 tests)
├── docs/
│   ├── REPORTE_DEFECTO.md  # Reporte + RCA (Tareas 1 y 3a)
│   └── INFORME_PRUEBAS.md  # Extracto IEEE 829 (Tarea 4)
└── README.md
```

## Defecto corregido

**LAB10-001:** `aplicar_descuento()` no validaba que el parámetro `total` fuera ≥ 0,
permitiendo retornar valores negativos sin lanzar excepción.

**Corrección:** se agregó validación `if total < 0: raise ValueError(...)` y retorno
`max(0.0, ...)` como salvaguarda defensiva.

## Ejecutar los tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src --cov-report=term-missing
```

Resultado esperado: **17 passed**, cobertura **100 %**.
