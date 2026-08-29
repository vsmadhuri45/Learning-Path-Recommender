"use client";

import { forwardRef, useImperativeHandle, useRef, useState } from "react";
import { Sparkles, Send } from "lucide-react";
import { askAssistant } from "@/lib/api";

interface QA {
  id: string;
  question: string;
  answer: string;
}

export type AssistantHandle = { ask: (question: string) => void };

interface Props {
  userId: string;
}

const AssistantPanel = forwardRef<AssistantHandle, Props>(function AssistantPanel(
  { userId },
  ref,
) {
  const [history, setHistory] = useState<QA[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useImperativeHandle(ref, () => ({
    ask: (question: string) => submit(question),
  }));

  async function submit(question: string) {
    const trimmed = question.trim();
    if (!trimmed || busy) return;

    setError(null);
    setInput("");
    setBusy(true);

    try {
      const answer = await askAssistant(userId, trimmed);
      setHistory((h) => [...h, { id: crypto.randomUUID(), question: trimmed, answer }]);
      requestAnimationFrame(() => {
        scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
      });
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Something went wrong.";
      setError(`Couldn't reach the assistant (${msg}).`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="rounded-2xl border border-line bg-surface/70 p-5 backdrop-blur-sm">
      <div className="mb-3 flex items-center gap-2">
        <div className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-brand-soft">
          <Sparkles size={14} className="text-brand" />
        </div>
        <h2 className="font-display text-lg font-semibold text-ink">Ask about your path</h2>
      </div>

      {history.length > 0 && (
        <div
          ref={scrollRef}
          className="scroll-quiet mb-3 max-h-64 space-y-3 overflow-y-auto pr-1"
        >
          {history.map((qa) => (
            <div key={qa.id} className="space-y-1.5">
              <p className="text-xs font-semibold text-muted">{qa.question}</p>
              <p className="rounded-xl bg-brand-soft/40 px-3 py-2 text-sm leading-relaxed text-ink">
                {qa.answer}
              </p>
            </div>
          ))}
        </div>
      )}

      {busy && (
        <p className="mb-2 text-xs text-muted">Thinking…</p>
      )}

      {error && (
        <p className="mb-2 text-xs text-red-600">{error}</p>
      )}

      <div className="flex items-end gap-2 rounded-xl border border-line bg-surface p-1.5 transition focus-within:border-brand focus-within:ring-4 focus-within:ring-brand-soft">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              submit(input);
            }
          }}
          rows={1}
          placeholder="Ask why something's on your path…"
          className="max-h-24 flex-1 resize-none bg-transparent px-2 py-1.5 text-sm text-ink outline-none placeholder:text-muted/50"
        />
        <button
          onClick={() => submit(input)}
          disabled={busy || !input.trim()}
          aria-label="Ask"
          className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-brand text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-30"
        >
          <Send size={15} />
        </button>
      </div>
    </div>
  );
});

export default AssistantPanel;