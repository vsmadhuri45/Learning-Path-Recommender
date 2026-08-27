// Mirrors docs/CONTRACT.md section 2. Keep in sync with the backend.

export type ExperienceLevel = "beginner" | "intermediate" | "advanced";

export interface Skill {
  skill: string;
  proficiency: number; // 1-5
}

export interface CompletedCourse {
  course_id: string;
  title: string;
  provider?: string;
  completed_at?: string;
}

export interface LearnerProfile {
  user_id: string;
  created_at?: string | null;
  updated_at?: string | null;
  interests: string[];
  experience_level: ExperienceLevel;
  goals: {
    raw_text: string;
    parsed: string[];
    target_role: string | null;
  };
  completed_courses: CompletedCourse[];
  current_skills: Skill[];
  preferences: {
    time_commitment?: string | null;
    preferred_formats?: string[];
  };
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
}

export function emptyProfile(userId: string): LearnerProfile {
  return {
    user_id: userId,
    interests: [],
    experience_level: "beginner",
    goals: { raw_text: "", parsed: [], target_role: null },
    completed_courses: [],
    current_skills: [],
    preferences: { time_commitment: null, preferred_formats: [] },
  };
}
