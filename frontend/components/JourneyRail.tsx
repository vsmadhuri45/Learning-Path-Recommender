import React from 'react';
import { Target, Footprints, Wrench, Clock3, Flag, Check } from "lucide-react";
import { LearnerProfile } from "@/lib/types";

// Expected prop interface from the Python backend
export interface GapNode {
  concept_id: string;
  title: string;
  current_mastery: number;
  target_mastery: number;
  status: 'Ready to Study' | 'Locked' | 'Needs Mastery';
}

type Stop = {
  key: string;
  label: string;
  icon: React.ReactNode;
  captured: boolean;
  value?: React.ReactNode;
};

// We make all props optional so the component can handle either the Setup Phase OR the Roadmap Phase
interface JourneyRailProps {
  profile?: LearnerProfile;
  onGeneratePath?: () => void;
  roadmapData?: GapNode[] | null;
}

export default function JourneyRail({
  profile,
  onGeneratePath,
  roadmapData
}: JourneyRailProps) {

  // ==========================================
  // PHASE 2: ROADMAP MODE (If data is present)
  // ==========================================
  if (roadmapData && roadmapData.length > 0) {
    return (
      <div className="relative border-l-2 border-gray-200 ml-4 pl-6 space-y-6">
        {roadmapData.map((node, index) => (
          <div 
            key={node.concept_id} 
            className={`relative transition-all duration-200 ${
              node.status === 'Locked' ? 'opacity-50 grayscale cursor-not-allowed' : 'opacity-100'
            }`}
          >
            {/* Timeline Node Marker */}
            <div className={`absolute -left-[35px] top-4 w-6 h-6 rounded-full border-4 flex items-center justify-center 
              ${node.status === 'Ready to Study' 
                ? 'bg-blue-600 border-blue-200 animate-pulse' 
                : 'bg-gray-300 border-white'}`} 
            />
            
            {/* To-Do List Card */}
            <div className="bg-white p-5 rounded-lg shadow-sm border border-gray-100 hover:shadow-md">
              <div className="flex justify-between items-start">
                <h3 className="font-semibold text-lg text-gray-800">
                  Step {index + 1}: {node.title}
                </h3>
                
                {/* Status Badge */}
                <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wide 
                  ${node.status === 'Ready to Study' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-500'}`}>
                  {node.status.toUpperCase()}
                </span>
              </div>
              
              {/* Mastery Progress Visual */}
              <div className="mt-4 flex items-center gap-4 text-sm">
                <div className="flex-1 bg-gray-200 rounded-full h-2.5">
                  <div 
                    className={`h-2.5 rounded-full ${node.status === 'Ready to Study' ? 'bg-blue-600' : 'bg-gray-400'}`}
                    style={{ width: `${node.current_mastery * 100}%` }}
                  ></div>
                </div>
                <div className="text-gray-600 font-medium whitespace-nowrap">
                  {(node.current_mastery * 100).toFixed(0)}% / {(node.target_mastery * 100).toFixed(0)}% Target
                </div>
              </div>
              
              {/* Call to action */}
              {node.status === 'Ready to Study' && (
                <button className="mt-4 w-full py-2 bg-black text-white rounded-md font-medium hover:bg-gray-800 transition-colors">
                  Start Learning This Concept
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    );
  }

  // ==========================================
  // PHASE 1: SETUP MODE (Waiting for user chat)
  // ==========================================
  if (!profile || !onGeneratePath) {
    return null; // Safety fallback
  }

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
                Take Quiz
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

// Sub-component for rendering the Setup phase timeline
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