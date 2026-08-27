"use client";

import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from "react";
import { ArrowUp, AlertCircle, Sparkles } from "lucide-react";
import { ChatMessage, LearnerProfile } from "@/lib/types";
import { demoExtract, demoReply, demoPathReply, isPathRequest } from "@/lib/demoExtractor";
import { sendChat } from "@/lib/api";

const STARTERS = [
  "I want to become a data analyst. I know a little Python and Excel.",
  "New to coding — I'd like to learn web development, about 5 hours a week.",
  "I know some Python and want to move into machine learning.",
];

const INTRO: ChatMessage = {
  id: "intro",
  role: "assistant",
  text: "Hi — I'm Pathfinder. Tell me what you'd like to learn and where you're starting from, and I'll map out your path as we talk.",
};

export type ChatHandle = { reset: () => void; send: (text: string) => void };

interface Props {
  userId: string;
  mode: "demo" | "live";
  profile: LearnerProfile;
  onProfileChange: (p: LearnerProfile) => void;
}

const ChatInterface = forwardRef<ChatHandle, Props>(function ChatInterface(
  { userId, mode, profile, onProfileChange },
  ref,
) {
  const [messages, setMessages] = useState<ChatMessage[]>([INTRO]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useImperativeHandle(ref, () => ({
    reset: () => {
      setMessages([INTRO]);
      setError(null);
      setInput("");
    },
    send: (text: string) => submit(text),
  }));

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, busy]);

  async function submit(text: string) {
    const trimmed = text.trim();
    if (!trimmed || busy) return;

    setError(null);
    setInput("");
    setMessages((m) => [...m, { id: crypto.randomUUID(), role: "user", text: trimmed }]);
    setBusy(true);

    try {
      if (mode === "live") {
        const result = await sendChat(userId, trimmed);
        onProfileChange(result.profile);
        setMessages((m) => [
          ...m,
          { id: crypto.randomUUID(), role: "assistant", text: result.reply },
        ]);
      } else {
        await new Promise((r) => setTimeout(r, 360));
        const updated = demoExtract(trimmed, profile);
        onProfileChange(updated);
        const reply = isPathRequest(trimmed) ? demoPathReply(updated) : demoReply(updated);
        setMessages((m) => [
          ...m,
          { id: crypto.randomUUID(), role: "assistant", text: reply },
        ]);
      }
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Something went wrong.";
      setError(
        `Couldn't reach the backend in Live mode (${msg}). Is it running on port 8000? Switch to Demo to keep going.`,
      );
    } finally {
      setBusy(false);
    }
  }

  const showStarters = messages.length <= 1;

  return (
    <div className="flex h-full flex-col">
      <div ref={scrollRef} className="scroll-quiet flex-1 space-y-5 overflow-y-auto px-1 py-2">
        {messages.map((m) =>
          m.role === "assistant" ? (
            <div key={m.id} className="animate-fade-up flex gap-2.5">
              <div className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-full bg-brand-soft">
                <Sparkles size={14} className="text-brand" />
              </div>
              <div className="max-w-[85%] rounded-2xl rounded-tl-sm bg-surface px-4 py-2.5 text-sm leading-relaxed text-ink shadow-sm ring-1 ring-line">
                {m.text}
              </div>
            </div>
          ) : (
            <div key={m.id} className="animate-fade-up flex justify-end">
              <div className="max-w-[85%] rounded-2xl rounded-br-sm bg-brand px-4 py-2.5 text-sm leading-relaxed text-white">
                {m.text}
              </div>
            </div>
          ),
        )}

        {busy && (
          <div className="flex gap-2.5">
            <div className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-full bg-brand-soft">
              <Sparkles size={14} className="text-brand" />
            </div>
            <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm bg-surface px-4 py-3.5 shadow-sm ring-1 ring-line">
              <Dot /> <Dot delay="0.15s" /> <Dot delay="0.3s" />
            </div>
          </div>
        )}

        {showStarters && (
          <div className="animate-fade-up space-y-2 pl-9 pt-1">
            <p className="text-xs font-medium text-muted">Try one of these</p>
            {STARTERS.map((s) => (
              <button
                key={s}
                onClick={() => submit(s)}
                className="block w-full rounded-xl border border-line bg-surface/60 px-4 py-2.5 text-left text-sm text-muted transition hover:border-brand hover:bg-surface hover:text-ink"
              >
                {s}
              </button>
            ))}
          </div>
        )}
      </div>

      {error && (
        <div className="mx-1 mb-2 flex items-start gap-2 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700 ring-1 ring-red-100">
          <AlertCircle size={14} className="mt-0.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="flex items-end gap-2 rounded-2xl border border-line bg-surface p-2 shadow-sm transition focus-within:border-brand focus-within:ring-4 focus-within:ring-brand-soft">
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
          placeholder="Describe your goal…"
          className="max-h-32 flex-1 resize-none bg-transparent px-2 py-1.5 text-sm text-ink outline-none placeholder:text-muted/50"
        />
        <button
          onClick={() => submit(input)}
          disabled={busy || !input.trim()}
          aria-label="Send message"
          className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-brand text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-30"
        >
          <ArrowUp size={18} strokeWidth={2.5} />
        </button>
      </div>
      <p className="mt-1.5 px-1 text-center text-[11px] text-muted/50">
        Enter to send · Shift + Enter for a new line
      </p>
    </div>
  );
});

export default ChatInterface;

function Dot({ delay = "0s" }: { delay?: string }) {
  return (
    <span
      className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-muted/40"
      style={{ animationDelay: delay }}
    />
  );
}
