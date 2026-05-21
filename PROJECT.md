# Agent Business — Project Overview

## Goal

Build a Windows desktop app that autonomously runs a print-on-demand shirt business on Etsy.
A team of specialised AI agents handles every part of the operation — research, design, listing,
marketing, analytics, and fulfilment — while a Board of Directors and Overseer agent coordinate
strategy. The owner watches the whole operation live through a control-room dashboard.

**First business vertical:** T-shirts via Printify → Etsy

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| Desktop app | Electron + React |
| Agent runtime | Python + FastAPI |
| Agent AI | Claude API (Haiku / Sonnet / Opus tiered) |
| Image generation | DALL-E 3 (OpenAI) |
| Print-on-demand | Printify |
| Marketplace | Etsy API |
| Real-time UI updates | WebSockets |
| Local data | SQLite |

---

## Agent Hierarchy

```
Board of Directors  (Claude Opus)   — sets weekly strategy & directives
    └── Overseer    (Claude Sonnet) — breaks directives into tasks, dispatches workers
            ├── Research    (Haiku) — finds trending niches & keywords
            ├── Design      (Haiku) — generates shirt designs via DALL-E 3
            ├── Listing     (Haiku) — writes SEO-optimised Etsy titles/descriptions/tags
            ├── Marketing   (Haiku) — social media captions, promotion copy
            ├── Analytics   (Haiku) — tracks sales, flags underperformers
            └── Operations  (Haiku) — Printify fulfillment, Etsy order management
```

---

## Phases & Status

### ✅ Phase 0 — Account Setup  *(manual — user)*
- [ ] Create Etsy seller account → enable API → save Client ID + Secret
- [ ] Create Printify account → connect Etsy shop → save API key
- [ ] Create Anthropic API key
- [ ] Create OpenAI API key
- [ ] Copy `.env.example` → `.env` and fill in all keys

### ✅ Phase 1 — Project Skeleton  *(complete)*
- [x] Electron + React desktop app shell
- [x] Vite build pipeline
- [x] Dashboard layout: agent panels, tabs (Agents / Products / Revenue), event log
- [x] All 8 agent panels with live status display
- [x] Board of Directors panel + Overseer panel
- [x] Products board (grid view with mockup thumbnails)
- [x] Revenue board (KPI cards + daily revenue line chart)
- [x] Event log sidebar (real-time scrolling feed)
- [x] Python FastAPI backend with WebSocket hub
- [x] SQLite schema (tasks, events, products, orders)
- [x] BaseAgent class with Claude API integration
- [x] All 8 agent classes wired up
- [x] AgentManager with full business cycle orchestration
- [x] Etsy, Printify, DALL-E 3 API client stubs
- [x] `useAgentSocket` React hook (auto-reconnect WebSocket)
- [x] Full cycle tested end-to-end — agents run, event log populates live

### 🔲 Phase 2 — Live Agent Reasoning  *(next)*
- [ ] Add `.env` keys so agents use real Claude reasoning
- [ ] Test Board → Overseer → Worker pipeline with actual API calls
- [ ] Validate Research agent finds real niches
- [ ] Validate Listing agent writes real SEO copy
- [ ] Validate Marketing agent produces real social copy

### 🔲 Phase 3 — External API Clients
- [ ] Etsy OAuth 2.0 flow (browser popup → token exchange)
- [ ] Etsy: list product, get orders, get listing stats
- [ ] Printify: upload design, create product, generate mockups, publish to Etsy
- [ ] DALL-E 3: generate shirt design from prompt
- [ ] Error handling + retry logic on all clients
- [ ] Manual test each client in isolation before wiring into agents

### 🔲 Phase 4 — Full Product Creation Pipeline
- [ ] Research → niche + keywords
- [ ] Design → DALL-E 3 image
- [ ] Operations → upload to Printify, create product + mockups
- [ ] Listing → write title, description, tags, price
- [ ] Operations → publish to Etsy via Printify
- [ ] Save product to SQLite, push to Products board in UI
- [ ] End-to-end test: one real shirt listed on Etsy

### 🔲 Phase 5 — Dashboard Polish
- [ ] Mockup images shown in Products board from Printify URLs
- [ ] Overseer queue shows live task countdown
- [ ] Agent panels show timestamps of last action
- [ ] Revenue board pulls real Etsy sales data
- [ ] Notification when a product sells

### 🔲 Phase 6 — Marketing Agent
- [ ] Social captions generated for each new product
- [ ] Copy shown in dashboard for manual review before posting
- [ ] Optional: auto-post to social APIs (Twitter/X, Instagram)

### 🔲 Phase 7 — Analytics & Iteration Loop
- [ ] Analytics agent polls Etsy daily (views, favourites, sales per listing)
- [ ] Low-performer flagging → Overseer → Board strategy update
- [ ] Revenue dashboard shows rolling daily/weekly/monthly metrics
- [ ] Board adjusts niche/price strategy based on analytics

---

## Current State

**The app runs.** Phase 1 is complete and tested:

- `npm run dev` launches the full stack (Electron window + Python backend)
- Dashboard renders with all 8 agent panels
- WebSocket connects automatically, reconnects on drop
- Clicking START runs a complete agent business cycle end-to-end
- Agents fall back to sensible defaults when no API keys are present
- Design and Printify steps are skipped gracefully until keys are added

**Immediate next step:** Add API keys to `.env` (copy from `.env.example`).
Once the Anthropic key is present, agents will use real Claude reasoning on the next cycle.

---

## Key Files

```
electron/main.js              — Electron entry; spawns Python backend using venv
src/App.jsx                   — Root layout, tab navigation, START/STOP controls
src/hooks/useAgentSocket.js   — WebSocket hook feeding all UI state
src/components/AgentPanel.jsx — Per-agent status card
src/components/EventLog.jsx   — Live event feed sidebar
backend/main.py               — FastAPI app + WebSocket hub
backend/agents/manager.py     — Orchestrates the full business cycle
backend/agents/base.py        — BaseAgent (Claude API, status emitter)
backend/agents/board.py       — Board of Directors (Opus)
backend/agents/overseer.py    — Overseer (Sonnet)
backend/clients/printify.py   — Printify REST client
backend/clients/etsy.py       — Etsy REST client
backend/clients/imagegen.py   — DALL-E 3 client
backend/db.py                 — SQLite helpers
.env.example                  — API key template (copy to .env)
```
