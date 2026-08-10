# Prompt patterns that worked

These are the base templates. Fill in `[BRACKETS]` for the specific brand and always append the palette guardrail at the end.

## The palette guardrail (append to every nano-banana-pro prompt)

```
Palette strictly confined to [BRAND] colors: #XXXXXX ([name]), #XXXXXX ([name]),
#XXXXXX ([name]), #XXXXXX ([name]), #XXXXXX ([name]), #XXXXXX ([name]). No other
colors. No pastel baby-pink, no baby-blue, no kraft brown, no unicorn gradients,
no colors outside this palette. No visible text of any kind (unless explicitly
requested), no watermarks, no signatures.
```

## Logo (gpt-image-2-text-to-image, 1:1)

Do NOT ask for transparent background — gpt-image-2 fills it with a gradient. Ask for a **flat cream ground** in the brand's palette and cut it out locally afterwards.

```
A minimalist FLAT vector logo wordmark reading exactly '[BRAND NAME]' as a single
word, in a confident, expressive handwritten cursive script — like a painter's
signature at the corner of a canvas. Deep warm ink black color (hex [TINTA]).
One small FLAT SOLID matte round dot of [ACCENT COLOR NAME] ([HEX]) placed right
after the final letter as a wet paint accent — the dot must be a completely flat
solid color circle, NO 3D shading, NO gradient, NO highlight, NO drop shadow,
NO reflection, NO glow.

Background: solid flat [BASE COLOR NAME] color [HEX] covering the entire canvas
edge-to-edge — NO gradient, NO vignette, NO grey, NO texture. Absolutely flat 2D
vector illustration only: clean solid strokes with slight organic weight variation,
no shadows anywhere, no gradients anywhere, no photographic texture, no additional
decorative flourishes, no other words or subtitles. Centered composition with
balanced negative space around the word. Print-ready, sharp edges.

Spelling must be exactly: [B-R-A-N-D N-A-M-E letter by letter].
```

## Hero product portrait (nano-banana-pro, 2K)

Include the reference image URL in `image_input`. Generate BOTH 1:1 and 16:9 variants. Composition changes based on aspect.

```
A museum-quality artistic portrait of the specific [SUBJECT] shown in the reference
photo — [BRIEF SUBJECT DESCRIPTION]. Preserve the exact [distinctive features] of
the reference. {composition_block} Background: warm [BASE COLOR NAME] (#XXXXXX)
raw canvas / paper tone with subtle organic texture — no other objects, no props,
no [any legible items with text], no signatures, no watermarks, no border, no
frame. Studio-lit as if for a gallery print, soft directional light from
upper-left. {style_block}
```

Composition blocks:
- `1:1`: `Composition: centered three-quarter portrait, [subject] positioned to fill the frame with balanced negative space above.`
- `16:9`: `Composition: [subject] positioned to the LEFT third of the frame, with generous clean negative space filling the RIGHT two thirds — for eventual title text placement (do NOT add any text). FULL BODY, all anatomy visible, no cropped legs or edges.`

## Banner hero still (nano-banana-pro, 4K, 16:9)

The banner is the SITE hero. It shows the product in its natural setting (framed on a wall, on a shelf, in-hand). Use one of the already-generated heroes as `image_input` so the frame contains a real brand piece.

```
A cinematic warm-home hero photograph: a beautifully framed [ASPECT] canvas
[PRODUCT] (matching the reference [style]) hanging on a warm [BASE COLOR] plaster
wall — the [PRODUCT] is inside an elegant thin [ACCENT COLOR] wooden frame,
museum-quality, catching soft golden hour light from the LEFT. Positioned to the
LEFT third of the frame. The RIGHT two thirds are clean empty warm wall with a
subtle grain of natural plaster texture — deliberate breathing space for a
website title overlay. Below the frame, softly out of focus, [small in-brand
prop hint]. Overall mood: [tone words]. Photographic style: full-frame camera,
35mm lens, natural light, shallow depth of field on the background, [product]
perfectly sharp. NO people in the shot.
```

## Action macros (nano-banana-pro, 4K, 16:9)

3 shots of the physical process. Extreme macro, product-only, no hands.

```
Extreme macro photograph, 100mm macro lens shot: [physical action - brush loaded
with paint touching canvas / dough being kneaded / espresso pulling / etc.].
Extreme detail on [the material]. Warm [BASE COLOR] background, soft directional
studio light from upper-left. Shallow depth of field with [main subject] in
razor-sharp focus. Mood: physical, sensuous, alive. NO hands visible, only [the
minimum tools + material].
```

## Detail flat-lay (nano-banana-pro, 2K, 1:1)

Overhead editorial flat-lay showing the brand's toolkit or raw materials.

```
Overhead flat-lay top-down photograph on a warm [BASE COLOR] linen background:
a curated [brand] toolkit — arranged with editorial precision. Include:
[itemize 5-7 objects, each in-palette]. Warm directional light from upper-left
casting soft shadows. Photographed with a 50mm lens, everything tack sharp,
editorial composition with generous breathing space. NO people, NO text on any
object.
```

## Lifestyle with hands (nano-banana-pro, 2K, 16:9)

Human hands in scene. NO faces. NO legible text.

```
Warm cinematic photograph of a pair of human hands (soft warm skin tone, no
jewelry, no visible text on clothing) [action - hanging the frame / opening the
box / holding the product]. Golden hour sunlight streams in from a window
off-camera to the LEFT, casting long soft shadows. Composition: hands and
[product] slightly left of center, [background] breathing to the right. Shot
with a 50mm lens, shallow depth of field on the hands, the [product] tack-sharp.
Warm alegre premium mood. NO faces visible in the frame, NO text on any surface.
```

## Extras

### Splash overlay (nano-banana-pro, 2K, 1:1)

One per style/medium/flavor. On flat cream ground for later cutout.

```
An isolated [description: e.g. thick impasto oil paint stroke, single loose
watercolor splash, powdery pastel smudge, ...] in [PIGMENT NAME] ([HEX]).
Centered on a flat solid [BASE COLOR] ([HEX]) background covering the entire
canvas edge-to-edge — no gradient, no shadow beyond the natural pigment. The
mark should occupy roughly the central 60% of the frame with clean breathing
space around it. Extreme macro detail on the pigment. NO other elements, NO
text, NO extra marks, ONE mark only. Museum-quality material study photograph.
```

### Texture background (nano-banana-pro, 2K, 16:9)

**CRITICAL: reformulate as "seamless abstract pattern"**, not "photograph of fabric". Fabric prompts trigger Google's content filter.

```
A high-resolution abstract organic [SEAMLESS PATTERN DESCRIPTION - e.g.
ORTHOGONAL WOVEN LINE PATTERN, DIMPLED GRAIN PATTERN, WARM PAPER FIBER PATTERN]
filling the entire frame edge-to-edge — [details describing the tone and
composition of the pattern, in-palette colors]. For website background texture.
Uniformly lit, no vignette, no shadows, no folds, no gradients, no borders,
no seams. Absolutely flat pattern across the whole image.
```

### Circular seal / brand stamp (nano-banana-pro, 2K, 1:1)

```
A perfectly circular hand-carved-look ink stamp mark in [TINTA] ([HEX]) on a
flat [BASE COLOR] ([HEX]) background, occupying the central 70% of a square
canvas. INSIDE THE CIRCLE, arranged as a proper atelier seal: at the TOP curving
along the inside of the ring, the words '[LINE 1]' in clean simple sans-serif
capital letters; at the BOTTOM curving along the inside of the ring, the word
'[BRAND]' in matching capitals; in the exact center, [a tiny simple silhouette
of the brand mascot / symbol], rendered as a solid black shape. Two thin
decorative concentric ring lines form the border. Slight organic imperfection
like a real rubber stamp on paper (tiny ink bleeds, faint spots). NO OTHER text
of any kind. Spelling must be exact: [LINE 1] and [BRAND].
```

### Empty frame mockup — the uploader base (nano-banana-pro, 2K, 1:1)

```
A cinematic photograph of a beautiful empty [ASPECT] framed canvas hanging on a
warm [BASE COLOR] plaster wall — the canvas inside is a clean flat primed white
surface (subtle woven linen texture, ready to receive a portrait), and the frame
is an elegant thin [ACCENT COLOR] wooden molding, museum-quality. Perfectly
centered on the wall, straight on camera angle, soft directional light from
upper-left casting a gentle rectangular shadow behind the frame. Shot with 50mm
lens, tack sharp focus on the canvas. NO artwork inside the canvas — it must be
BLANK. NO text, NO people. This is for a website product uploader — users will
'drop' their photo into the canvas area.
```

### Palette swatches (nano-banana-pro, 2K, 16:9)

```
An artistic overhead photograph of [N] distinct thick oil-paint blobs arranged
in a horizontal row across a flat [BASE COLOR] background, each blob roughly
the same size, with clean breathing space between them. From LEFT to RIGHT the
colors must be exactly: 1) [name] ([hex]), 2) [name] ([hex]), … Each blob is
glossy, thick, with tiny impasto ridges and a beautiful natural shape — like a
painter squeezed each color straight onto a palette. Shot top-down, tack sharp
macro focus, warm side light. NO text, NO labels, NO other elements.
```

### Icon set (nano-banana-pro, 2K, 16:9)

```
A perfectly aligned horizontal row of [N] minimalist flat vector LINE ICONS on
a flat [BASE COLOR] background, each rendered in [TINTA] with clean solid
strokes of even weight, each inscribed in an invisible square of the same size
with even spacing between icons. From LEFT to RIGHT the icons represent:
1) [icon 1 description]; 2) [icon 2]; 3) [icon 3]; … Clean minimal line icons
with subtle fill only on [detail], no shadow, no gradient, no photographic
texture, no 3D. NO text or labels.
```

### Grain overlay (nano-banana-pro, 2K, 16:9)

```
A high-resolution SUBTLE ORGANIC PAPER-GRAIN NOISE TEXTURE filling the entire
frame edge-to-edge — a medium-density scatter of tiny darker and lighter specks
with faint fiber traces, at low overall contrast, on a neutral mid-gray
background (RGB ~128,128,128). Absolutely uniform coverage, no vignette, no
gradient, no blotches, no large shapes, no lines, no drawing marks — just fine
grain. Intended as a screen/multiply overlay on a website hero, so must be
subtle and non-directional. NO text, NO objects.
```

## Motion loop (bytedance/seedance-2, 1080p, 5s, no audio)

Use the best `action/*` still as `first_frame_url`. Upload it first.

```
Ultra slow-motion cinematic macro. [Continue the physical action from the
still — e.g. "the loaded sable brush moves ever so slowly to the LEFT across
the primed canvas, laying down a thick buttery ridge of glossy [COLOR] paint.
Tiny pigment crests form and slowly settle behind the bristles."]. The [main
subject] stays razor-sharp; background stays softly out of focus. Warm side
light from upper-left. Very gentle, deliberate movement — a satisfying physical
loop. No people, no hands, no text.
```

Cost warning: Seedance 5s 1080p ≈ **510 credits**. Quote high.
