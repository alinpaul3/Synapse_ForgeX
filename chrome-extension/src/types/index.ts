// Shared types for Chrome Extension + API communication

export type Platform = "youtube" | "reddit";

export interface OceanScores {
  openness: number;
  conscientiousness: number;
  extraversion: number;
  agreeableness: number;
  neuroticism: number;
  confidence?: number;
  trend?: "increasing" | "decreasing" | "stable";
}

export interface PlatformScores {
  youtube?: OceanScores | null;
  reddit?: OceanScores | null;
}

export interface UserProfile {
  user_id: string;
  ocean: OceanScores | null;
  platforms: PlatformScores;
  last_updated: string | null;
}

export interface AuthStartRequest {
  platforms: Platform[];
  historical_fetch: boolean;
  future_sync: boolean;
}

export interface AuthStartResponse {
  auth_urls: Record<Platform, string>;
  session_id: string;
}

export interface AuthCallbackResponse {
  status: string;
  user_id: string;
  token: string;
  platform: Platform;
}

export interface SyncRequest {
  historical: boolean;
}

export interface SyncResponse {
  status: string;
  job_id: string;
  platform: Platform;
}

export interface SyncStatus {
  status: "pending" | "syncing" | "completed" | "failed";
  platform: Platform;
  data_count: number;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
}

export interface ConsentData {
  platforms: Platform[];
  historical_allowed: boolean;
  sync_allowed: boolean;
}

// Chrome storage keys
export const STORAGE_KEYS = {
  USER_ID: "synapse_user_id",
  AUTH_TOKEN: "synapse_auth_token",
  CONNECTED_PLATFORMS: "synapse_connected_platforms",
  CONSENT: "synapse_consent",
  LAST_SYNC: "synapse_last_sync",
} as const;
