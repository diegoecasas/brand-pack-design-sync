---
name: brand-pack-design-sync
description: Build a full brand assets pack with kie.ai (logo, hero photography, motion loop, textures) AND compile it into a real Claude Design system package — tokens, guideline cards, and React components — ready to push to claude.ai/design via /design-sync. Use when the user wants a brand kit, identity pack, or design system, or asks to get their brand into Claude Design. Requires KIE_API_KEY.
---

# Brand Pack → Design System

This skill does two jobs in sequence:

1. **Generate the brand pack** with kie.ai — logo, hero photography, action macros, lifestyle, motion loop, textures, extras. (Steps 0-3.5.)
2. **Compile it into a Claude Design system package** — tokens, guideline cards, component library — and get it into claude.ai/design. (Steps 4-6.)

Job 2 is what makes this different from a folder of pretty PNGs. A design system is what a model reads later to build *on brand*; a folder of PNGs is a mood board.

If the user only wants the assets, stop after Step 3.5 and hand them the folder.

Read `KIE_API_KEY` from the environment. Never ask for it in chat, never write it into a file.

---

## Part 1 — The brand pack

### kie.ai API primer

All calls carry `Authorization: Bearer $KIE_API_KEY`. Generations are async: create a task, poll, download when `success` (URLs expire ~24h, files purge at 14 days — download immediately).

- **Create** — `POST https://api.kie.ai/api/v1/jobs/createTask` with `{model, input}`
- **Poll** — `GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...`
  - `data.state`: `waiting / queuing / generating / success / fail`
  - On success, `data.resultJson` is a JSON **string** of `{"resultUrls":[...]}` — parse it
  - `data.creditsConsumed` is the real cost — log it every time
- **Upload** (Seedance needs URLs) — `POST https://kieai.redpandaai.co/api/file-stream-upload`, multipart, returns `data.downloadUrl`
- **Balance** — `GET https://api.kie.ai/api/v1/chat/credit` → balance in `data`
- Poll every 3-8s with backoff; give up at 15 min.

**Cloudflare blocks the upload endpoint without a browser-like User-Agent.** Send `User-Agent: Mozilla/5.0 ...` on `/file-stream-upload` or you get `HTTP 403 error code 1010`.

Model inputs:
- `gpt-image-2-text-to-image` — `prompt`, `aspect_ratio`
- `nano-banana-pro` — `prompt`, `image_input` (URL array, may be empty), `aspect_ratio`, `resolution` (1K/2K/4K), `output_format`
- `bytedance/seedance-2` — `prompt`, `first_frame_url`, `aspect_ratio`, `resolution` (720p/1080p), `duration`, `generate_audio` (false)

### Step 0 — Interview (generate nothing yet)

Ask in one round, then confirm your understanding:

1. What is the product or business? (category, what they sell, for whom)
2. Brand name, or should you propose 3 with personality?
3. Vibe? (2-3 adjectives, or a movie/place/era)
4. How many hero products, and do they have names?
5. Anything to avoid? (colors they hate, category clichés, competitors)
6. Existing web project to integrate into, or pack first?

If they have **reference images** of the product or existing artwork, ask for the folder path. Uploading those as `image_input` is the single biggest lever for pack cohesion.

Do not proceed until they confirm.

### Step 1 — Direction of art

Research the category briefly, for reference energy only, never to copy. Then deliver:

- **The palette** — 5-6 named colors with exact hex, saved to `palette.md`. Every asset lives inside it. Deliberately dodge the category's convergent cliché: look at 3-5 competitors, identify the shared base tone / font / gimmick, and pick against it.
- **Logo direction** — 2-3 concepts, one line each, with a recommendation.
- **The Bespoke Extras Plan** — 5-13 extras specific to *this* brand, each with a one-line purpose. Atmosphere overlays, texture packs, patterns, seals, macros, environment shots. A burger brand wants smoke and char; a candle brand wants light bloom and linen. **The user approves this list before you generate anything.**

### Step 2 — Parameters and cost

- Hero products: 16:9 AND 1:1 each · banner and the rest: 16:9 · logo: 1:1
- 2K for most, 4K for banner and action · motion 1080p, 5s, no audio
- One generation per asset first pass; only regenerate failures

Before creating any job: report the credit balance, report the generation count broken down by model, then **wait for their go**.

Be honest: kie.ai has no pre-generation cost estimate. You can give the count and the balance, not the price. Reference: <https://kie.ai/pricing>.

Observed costs — log the real `creditsConsumed`, but quote from these:

| Model | Cost |
|---|---|
| `nano-banana-pro` 2K | ~18 credits |
| `nano-banana-pro` 4K | ~24 credits |
| `gpt-image-2-text-to-image` | ~6 credits |
| `bytedance/seedance-2` 5s 1080p | **~510 credits** |

That last one is not a typo. One motion loop can cost more than the other 32 generations combined. Quote it loudly and separately.

**Recommend phasing.** Phase 1 = logo + heroes (~11 gens, cheap). If the visual language reads right, continue. Phase 2 = banner, action, detail, lifestyle, extras. Phase 3 = motion, last, from the best action still. Phasing saves the user from spending 200+ credits on a pack that's off-tone.

### Step 2.5 — Use the helper

Copy `scripts/kie.py` into the project's `_scripts/`. It does create → poll → parse → download → return credits, stdlib only, with a batch runner.

Detach background batches or the parent shell can kill them:

```bash
nohup python3 _scripts/kie.py batch --tasks tasks.json --concurrency 3 \
  > _logs/result.json 2> _logs/stderr.log &
disown
```

Then tail `_logs/kie.log` filtered on `"event": "batch_(ok|err)"` to stream progress. Don't poll — let the log push.

Concurrency **3** (the limit is 20 req/10s). Order matters: anything that references another asset waits for it; motion goes last. If one generation fails, keep going and report at the end — never abort the pack for one image.

### Step 3 — Generate

```
logo/ banner/ heroes/ action/ detail/ lifestyle/ motion/ extras/
_refs/ _scripts/ _logs/
```

See `references/prompt-patterns.md` for the templates.

**Model quirks that will bite you:**

- **gpt-image-2 cannot do real transparency.** Asking for it yields a gradient gray fill and a 3D-looking dot. Generate the logo on **flat cream** instead, then cut it out locally in Step 3.5.
- **nano-banana-pro filters "photograph of fabric / cotton paper / kraft paper"** as a Prohibited Use false positive. Reformulate as **"seamless abstract organic pattern"** and it passes.
- **Anatomy gets cropped in 16:9.** Say "FULL BODY, all four paws visible, complete anatomy, NO cropped legs, NO mutilated silhouette" explicitly.
- **"Monochromatic" must be shouted.** "The ENTIRE artwork must be strictly grayscale — ABSOLUTELY NO brown, NO tan, NO amber. Even where the subject would normally be brown, render it MID GRAY."
- **Seedance needs an uploaded `first_frame_url`**, never a local path. Extract the poster with `ffmpeg -i loop.mp4 -vframes 1 poster.jpg` — don't burn credits on a still.

**Repeat the palette hexes in every single prompt.** That's what makes 30 generations feel like one brand.

### Step 3.5 — Local post-processing (free)

Run `scripts/finalize.py`:

- **Transparent cutouts** via **luminance threshold**, not color distance. Generated cream has paper-grain variation that defeats color matching, but ink is luminance ≤175 and cream is ≥205. Threshold on `Y = (299R + 587G + 114B)/1000`, feather between.
- **Dark-mode logo variant** — repaint every non-transparent, non-accent pixel to cream.
- **Favicon set** — 16, 32, 180, and a bundled `.ico`.

---

## Part 2 — The design system

This is the half that makes the pack usable by a model later.

### Step 4 — Scaffold the package

Write a brand spec JSON (see the header of `scripts/scaffold_design_system.py` for the schema — brand, slug, system_name, colors with roles, fonts, tone_words, dos, donts), then:

```bash
python3 scripts/scaffold_design_system.py brand.json --out ~/Desktop/<slug>-design-system
```

That emits, deterministically: `styles.css`, `tokens/*.css` (colors with alpha ramps and semantic aliases, typography roles, spacing, radius, elevation, motion, texture, base), 10 `guidelines/*.card.html`, `SKILL.md`, `readme.md`, `thumbnail.html`, and the folder tree.

Then copy the brand pack assets into `assets/{logo,heroes,banner,action,detail,lifestyle,motion,textures,icons,extras,favicon}/` and point `tokens/texture.css` at the real texture files.

**Read `references/design-system-structure.md` before hand-authoring anything.** It documents the exact structure — verified by reading a real published system, not guessed.

### Step 5 — Author the components

Every component is a **triple**:

```
components/core/Button.jsx        the implementation
components/core/Button.d.ts       the prop contract
components/core/Button.prompt.md  how a model should USE it
```

The `.prompt.md` is the highest-leverage file in the package. Format:

> **One-sentence purpose with variant guidance** → **a real JSX usage block** → **2-4 bullets that are RULES, not features.**

Every bullet should be something a model could plausibly get wrong. Put the brand's prohibitions here — "never two primary buttons in one viewport" belongs in `Button.prompt.md`, not in a doc nobody reads.

Suggested coverage: `core/` (Button, Card, Badge, Tag, Divider, IconButton), `forms/` (Input, Select, Checkbox, Radio, Switch, + the brand's own uploader), `navigation/` (Navbar, Footer, + brand tabs), `feedback/` (Dialog, Toast, Tooltip), `brand/` (the ones only this brand has — a Sello, an ArtworkFrame, a ProcessStep).

Add one `<group>.card.html` per folder rendering the family as a gallery.

**Card rules:** every `*.card.html` needs a first-line `<!-- @dsCard group="…" viewport="WxH" name="…" subtitle="…" -->`. No marker, no card. Reference tokens, never raw hexes (swatch chips excepted). Make the subtitle state a rule, not a description.

**Verify the cards actually render before syncing.** Serve the package and measure — don't assume:

```bash
cd <package> && python3 -m http.server 8899
```

Then load each card in an iframe at its declared viewport and compare `body.scrollHeight` against the declared height. A clipped card looks broken in the pane and you will not notice from the source. The scaffolded cards are pre-measured; anything you hand-author is not.

### Step 6 — Sync to claude.ai/design

Two channels. **Read `references/design-sync-playbook.md` for the full contract.**

**Channel A — the user runs it (official, BEST FIDELITY).** The product is explicit: *"type `/design-sync` yourself at the prompt — asking Claude to run it won't work."* So build the package and hand them:

```bash
cd ~/Desktop/<slug>-design-system
claude
```

…then tell them to type `/design-sync` themselves. Needs a Claude account login (not Bedrock/Vertex/Foundry) and a current Claude Code.

**Channel B — you drive the `DesignSync` tool**, if it's available in your session:

```
list_projects → (create_project if needed) → finalize_plan → write_files
```

- Check `list_projects` first — the user may already have a system for this brand that should be **updated**, not duplicated.
- `finalize_plan` locks the write paths and `localDir`; the user sees them in the permission prompt.
- `write_files` takes **256 files per call** and prefers **`localPath`** — the tool reads from disk so contents never enter your context. That's how 250 MB of assets syncs without touching the context window.
- Sync **incrementally**, diffing against `list_files`. Never wholesale-replace; you'd destroy a teammate's work.
- `register_assets` is legacy — cards come from `@dsCard`.

**Do not automate the browser upload form.** It caps at 10 MB per call, it lands everything in `uploads/` as raw material for Claude Design to *infer* tokens from PNGs (you already know the exact hexes), and DOM selectors break on every UI change. Emitting the structure directly skips a lossy round-trip.

### Step 7 — Deliverables

In the assets folder: `palette.md`, `manifest.md` (every file, model, prompt reference, and the real `creditsConsumed` you logged, with per-phase and grand totals), `embed-guide.md` (HTML/CSS snippets — see `examples/`), `claude-design-brief.md`.

In the design-system package: everything from Step 4-5, plus its own `SKILL.md` with `user-invocable: true`.

A `.gitignore` in both, blocking `.env`, `_logs/`, `.venv/`, `.DS_Store`.

Finish by printing `claude-design-brief.md` in full, and giving the user the two-line `/design-sync` instruction.

---

## Rules

- Same product build and same lighting language across every asset. Consistency is the entire point.
- Every asset inside the Step-1 palette. Repeat the hexes in every prompt.
- No burnt-in text in any photograph. Only `logo/` files carry the brand name.
- Overlays and textures subtle enough to live under foreground text.
- Off-brand or deformed result: regenerate **once** before showing the user.
- Never ask for the API key in chat; never write it to a file.
- Verify rendering by measuring, not by assuming.
- Convert relative dates to absolute in any notes you write.

## What's in this skill

**Scripts** — `kie.py` (async kie.ai helper, stdlib only), `finalize.py` (cutouts, dark-mode logo, favicons; needs Pillow), `scaffold_design_system.py` (emits the whole token + card layer from a brand spec).

**References** — `design-system-structure.md` (the verified package structure, `@dsCard` format, component triple), `design-sync-playbook.md` (both sync channels, the DesignSync method contract, pre-flight checklist), `prompt-patterns.md` (all the generation templates), `example-palette.md` (a worked palette).

**Examples** — a complete `embed-guide` and `claude-design-brief` from a real build. Use them as **templates**; the palette, tone, and system name always come from the user's Step 0 answers, never from the example.
