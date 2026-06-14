# Doble Fondo

**Plataforma de periodismo de datos judicial.**  
Dos casos activos en la Audiencia Nacional documentados con grafos de relaciones interactivos, cronologías y flujos económicos.

---

## Casos cubiertos

| # | Caso | Juzgado | Juez |
|---|------|---------|------|
| 01 | Red de influencias Zapatero | JCI Nº4 | Calama Teixeira |
| 02 | Operación Fidelidad — Leire Díez | JCI Nº6 | Santiago Pedraz |

## Qué incluye cada caso

- **Grafo interactivo** — red de personas, sociedades y conexiones documentadas en el auto judicial
- **Cronología** — hechos probados ordenados con indicadores de hito
- **Flujos económicos** — diagrama Sankey origen → intermediarios → beneficiario
- **Marco legal** — delitos imputados con texto del artículo correspondiente
- **Changelog público** — registro de cada actualización con fuente y fecha

## Stack técnico

HTML estático · D3.js v7.8.5 · Sin framework · Sin backend · Sin tracking

## Ejecutar en local

```bash
# Clonar
git clone https://github.com/Ivanchux/doble-fondo.git
cd doble-fondo

# Abrir directamente (sin servidor)
# Nota: el módulo de noticias RSS requiere HTTPS para funcionar (CORS)
open index.html
```

O con servidor local para RSS:

```bash
npx serve .
# → http://localhost:3000
```

## Sistema de fuentes

| Indicador | Nivel |
|-----------|-------|
| 🟡 Amarillo | Periodística — información de medios, no verificada con documento oficial |
| 🔵 Azul | Oficial — dato proveniente de auto judicial, informe UDEF/UCO o acta de registro |
| 🟢 Verde | Verificado + PDF — documento oficial con copia adjunta |

## Aviso legal

Todos los investigados mencionados son inocentes hasta sentencia firme.  
Los autos describen indicios racionales en fase de instrucción, no hechos probados.

---

*Periodismo de datos judicial · España · 2026*
