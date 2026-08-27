import { Target, Footprints, Wrench, Clock3, Flag, Check } from "lucide-react";
import { LearnerProfile } from "@/lib/types";

type Stop = {
  key: string;
  label: string;
  icon: React.ReactNode;
  captured: boolean;
  value?: React.ReactNode;
};

export default function JourneyRail({
  profile,
  onGeneratePath,
}: {
  profile: LearnerProfile;
  onGeneratePath: () => void;
}) {
  const started = profile.goals.raw_text !== "";

  const stops: Stop[] = [
    {
      key: "goal",
      label: "Goal",
      icon: <Target size={15} />,
      captured: !!profile.goals.target_role,
      value: profile.goals.target_role ?? undefined,
    },
    {
      key: "start",
      label: "Starting point",
      icon: <Footprints size={15} />,
      captured: started,
      value: started ? (
        <span className="capitalize">{profile.experience_level}</span>
      ) : undefined,
    },
    {
      key: "skills",
      label: "Skills you have",
      icon: <Wrench size={15} />,
      captured: profile.current_skills.length > 0,
      value:
        profile.current_skills.length > 0 ? (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {profile.current_skills.map((s) => (
              <span
                key={s.skill}
                className="animate-pop inline-flex items-center gap-1 rounded-full bg-brand-soft px-2 py-0.5 text-xs font-medium text-brand"
              >
                {s.skill}
                <span className="text-brand/50">{s.proficiency}/5</span>
              </span>
            ))}
          </div>
        ) : undefined,
    },
    {
      key: "time",
      label: "Time you've got",
      icon: <Clock3 size={15} />,
      captured: !!profile.preferences.time_commitment,
      value: profile.preferences.time_commitment ?? undefined,
    },
  ];

  const capturedCount = stops.filter((s) => s.captured).length;
  const unlocked =
    !!profile.goals.target_role && started && profile.current_skills.length > 0;

  return (
    <aside className="rounded-2xl border border-line bg-surface/70 p-5 backdrop-blur-sm">
      <div className="mb-1 flex items-baseline justify-between">
        <h2 className="font-display text-lg font-semibold text-ink">Your journey</h2>
        <span className="text-xs font-medium text-muted">{capturedCount} of 4</span>
      </div>
      <p className="mb-5 text-xs leading-relaxed text-muted">
        Each thing you tell me lights up a stop on your path.
      </p>

      <div>
        {stops.map((stop, i) => (
          <RailNode key={stop.key} stop={stop} isLast={false} lit={stop.captured} index={i} />
        ))}

        {/* final milestone */}
        <div className="flex gap-3">
          <div className="flex flex-col items-center">
            <div
              className={`grid h-8 w-8 place-items-center rounded-full border-2 transition-colors ${
                unlocked
                  ? "animate-halo border-gold bg-gold text-white"
                  : "border-dashed border-line bg-surface text-muted/40"
              }`}
            >
              <Flag size={15} />
            </div>
          </div>
          <div className="pt-1">
            <p
              className={`font-display text-sm font-semibold ${
                unlocked ? "text-ink" : "text-muted/50"
              }`}
            >
              Ready for your path
            </p>
            {unlocked ? (
              <button
                onClick={onGeneratePath}
                className="mt-2 inline-flex items-center gap-1.5 rounded-lg bg-gold px-3 py-1.5 text-xs font-semibold text-white transition hover:brightness-105"
              >
                Generate my path
              </button>
            ) : (
              <p className="mt-0.5 text-xs text-muted/60">
                Share a goal, your level and a skill to unlock.
              </p>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
}

function RailNode({
  stop,
  lit,
  index,
}: {
  stop: Stop;
  isLast: boolean;
  lit: boolean;
  index: number;
}) {
  return (
    <div className="flex gap-3">
      {/* marker + connector */}
      <div className="flex flex-col items-center">
        <div
          className={`grid h-8 w-8 place-items-center rounded-full border-2 transition-all duration-300 ${
            lit
              ? "animate-pop border-brand bg-brand text-white"
              : "border-line bg-surface text-muted/40"
          }`}
          style={lit ? { animationDelay: `${index * 40}ms` } : undefined}
        >
          {lit ? <Check size={15} strokeWidth={3} /> : stop.icon}
        </div>
        {/* the path segment below this node fills when this node is lit */}
        <div className="relative my-1 w-0.5 flex-1 overflow-hidden rounded bg-line">
          {lit && (
            <div className="absolute inset-0 origin-top animate-grow rounded bg-brand" />
          )}
        </div>
      </div>

      {/* content */}
      <div className="min-h-[3.25rem] pb-2 pt-1">
        <p
          className={`text-xs font-semibold uppercase tracking-wide ${
            lit ? "text-brand" : "text-muted/60"
          }`}
        >
          {stop.label}
        </p>
        {stop.value ? (
          typeof stop.value === "string" ? (
            <p className="animate-fade-up font-display text-base font-semibold text-ink">
              {stop.value}
            </p>
          ) : (
            stop.value
          )
        ) : (
          <p className="text-sm text-muted/40">Not yet</p>
        )}
      </div>
    </div>
  );
}
