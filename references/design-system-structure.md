# The Claude Design system package structure

This is **ground truth**, read directly off a real published design system via `DesignSync.list_files` — not guessed. Emit this shape and the sync lands a fully-formed, browsable design system.

## Top-level layout

```
SKILL.md                     # the design system's OWN skill (user-invocable) — see below
readme.md                    # orientation doc for whoever opens the system
styles.css                   # single entry point that @imports every token file
thumbnail.html               # the card shown in the Design systems list

tokens/
  base.css                   # resets + the :root that pulls it together
  colors.css                 # palette + semantic aliases + tints + alpha ramps
  typography.css             # type roles (display/body/eyebrow/caption)
  fonts.css                  # @font-face or Google Fonts import
  spacing.css                # scale + layout rhythm
  radius.css                 # corner radii
  elevation.css              # shadows
  motion.css                 # durations, easings, press-scale
  texture.css                # background textures as CSS custom props

guidelines/                  # *.card.html — one card per concept, THE visible surface
  colors-pigments.card.html
  colors-grounds.card.html
  colors-semantic-text.card.html
  colors-semantic-surface.card.html
  colors-tints.card.html
  colors-medium.card.html
  type-display.card.html
  type-body.card.html
  type-eyebrow.card.html
  type-pairing.card.html
  spacing-scale.card.html
  spacing-layout.card.html
  radius.card.html
  elevation.card.html
  motion.card.html
  states.card.html
  brand-logo.card.html
  brand-photography.card.html
  brand-artwork.card.html
  brand-textures.card.html
  brand-splashes.card.html
  brand-icons.card.html
  brand-sello.card.html

components/
  core/        Button, Card, Badge, Tag, Divider, IconButton  + core.card.html + surfaces.card.html
  forms/       Input, Select, Checkbox, Radio, Switch, <BrandUploader>  + forms.card.html
  navigation/  Navbar, Footer, <BrandTabs>  + navigation.card.html
  feedback/    Dialog, Toast, Tooltip  + feedback.card.html
  brand/       the brand-specific ones  + brand.card.html

assets/                      # organized, referenced by components & cards
  logo/ heroes/ banner/ action/ detail/ lifestyle/ motion/ textures/ icons/ extras/ favicon/

templates/<name>/            # full-page compositions
  <Name>.dc.html

ui_kits/<name>/              # multi-page React reference implementation
  Home.jsx, ... , shared.jsx, index.html, README.md
```

Files the platform generates for you — **do not hand-author**: `_ds_manifest.json`, `_ds_bundle.js`, `_adherence.oxlintrc.json`, `_thumbnail.state.json`, `.thumbnail`.

## The `@dsCard` marker — how cards get into the pane

The Design System pane builds its card index from **the first line** of each preview HTML. Miss this and your card is invisible.

```html
<!-- @dsCard group="Colors" viewport="700x150" name="Los seis pigmentos" subtitle="The entire palette. Nothing outside these six." -->
```

- `group` — the section label in the pane. Reuse a small vocabulary: `Colors`, `Type`, `Spacing`, `Elevation`, `Motion`, `Brand`, `Components`, `Forms`, `Navigation`, `Feedback`.
- `viewport` — `WIDTHxHEIGHT` in px. Sets the card's render box. Size it to the content: swatch rows ~`700x150`, component galleries ~`700x400`, type specimens ~`700x300`.
- `name` — short human label.
- `subtitle` — one line stating the rule, not a description. "The entire palette. Nothing outside these six." beats "A display of colors."

`register_assets` on the DesignSync tool is **legacy** — you don't need it when your files carry `@dsCard`.

### Card body conventions

Each card is a complete standalone HTML document that links the shared stylesheet with a relative path:

```html
<!-- @dsCard group="Colors" viewport="700x150" name="…" subtitle="…" -->
<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../styles.css">
<style>body{margin:0;padding:18px 20px;background:var(--lienzo);font-family:var(--font-body)}
/* card-local layout only */</style>
</head><body>
  <!-- render the concept using ONLY token vars, never raw hexes in layout -->
</body></html>
```

Rules that make cards read as a system:
- Reference tokens (`var(--cadmio)`), not literals — except in a swatch chip where showing the literal IS the point.
- Show the **token name** next to every value. A swatch without `--cadmio` under it is decoration; with it, it's documentation.
- Keep padding consistent across cards (`18px 20px` works well).
- One concept per card. Six pigments = one card. Semantic text colors = a different card.

## The component triple

Every component ships as **three files**, always:

```
components/core/Button.jsx        # the implementation
components/core/Button.d.ts       # the prop contract
components/core/Button.prompt.md  # how a model should USE it
```

The `.prompt.md` is the highest-leverage file in the whole package — it is what makes a model build on-brand later. Format observed in production:

```markdown
One-sentence: the pill CTA — use `primary` for the single Cadmio Vivo action on a
view, `secondary` for the outlined companion, `quiet` for inline Cobalto
links-as-buttons, `ink` on cream sections that need weight without orange.

```jsx
<Button variant="primary" size="lg" href="#empezar">Empezar mi retrato</Button>
<Button variant="secondary">Ver los 5 estilos</Button>
```

- Never place two `primary` buttons in the same viewport — the brand rule is "un solo Cadmio grande por vista".
- Press state shrinks (`--press-scale`); hover deepens the fill. No bounce.
- On `[data-ground="ink"]` sections `secondary` flips to cream automatically.
```

Structure: **one-sentence purpose with variant guidance → a real JSX usage block → 2-4 bullets that are RULES, not features.** Every bullet should be something a model could get wrong. Write the brand's prohibitions in here — this is where "un solo Cadmio por vista" actually gets enforced.

Then one `<folder>.card.html` per component folder renders the whole family as a gallery card.

## The design system's own SKILL.md

The package carries a skill so the system is invocable later. Real example:

```markdown
---
name: <brand>-design
description: Use this skill to generate well-branded interfaces and assets for <Brand>, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.
If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets
out and create static HTML files for the user to view. If working on production code,
you can copy assets and read the rules here to become an expert in designing with this
brand. If the user invokes this skill without any other guidance, ask them what they
want to build or design, ask some questions, and act as an expert designer who outputs
HTML artifacts _or_ production code, depending on the need.
```

## Token conventions worth copying

From a real system, the naming that worked:

- **Raw palette**: one var per brand color, named in the brand's own language — `--lienzo`, `--tinta`, `--cadmio`, `--cobalto`, `--ocre`, `--ftalo`. Brand-native names beat `--color-primary-500`; they make the `.prompt.md` files readable and keep the team speaking one language.
- **Alpha ramps**: `--tinta-a12`, `--tinta-a24` for borders and scrims derived from ink.
- **Semantic aliases** layered on top: `--text-strong`, `--text-muted`, `--surface-card`.
- **Type roles as composite shorthands**: `--text-caption-role: 600 12px/1.3 var(--font-body)` so a card can do `font: var(--text-caption-role)`.
- **Ground switching**: `[data-ground="ink"]` on a section flips semantic vars so components invert automatically instead of needing dark variants.
- **Motion**: `--press-scale`, plus named durations/easings.

That `[data-ground]` pattern is the single best structural idea in the observed system — it means a Button doesn't need a `dark` prop, it just reads the ground it's standing on.
