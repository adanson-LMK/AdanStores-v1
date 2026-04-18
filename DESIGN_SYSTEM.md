# AdanStore — Design System & Standards

Este documento define las bases visuales de la tienda para mantener la consistencia estética "The Precision Archive".

## 1. Paleta de Colores (Monochrome Dark)
Se utiliza una escala de grises profundos para resaltar los productos.

| Token | Valor | Uso |
| :--- | :--- | :--- |
| `--k` | `#0a0a0a` | Fondo principal (Pure Black) |
| `--k2` | `#141414` | Fondos de Cards y Secciones |
| `--k3` | `#1c1c1c` | Hovers y elementos secundarios |
| `--k4` | `#242424` | Inputs y bordes suaves |
| `--w` | `#f9f9f9` | Texto principal / High contrast |
| `--w2` | `#e8e8e8` | Texto secundario / Botones |
| `--dim` | `#444444` | Texto desactivado / Placeholders |
| `--line`| `#1e1e1e` | Líneas de división y bordes |

## 2. Tipografía
La jerarquía visual se basa en tres familias de fuentes:

- **Display (Titulares):** `Syne`. Para H1, H2 y nombres de categorías. Transmite fuerza y precisión.
- **Sans (Cuerpo):** `Instrument Sans`. Para descripciones, menús y lectura general.
- **Mono (Datos):** `JetBrains Mono`. Para precios, insignias (badges), botones pequeños y metadatos. Da un toque técnico/archivo.

## 3. Componentes Estándar
- **Bordes:** `--r: 4px` (Esquinas ligeramente suavizadas, no redondeadas).
- **Transiciones:** `0.2s ease` para hovers estándar. `0.65s` para revelado de secciones.
- **Scroll:** 3px de ancho, color `--dim`.

## 4. Reglas de Diseño
1. **Grayscale First:** Todo debe ser escala de grises. El color solo se permite en fotos de productos o badges de éxito (ej: `#4ade80` para "En Stock").
2. **Precision Borders:** Evitar sombras pesadas (box-shadow). Usar bordes de `1px solid var(--line)` para separar elementos.
3. **White Space:** Mantener padding amplio en secciones (`64px 32px`) para dar aire de exclusividad.
