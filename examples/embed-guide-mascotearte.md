# Mascotearte — Embed Guide

Snippets HTML/CSS listos para pegar. Asume que copias la carpeta `mascotearte-assets/` en `public/assets/mascotearte/` (o donde vayan tus estáticos) y que ya tienes la paleta como CSS variables:

```css
:root {
  --lienzo:   #F4EBDD;
  --tinta:    #141215;
  --cadmio:   #F26A1F;
  --cobalto:  #1E4FCC;
  --ocre:     #C48A3B;
  --ftalo:    #2A6E5A;
}
body { background: var(--lienzo); color: var(--tinta); }
```

---

## 1. Hero con motion loop (autoplay muted)

El video es el fondo, el poster es fallback para dispositivos que bloqueen autoplay.

```html
<section class="hero">
  <video
    class="hero__video"
    autoplay muted loop playsinline
    poster="/assets/mascotearte/motion/hero_poster.jpg">
    <source src="/assets/mascotearte/motion/hero_loop.mp4" type="video/mp4">
  </video>
  <div class="hero__overlay"></div>
  <div class="hero__content">
    <h1>Tu mascota, pintada a mano.</h1>
    <p>Cinco estilos. Impresión en lienzo con marco. A domicilio.</p>
    <a href="#empezar" class="btn btn--primary">Empezar mi retrato</a>
  </div>
</section>
```

```css
.hero { position: relative; height: 100vh; overflow: hidden; background: var(--tinta); }
.hero__video {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}
.hero__overlay {
  position: absolute; inset: 0;
  background: linear-gradient(90deg,
    rgba(20,18,21,0.55) 0%,
    rgba(20,18,21,0.25) 50%,
    rgba(20,18,21,0) 100%);
}
.hero__content {
  position: relative;
  max-width: 640px;
  padding: 8vh 6vw;
  color: var(--lienzo);
}
.hero__content h1 { font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; margin: 0 0 1rem; }
.btn--primary { background: var(--cadmio); color: var(--tinta); padding: 0.9rem 1.6rem; border-radius: 999px; font-weight: 600; }
```

---

## 2. Nav con logo

```html
<nav class="nav">
  <a class="nav__brand" href="/">
    <img src="/assets/mascotearte/logo/logo_A_firma_cream.png"
         alt="Mascotearte" height="42">
  </a>
  <ul class="nav__links">
    <li><a href="#estilos">Estilos</a></li>
    <li><a href="#proceso">Proceso</a></li>
    <li><a href="#empezar" class="btn btn--primary">Empezar</a></li>
  </ul>
</nav>
```

```css
.nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; }
.nav__brand img { display: block; }
```

**Favicon:** Usa `logo_A_firma_cream.png` reducido a 32×32 y 180×180 (para iOS).

---

## 3. Grid de estilos (los 5 heroes)

```html
<section id="estilos" class="styles">
  <h2>Cinco estilos, uno para cada mascota.</h2>
  <div class="styles__grid">
    <article class="style-card">
      <img src="/assets/mascotearte/heroes/colores_1x1.png" alt="Retrato en lápices de colores">
      <h3>Lápices de colores</h3>
    </article>
    <article class="style-card">
      <img src="/assets/mascotearte/heroes/acuarela_1x1.png" alt="Retrato en acuarela">
      <h3>Acuarela</h3>
    </article>
    <article class="style-card">
      <img src="/assets/mascotearte/heroes/oleo_1x1.png" alt="Retrato en óleo">
      <h3>Óleo</h3>
    </article>
    <article class="style-card">
      <img src="/assets/mascotearte/heroes/pastel_1x1.png" alt="Retrato en pastel">
      <h3>Pastel</h3>
    </article>
    <article class="style-card">
      <img src="/assets/mascotearte/heroes/charcoal_1x1.png" alt="Retrato en carboncillo">
      <h3>Charcoal & grafito</h3>
    </article>
  </div>
</section>
```

```css
.styles { padding: 6rem 2rem; background: var(--lienzo); }
.styles__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}
.style-card { text-align: center; }
.style-card img { width: 100%; aspect-ratio: 1/1; object-fit: cover; border-radius: 8px; }
.style-card h3 { margin-top: 1rem; font-size: 1.1rem; }
```

---

## 4. Banner secundario (sección "cómo se ve")

```html
<section class="banner" style="background-image: url('/assets/mascotearte/banner/banner_hero_4k.png');">
  <div class="banner__content">
    <h2>Cada retrato, impreso en lienzo con marco.</h2>
    <p>Listo para colgar. Envío a domicilio en 7-10 días.</p>
  </div>
</section>
```

```css
.banner {
  min-height: 60vh;
  background-size: cover;
  background-position: center;
  display: flex; align-items: center;
  padding: 4rem 8vw;
}
.banner__content { max-width: 480px; margin-left: 50%; color: var(--tinta); }
```

---

## 5. Sección proceso (los 3 action macros)

```html
<section id="proceso" class="process">
  <h2>El proceso, sin atajos.</h2>
  <div class="process__grid">
    <figure class="process__step">
      <img src="/assets/mascotearte/action/action_pencil_hair_4k.png" alt="">
      <figcaption><strong>1. Trazo.</strong> El primer pigmento toca el papel.</figcaption>
    </figure>
    <figure class="process__step">
      <img src="/assets/mascotearte/action/action_watercolor_bleed_4k.png" alt="">
      <figcaption><strong>2. Color.</strong> Pigmento sobre pigmento, vivo.</figcaption>
    </figure>
    <figure class="process__step">
      <img src="/assets/mascotearte/action/action_oil_brush_4k.png" alt="">
      <figcaption><strong>3. Materia.</strong> Óleo cargado sobre lienzo.</figcaption>
    </figure>
  </div>
</section>
```

```css
.process { padding: 6rem 2rem; background: var(--tinta); color: var(--lienzo); }
.process__grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
.process__step img { width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 4px; }
@media (max-width: 720px) { .process__grid { grid-template-columns: 1fr; } }
```

---

## 6. Uploader (frame mockup vacío + drop zone)

```html
<section class="uploader">
  <h2>Sube la foto de tu mascota.</h2>
  <label class="uploader__frame">
    <img class="uploader__frame-bg" src="/assets/mascotearte/extras/frame_mockup_empty.png" alt="">
    <input type="file" accept="image/*" hidden>
    <span class="uploader__prompt">Arrastra o haz clic</span>
    <!-- Cuando el usuario sube, insertar aquí la foto con position absolute cubriendo el canvas interno del mockup -->
  </label>
</section>
```

```css
.uploader__frame {
  position: relative;
  display: inline-block;
  cursor: pointer;
  max-width: 520px;
}
.uploader__frame-bg { width: 100%; display: block; }
.uploader__prompt {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  color: var(--tinta);
  background: rgba(244,235,221,0.9);
  padding: 0.6rem 1rem;
  border-radius: 999px;
}
```

---

## 7. Sello de garantía + swatches como divider

```html
<!-- badge de garantía (checkout, footer) -->
<img src="/assets/mascotearte/extras/sello_hecho_a_mano.png"
     alt="Hecho a mano · Mascotearte"
     class="badge" width="120">

<!-- divider entre secciones -->
<div class="divider">
  <img src="/assets/mascotearte/extras/swatches_palette.png" alt="">
</div>
```

```css
.badge { display: block; margin: 2rem auto; }
.divider { padding: 3rem 0; }
.divider img { max-width: 360px; margin: 0 auto; display: block; opacity: 0.9; }
```

---

## 8. Texturas de fondo (sección)

```css
.section--linen { background: url('/assets/mascotearte/extras/texture_linen.png') var(--lienzo); background-size: 600px; }
.section--cotton { background: url('/assets/mascotearte/extras/texture_watercolor_paper.png') var(--lienzo); background-size: 600px; }
.section--warm { background: url('/assets/mascotearte/extras/texture_warmpaper.png') var(--lienzo); background-size: 600px; }
```

Aplícalas al `<section>` que quieras darle "tacto" (about, testimonios, faq).

---

## 9. Grain overlay sobre el hero

Para darle textura orgánica sin sacrificar legibilidad del texto:

```css
.hero::after {
  content: "";
  position: absolute; inset: 0;
  background: url('/assets/mascotearte/extras/grain_overlay.png');
  background-size: 400px;
  mix-blend-mode: overlay;
  opacity: 0.35;
  pointer-events: none;
}
```

---

## 10. Splashes como transiciones entre secciones

Cada splash tiene el color del estilo. Úsalos como *stamps* sobre las cards de cada medio:

```html
<article class="style-card style-card--acuarela">
  <img class="style-card__work" src="/assets/mascotearte/heroes/acuarela_1x1.png" alt="">
  <img class="style-card__splash" src="/assets/mascotearte/extras/splash_acuarela.png" alt="">
  <h3>Acuarela</h3>
</article>
```

```css
.style-card { position: relative; }
.style-card__splash {
  position: absolute;
  top: -20px; right: -20px;
  width: 90px; height: 90px;
  transform: rotate(15deg);
  pointer-events: none;
  mix-blend-mode: multiply; /* si el fondo es cream */
}
```

---

## Tipografía sugerida (Google Fonts, gratis)

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Fraunces', serif;   /* titulares — carácter, contrast alto */
  --font-body:    'Inter', sans-serif;  /* UI y párrafos */
}
h1, h2, h3 { font-family: var(--font-display); font-weight: 700; }
body { font-family: var(--font-body); }
```
