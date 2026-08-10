# Brief para Claude Design — Mascotearte

## Nombre de la compañía
**Mascotearte**

## Blurb (voz de la marca)
Convertimos la foto de tu mascota en una obra pintada a mano, impresa en lienzo con marco y enviada a tu puerta. Cinco estilos —lápices de colores, acuarela, óleo, pastel y carboncillo— para que elijas cómo quieres verla siempre. Alegre, premium, tuya para toda la vida.

## Nombre del design system
**Estudio Alegre** — pensado como el atelier de un pintor: crema como lienzo crudo, pigmentos saturados de verdad, y la energía de un lugar donde se está haciendo algo con las manos, no una tienda pulida.

## Paleta (6 colores, hex exactos)

| Nombre | Hex | Rol |
|---|---|---|
| Lienzo Crudo | `#F4EBDD` | Fondo base. Casi blanco, cálido. Nunca uses `#FFFFFF` puro. |
| Tinta Nocturna | `#141215` | Texto y contornos. Negro cálido, no negro puro. |
| Cadmio Vivo | `#F26A1F` | Acento principal. CTAs, highlights, la "alegría". |
| Cobalto Estudio | `#1E4FCC` | Acento secundario. Contraste premium, links importantes. |
| Ocre Antiguo | `#C48A3B` | Detalles cálidos. Marcos, iconos, warm accents. |
| Verde Ftalo | `#2A6E5A` | Respiro. Fondos de secciones secundarias, badges. |

## Pareja tipográfica sugerida
- **Display / Titulares:** **Fraunces** (Google Fonts). Serif contemporáneo con alto contraste, personalidad "editorial de galería". Pesos 500-700.
- **UI / Cuerpo:** **Inter** (Google Fonts). Sans-serif neutro, legible en todos los tamaños. Pesos 400-600.
- **Alternativas premium (de pago):** GT Sectra (display) + Söhne (body). Mismo espíritu, más carácter.

## Palabras de tono

Cinco palabras clave que deben leer los usuarios del sitio:

- **Alegre** — no gravedad de museo. Tiene chispa.
- **Físico** — hay pigmento, hay lienzo, hay manos. No es "digital".
- **Premium** — sin gritar el precio. Museo, no e-commerce.
- **Confiable** — un artista real detrás. Se ve el proceso.
- **Cálido** — todo respira warm cream, nunca frío.

## Reglas haz / no hagas

### Haz
- **Muestra el proceso**, no solo el resultado. Los assets de action y detail son parte del argumento de venta, no relleno.
- **Deja respirar.** El vibe premium viene del espacio negativo, no de saturar.
- **Usa Cadmio Vivo con hambre.** Es el color que "vende alegría" — botones, highlights, el punto del logo. Pero un solo Cadmio grande por vista, no dos.
- **Combina Cobalto + Ocre + Ftalo** en zonas secundarias para leer "galería", no "kids brand".
- **Deja el logo firma en su color natural** (Tinta Nocturna sobre Lienzo Crudo). Si va sobre fondo oscuro, invierte a cream.

### No hagas
- **No uses `#FFFFFF` puro.** Siempre Lienzo Crudo. Un blanco puro rompe todo el warmth.
- **No metas colores fuera de la paleta.** Ni rosa bebé, ni celeste bebé, ni kraft/manila, ni gradientes tipo "unicornio".
- **No pongas texto encima de las obras (heroes) sin overlay.** Las obras son la protagonista, el texto va en el 16:9 que ya tiene espacio limpio a la derecha.
- **No uses serif isabelina "renaissance royal".** Es el cliché de la categoría (Crown & Paw, West & Willow) — nos aleja del vibe alegre-moderno que buscamos.

## Assets disponibles

Total: **34 assets** en `~/Desktop/mascotearte-assets/`.

- **logo/** — 1 wordmark firma (versión cream + backup transparente-gris)
- **heroes/** — 5 estilos × 2 aspectos (16:9 + 1:1) del yorkie estelar; **usar `_1x1` en cards, `_16x9` en heroes con titular**
- **banner/** — 1 hero still 4K de canvas enmarcado en pared
- **action/** — 3 macros 4K del proceso (pincel de óleo, watercolor bleed, punta de lápiz)
- **detail/** — 2 tomas de calidad (flatlay de tools + macro esquina canvas con firma)
- **lifestyle/** — 2 con manos (colgando frame + unboxing con caja premium ftalo)
- **motion/** — 1 loop 5s 1080p sin audio + poster still (ideal para el hero de fondo)
- **extras/** — 5 splashes por estilo + 3 texturas de fondo + sello circular + frame mockup vacío (para el uploader) + swatches paleta + iconset 5 medios + grain overlay

Ver [manifest.md](manifest.md) para el detalle archivo por archivo, y [embed-guide.md](embed-guide.md) para snippets HTML/CSS listos.

## Consistencia visual del pack

Todos los assets se generaron con el mismo prompt-template que incluye:
1. Los 6 hex de la paleta explícitamente en cada prompt
2. Reglas de composición (aspect, espacio negativo)
3. Prohibición explícita de texto (excepto en el sello y en la firma del canvas corner)
4. La misma iluminación: luz cálida direccional desde upper-left
5. El mismo yorkie de referencia (`_refs/foto.jpeg`) como `image_input` en todos los heroes

Esto significa que puedes intercalar assets de cualquier categoría en cualquier sección — leerán como una sola marca.

---

**Mascotearte** — hecho con manos y pigmento, para que vivas con la cara de tu mascota siempre a la vista.
