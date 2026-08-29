import { LearnerProfile } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface ChatResult {
  reply: string;
  profile: LearnerProfile;
}

/** Calls the real backend /api/chat. Throws on any failure so the UI can react. */
export async function sendChat(userId: string, message: string): Promise<ChatResult> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  });

  if (!res.ok) {
    const detail = await res.json().catch(() => null);
    throw new Error(detail?.detail ?? `Request failed (${res.status})`);
  }
  return res.json();
}

export async function getRoadmap(userId: string) {
  const res = await fetch(`http://localhost:8000/api/roadmap/${userId}`);
  if (!res.ok) {
    throw new Error('Failed to fetch roadmap');
  }
  return res.json();
}