"use client";

import { useEffect, useRef, useState } from "react";
import { RotateCcw, Compass } from "lucide-react";
import ChatInterface, { type ChatHandle } from "@/components/ChatInterface";
import JourneyRail from "@/components/JourneyRail";
import QuizInterface from "@/components/QuizInterface";
import { emptyProfile, LearnerProfile } from "@/lib/types";
import { getRoadmap } from "@/lib/api";

// No accounts, no IDs to manage — a fixed local id keeps the backend contract happy.
const LOCAL_ID = "local-learner";

export default function Home() {
  const [mode, setMode] = useState<"demo" | "live">("demo");
  const [profile, setProfile] = useState<LearnerProfile>(emptyProfile(LOCAL_ID));
  const [isTakingQuiz, setIsTakingQuiz] = useState(false);
  const [roadmapData, setRoadmapData] = useState<any[] | null>(null);
  const chatRef = useRef<ChatHandle>(null);

  // Fetch the gap analysis data
  useEffect(() => {
    getRoadmap(LOCAL_ID)
      .then((data) => {
        if (data && data.roadmap) {
          setRoadmapData(data.roadmap);
        }
      })
      .catch((err) => {
        console.error("No roadmap available yet or error fetching:", err);
      });
  }, [isTakingQuiz]); // Re-fetch if quiz state changes (e.g., after completing the quiz)

  function reset() {
    setProfile(emptyProfile(LOCAL_ID));
    setIsTakingQuiz(false);
    setRoadmapData(null);
    chatRef.current?.reset();
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col px-4 py-6 sm:px-6">
      {/* header */}
      <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-ink text-canvas">
            <Compass size={20} />
          </div>
          <div>
            <h1 className="font-display text-xl font-bold tracking-tight text-ink">
              Pathfinder
            </h1>
            <p className="text-sm text-muted">Talk through your goals — watch your path appear.</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center rounded-lg border border-line bg-surface p-0.5 text-sm">
            {(["demo", "live"] as const).map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={`rounded-md px-3 py-1.5 font-medium capitalize transition ${
                  mode === m ? "bg-brand text-white" : "text-muted hover:text-ink"
                }`}
              >
                {m}
              </button>
            ))}
          </div>
          <button
            onClick={reset}
            aria-label="Start over"
            title="Start over"
            className="grid h-9 w-9 place-items-center rounded-lg border border-line bg-surface text-muted transition hover:text-ink"
          >
            <RotateCcw size={16} />
          </button>
        </div>
      </header>

      {/* body */}
      {isTakingQuiz ? (
        // VIEW 1: THE QUIZ
        <section className="flex-1 w-full py-8">
          {/* Error fixed here! Added onComplete prop */}
          <QuizInterface 
            userId={LOCAL_ID} 
            onComplete={() => setIsTakingQuiz(false)} 
          />
        </section>
      ) : roadmapData && roadmapData.length > 0 ? (
        // VIEW 2: THE FINAL ROADMAP (Takes over the whole screen)
        <section className="flex-1 w-full py-8 max-w-3xl mx-auto">
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-display font-bold text-ink mb-2">Your Personalized Learning Path</h2>
            <p className="text-muted">Here is your step-by-step roadmap to master your goals.</p>
          </div>
          <JourneyRail roadmapData={roadmapData} />
        </section>
      ) : (
        // VIEW 3: THE CHAT & SETUP (Default View)
        <div className="grid flex-1 gap-6 lg:grid-cols-[1fr_20rem]">
          <section className="flex min-h-[34rem] flex-col rounded-2xl border border-line bg-canvas/40 p-4 lg:min-h-0">
            <ChatInterface
              ref={chatRef}
              userId={LOCAL_ID}
              mode={mode}
              profile={profile}
              onProfileChange={setProfile}
            />
          </section>

          <section>
            <JourneyRail
              profile={profile}
              onGeneratePath={() => setIsTakingQuiz(true)} 
            />
          </section>
        </div>
      )}

      <footer className="mt-12 text-center text-xs text-muted/60">
        {mode === "demo"
          ? "Demo mode — your path is built right in the browser, no backend needed."
          : "Live mode — talking to your FastAPI backend at /api/chat."}
      </footer>
    </main>
  );
}