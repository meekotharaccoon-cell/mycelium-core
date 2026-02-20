# 🌐 Mycelium Core — Master Orchestrator

The central map of the whole organism. Every agent, every repo, every connection.

---

## The Organism — Live Map

```
                    ┌─────────────────────┐
                    │   meeko-brain        │  ← private memory
                    │   (remembers all)    │
                    └──────────┬──────────┘
                               │ syncs to
                    ┌──────────▼──────────┐
                    │  meeko-nerve-center  │  ← central nervous system
                    │  (runs everything)   │  github.com/meekotharaccoon-cell/meeko-nerve-center
                    └─────────┬───────────┘
                              │ spawns + monitors
          ┌───────────────────┼───────────────────┐
          │                   │                   │
┌─────────▼──────┐  ┌────────▼───────┐  ┌────────▼───────┐
│ mycelium-grants│  │ mycelium-money │  │mycelium-knowledge│
│ (finds free $) │  │ (legal revenue)│  │(learns+packages) │
└────────────────┘  └────────────────┘  └────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │ all feed into
                    ┌─────────▼──────────┐
                    │ mycelium-visibility │  ← audience growth
                    │ (spreads the word)  │
                    └─────────┬──────────┘
                              │ drives traffic to
                    ┌─────────▼──────────┐
                    │  gaza-rose-gallery  │  ← the product
                    │  (56 artworks, $1)  │  github.com/meekotharaccoon-cell/gaza-rose-gallery
                    └─────────┬──────────┘
                              │ 70% of sales go to
                    ┌─────────▼──────────┐
                    │       PCRF          │  ← Palestine Children's Relief Fund
                    │  (verified 4-star)  │  pcrf.net | EIN 93-1057665
                    └────────────────────┘
```

---

## All Repos + Status

| Repo | Purpose | Status | Schedule |
|------|---------|--------|----------|
| [meeko-nerve-center](https://github.com/meekotharaccoon-cell/meeko-nerve-center) | Central brain + workflows | 🟢 Live | 9AM + 9PM daily |
| [gaza-rose-gallery](https://github.com/meekotharaccoon-cell/gaza-rose-gallery) | Art gallery + payments | 🟢 Live | Always on (GitHub Pages) |
| [mycelium-grants](https://github.com/meekotharaccoon-cell/mycelium-grants) | Grant finder agent | 🟢 Live | 10:30AM daily |
| [mycelium-money](https://github.com/meekotharaccoon-cell/mycelium-money) | Legal revenue agent | 🟢 Live | 11AM daily |
| [mycelium-knowledge](https://github.com/meekotharaccoon-cell/mycelium-knowledge) | Knowledge packager | 🟢 Live | Growing |
| [mycelium-visibility](https://github.com/meekotharaccoon-cell/mycelium-visibility) | Audience builder | 🟢 Live | 11:30AM daily |
| [mycelium-core](https://github.com/meekotharaccoon-cell/mycelium-core) | This orchestrator | 🟢 Live | Monitors all |
| meeko-brain | Private memory | 🔒 Private | Syncs 2x daily |

---

## Secrets Required (add to nerve-center once, all agents inherit)

| Secret | Where to get | What it unlocks |
|--------|-------------|-----------------|
| `GMAIL_APP_PASSWORD` | myaccount.google.com/security → App Passwords | **EVERYTHING** — email, briefings, outreach |
| `OPENROUTER_KEY` | openrouter.ai | ✅ Already set |
| `SERPAPI_KEY` | serpapi.com | ✅ Already set |
| `DEVTO_API_KEY` | dev.to/settings/extensions | Auto-publishes article |
| `STRIKE_API_KEY` | dashboard.strike.me → API | Lightning zero-fee payments |

---

## The Loop (how it compounds)

```
New knowledge found
  → Uploaded to mycelium-knowledge (public, free)
  → Packaged as sellable guide on Lemon Squeezy ($10)
  → New agent spawned to pursue that path
  → Agent finds grants / revenue / audience
  → Money flows to gallery + PCRF + system
  → System gets smarter
  → Finds more knowledge
  → Loop
```

---

## How to Spawn a New Agent

When any agent discovers a new category worth pursuing:

1. Create repo: `mycelium-[category]`
2. Add README explaining the category
3. Add `agent/[category]_agent.py` with autonomous logic
4. Add `.github/workflows/daily-[category].yml`
5. Connect back to nerve-center by updating this map
6. Add a knowledge doc to mycelium-knowledge

Categories we'll spawn next (in order of value):
- `mycelium-legal` — TCPA/FCRA claim tracker, files FTC complaints automatically
- `mycelium-market` — Kalshi prediction market monitor (US-legal)
- `mycelium-affiliate` — manages ethical affiliate programs
- `mycelium-art` — generates new artworks, adds to gallery automatically
- `mycelium-translation` — translates KNOW_YOUR_RIGHTS into other languages

---

## For Anyone Who Finds This

This is all open source. Fork any repo. Adapt it to your cause.
The organism doesn't care what it grows for — point it at something good.

Gallery: https://meekotharaccoon-cell.github.io/gaza-rose-gallery
