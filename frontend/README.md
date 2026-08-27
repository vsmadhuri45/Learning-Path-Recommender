# Pathfinder — Learning Path Assistant (frontend)

A Next.js chat interface for the conversational learning assistant. The learner
describes their goals in plain language; a **journey rail** lights up beside the
chat as each fact is captured — goal, starting point, skills, time — ending in a
milestone that unlocks when there's enough to build a path.

No accounts, no keys, no setup. It runs immediately.

## Run it (in VS Code terminal)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000**.

## Demo mode vs Live mode

Toggle in the top-right.

- **Demo** (default): the profile is built right in the browser
  (`lib/demoExtractor.ts`) with simple keyword matching. No backend needed —
  perfect for showing the UI on its own.
- **Live**: sends each message to the FastAPI backend's `POST /api/chat`, which
  does the real LLM extraction. Start the backend first (see `backend/README.md`).

To point Live mode at a different backend, copy `.env.local.example` to
`.env.local` and set `NEXT_PUBLIC_API_URL`.

## Structure

| Path | What it is |
|---|---|
| `app/page.tsx` | App shell: header, mode toggle, reset, layout. |
| `components/ChatInterface.tsx` | The chat: messages, composer, demo/live logic. |
| `components/JourneyRail.tsx` | The signature — the path that lights up as you talk. |
| `lib/types.ts` | `LearnerProfile` type — mirrors `docs/CONTRACT.md`. |
| `lib/api.ts` | Calls the backend in Live mode. |
| `lib/demoExtractor.ts` | Browser-only extractor for Demo mode. |

## Design notes

- Palette, fonts, and motion live in `tailwind.config.ts`; fonts (Space Grotesk +
  Inter) load via a `<link>` in `app/layout.tsx`, so the build never needs them.
- Motion respects `prefers-reduced-motion`.
- When the backend adds profile fields, update `lib/types.ts` and the rail to match.
