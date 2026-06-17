# Informe de Resumen de Pruebas — Extracto IEEE 829

## 1. Identificador del informe

| Campo              | Valor                                                            |
|--------------------|------------------------------------------------------------------|
| Código             | IRP-LAB10-001                                                    |
| Versión del SUT    | 1.0.1 (post-corrección defecto LAB10-001)                        |
| Módulo evaluado    | `src/carrito.py`                                                 |
| Alcance            | Ciclo completo de corrección del defecto LAB10-001               |
| Responsable QA     | Sebastian — Ingeniería Civil Informática, U. Autónoma de Chile   |
| Fecha de emisión   | 16 de junio de 2025                                              |

---

## 2. Resumen de variaciones del plan

| Ítem                            | Planificado                               | Ejecutado                                | Diferencia |
|---------------------------------|-------------------------------------------|------------------------------------------|------------|
| Tests unitarios base            | 9 (suite provista en guía)                | 9                                        | Ninguna    |
| Tests de verificación (defecto) | 4 casos parametrizados (guía, Tarea 2)    | 8 (4 de resultado ≥ 0 + 4 de ValueError) | Se amplió la cobertura para incluir la verificación de `ValueError` en totales negativos |
| Pruebas BDD (Behave)            | No contempladas en esta guía              | No ejecutadas                            | Fuera de alcance para este laboratorio |
| Análisis estático               | No especificado                           | No ejecutado                             | Fuera de alcance |

> **Justificación de la variación principal:** el test parametrizado original (guía) verificaba
> únicamente que el resultado fuera ≥ 0 con totales positivos. Al implementar la corrección
> (lanzar `ValueError` para `total < 0`), se agregó un segundo grupo parametrizado
> (`test_total_negativo_lanza_error`) para validar explícitamente ese comportamiento. Esto
> incrementó el total de casos de 13 a 17, mejorando la cobertura sin eliminar ningún caso
> planificado.

---

## 3. Resumen de actividades

| Ítem                   | Detalle                                                    |
|------------------------|------------------------------------------------------------|
| Herramientas           | pytest 9.1.0, pytest-cov 7.1.0                             |
| Lenguaje               | Python 3.12.3 (GCC 13.3.0)                                 |
| Sistema operativo      | Linux 6.18.5 (Ubuntu 24.04)                                |
| IDE                    | VS Code con extensión Python                               |
| Control de versiones   | Git (commit de corrección: `fix/lab10-001-total-negativo`) |
| Tiempo total ejecución | ~0,06 s (suite completa, 17 tests)                         |
| Módulos bajo prueba    | `src/carrito.py` (funciones: `agregar_al_carrito`, `calcular_total`, `aplicar_descuento`) |

---

## 4. Resultados — Resumen de casos

### 4.1 Suite base (`test_carrito.py`)

| Tipo de prueba     | Ejecutados | Aprobados | Fallidos | Bloqueados | % Aprobación |
|--------------------|:----------:|:---------:|:--------:|:----------:|:------------:|
| Unitarias (pytest) | 9          | 9         | 0        | 0          | 100 %        |

### 4.2 Suite de verificación del defecto (`test_carrito_defecto.py`)

| Tipo de prueba                    | Ejecutados | Aprobados | Fallidos | Bloqueados | % Aprobación |
|-----------------------------------|:----------:|:---------:|:--------:|:----------:|:------------:|
| Parametrizadas — resultado ≥ 0    | 4          | 4         | 0        | 0          | 100 %        |
| Parametrizadas — ValueError total | 4          | 4         | 0        | 0          | 100 %        |

### 4.3 Totales consolidados (post-corrección)

| Categoría          | Ejecutados | Aprobados | Fallidos | Bloqueados | % Aprobación |
|--------------------|:----------:|:---------:|:--------:|:----------:|:------------:|
| **Total general**  | **17**     | **17**    | **0**    | **0**      | **100 %**    |

### 4.4 Cobertura de código

| Módulo            | Sentencias | Sin cubrir | Cobertura |
|-------------------|:----------:|:----------:|:---------:|
| `src/__init__.py` | 0          | 0          | 100 %     |
| `src/carrito.py`  | 15         | 0          | **100 %** |
| **TOTAL**         | **15**     | **0**      | **100 %** |

---

## 5. Métricas

### DRE (Defect Removal Efficiency)

```
DRE = Defectos hallados antes del release / (Defectos antes + Defectos después) × 100
    = 1 / (1 + 0) × 100
    = 100 %
```

> **Justificación:** se considera 1 defecto hallado antes del release (LAB10-001) y 0
> defectos que habrían escapado al release, dado que el pipeline de CI con el test
> parametrizado `test_total_negativo_lanza_error` habría interceptado el defecto
> automáticamente antes de cualquier despliegue. DRE = 100 % indica proceso de pruebas maduro.

### Densidad de defectos

```
Densidad = N° de defectos / KLOC
         = 1 defecto / 0,050 KLOC   (src/carrito.py tiene 50 líneas)
         = 20 defectos/KLOC
```

> **Nota:** el valor es alto porque el módulo es muy pequeño (50 líneas). La densidad
> absoluta (1 defecto en 50 LOC) es normal para código con un defecto intencional.
> En módulos de mayor tamaño este ratio se reduciría significativamente.

### Porcentaje de casos aprobados

```
% Aprobación = Casos aprobados / Casos ejecutados × 100
             = 17 / 17 × 100
             = 100 %
```

### Tasa de reapertura

```
Tasa reapertura = Defectos reabiertos / Defectos corregidos × 100
               = 0 / 1 × 100
               = 0 %
```

> El defecto LAB10-001 fue cerrado tras la primera corrección sin necesidad de reapertura.
> Una tasa del 0 % indica que el análisis de causa raíz fue correcto y la corrección atacó
> la causa, no solo el síntoma.

---

## 6. Evaluación general

El módulo `src/carrito.py` (v1.0.1) **está listo para integrarse** a la rama principal del
proyecto.

**Justificación basada en métricas:**

- **Cobertura 100 %:** todas las sentencias ejecutables del módulo son ejercidas por la suite,
  lo que minimiza el riesgo de defectos latentes no detectados.
- **% Aprobación 100 % (17/17):** no existe ningún caso fallido ni bloqueado tras la corrección;
  la regresión completa confirma que el fix no introdujo nuevos problemas.
- **DRE 100 %:** el proceso de pruebas capturó el único defecto conocido antes del release.
- **Tasa de reapertura 0 %:** la corrección fue precisa y suficiente en el primer intento,
  validando la calidad del RCA realizado.
- **Densidad 20 def/KLOC:** aunque el valor absoluto parece alto, corresponde a 1 defecto
  intencional en un módulo de 50 líneas; depurado dicho defecto, la densidad es 0.

**Recomendación:** integrar `src/carrito.py` v1.0.1, cerrar el Issue LAB10-001 y documentar
el patrón de validación de precondiciones (`total >= 0`) como estándar para futuros módulos
financieros del sistema de e-commerce.

---

## 7. Aprobaciones

| Rol             | Nombre                       | Fecha       | Firma       |
|-----------------|------------------------------|-------------|-------------|
| Responsable QA  | Sebastian                    | 2025-06-16  | _(firmado)_ |
| Desarrollador   | Sebastian                    | 2025-06-16  | _(firmado)_ |
| Docente         | Camilo Alejandro Fuentes Beals | —         | Pendiente   |
