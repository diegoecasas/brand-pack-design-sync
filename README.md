# KIE-brand-pack-design-sync

A [Claude Code](https://docs.claude.com/en/docs/agents-and-tools/claude-code/overview) skill that generates a full brand-assets pack with [kie.ai](https://kie.ai) **and compiles it into a real Claude Design system** — tokens, guideline cards, and a component library — ready to push to [claude.ai/design](https://claude.ai/design).

This is the v2 of [`brand-pack-skill`](https://github.com/diegoecasas/brand-pack-skill). v1 stops at a folder of assets plus a brief you paste in by hand. v2 continues into a design system package and syncs it.

## Why v2 exists

The manual path is: go to claude.ai/design → Create design system → Create here → drag ~35 files in → type a blurb → Continue to generation. Claude Design then *infers* your tokens and components from the PNGs you dropped.

That inference step is a lossy round-trip. You already know the exact hexes, the exact type roles, the exact component rules — writing them into a package and syncing that directly is strictly better:

| | Manual upload | This skill |
|---|---|---|
| Transport cap | 10 MB per batch | Reads from disk, no cap |
| Tokens | Inferred from JPEGs | Exact, authored |
| Components | Generated from scratch | Authored with `.prompt.md` rules |
| Contrast checks | None | Computed, WCAG-labeled |
| Repeatable | No | `scaffold_design_system.py brand.json` |
| Breaks when the UI changes | Yes | No |

## What you get

**A brand pack** (~35 files): logo with transparent + dark-mode variants, hero photography in 16:9 and 1:1, 4K action macros, lifestyle shots, a 5s motion loop with poster, textures, splashes, a seal, an icon set, a favicon set.

**A design system package**:

```
SKILL.md                      the system's own user-invocable skill
styles.css                    single entry point
tokens/                       colors (+ alpha ramps, semantic aliases, ground switching),
                              typography, spacing, radius, elevation, motion, texture, base
guidelines/*.card.html        10 pre-measured documentation cards
components/<group>/           .jsx + .d.ts + .prompt.md per component
assets/                       the brand pack, organized
```

Every card carries the `<!-- @dsCard … -->` marker the Design System pane reads to build its index.

## Install

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/diegoecasas/brand-pack-design-sync.git ~/.claude/skills/brand-pack-design-sync
```

Then ask for a brand pack in any Claude Code session, in any language — matching is semantic:

> "Build me a brand pack for my coffee roastery and get it into Claude Design"
>
> "Hazme un design system para mi marca de velas"

## Requirements

- `KIE_API_KEY` in the environment (`export`, or a project `.env` you `set -a && source`)
- Python 3.10+ — stdlib only for `kie.py` and `scaffold_design_system.py`; Pillow for `finalize.py`
- `ffmpeg` for the motion poster still
- ~$8-15 of kie.ai credits per full pack
- A Claude account login for `/design-sync` (not available on Bedrock, Vertex, or Foundry)

## Standalone usage

The scaffolder is useful on its own, with no kie.ai involved — if you already have a palette and just want a design system skeleton:

```bash
python3 scripts/scaffold_design_system.py brand.json --out ~/Desktop/acme-design-system
```

`brand.json` takes a brand name, slug, colors (each with a `var`, `name`, `hex`, and `role` — exactly one `ground` and one `ink`), a display/body font pair, tone words, and do/don't lists. Full schema in the script's docstring.

It emits 23 files: all tokens, 10 measured guideline cards, `styles.css`, `SKILL.md`, `readme.md`, `thumbnail.html`, and the folder tree. The contrast card computes real WCAG ratios and labels each color AAA / AA / AA-Large / Decorative-only — which usually reveals that your brightest accent can't legally carry body text.

## Getting it into Claude Design

The supported path is a slash command **the user types themselves** — per the product: *"asking Claude to run it won't work."*

```bash
cd ~/Desktop/<slug>-design-system
claude
```

…then type `/design-sync`.

If the `DesignSync` tool is available in the session, the skill can also push directly: `list_projects → finalize_plan → write_files`, incrementally, diffed against what's already there. See `references/design-sync-playbook.md`.

## What's here

```
SKILL.md                                   the skill instructions
scripts/
  kie.py                                   async kie.ai helper (create → poll → download, batch)
  finalize.py                              luminance cutouts, dark-mode logo, favicons
  scaffold_design_system.py                brand spec JSON → full token + card layer
references/
  design-system-structure.md               verified package structure, @dsCard, component triple
  design-sync-playbook.md                  both sync channels, DesignSync contract, pre-flight
  prompt-patterns.md                       generation templates for every asset type
  example-palette.md                       a worked palette + selection heuristic
examples/
  embed-guide-mascotearte.md               10 real HTML/CSS placements
  claude-design-brief-mascotearte.md       a finished brief
```

## Model choices

Locked in, do not substitute: **gpt-image-2-text-to-image** for the logo, **nano-banana-pro** for photography and textures, **bytedance/seedance-2** for motion.

Budget note: the Seedance loop runs ~510 credits — potentially more than every other generation combined. It is quoted separately for a reason.

## License

MIT. See `LICENSE`.
