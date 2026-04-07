import { create } from "zustand";
import { Platform, OceanScores, PlatformScores, ConsentData } from "../types";
import { STORAGE_KEYS } from "../types";
import { loadFromStorage, saveToStorage, saveAuthToken, loadAuthToken } from "../utils/storage";
import getApiClient from "../utils/api";

interface AppState {
  // Auth
  userId: string | null;
  authToken: string | null;
  connectedPlatforms: Platform[];

  // Consent
  consent: ConsentData | null;

  // Scores
  oceanScores: OceanScores | null;
  platformScores: PlatformScores;
  lastUpdated: string | null;

  // UI state
  isLoading: boolean;
  error: string | null;
  currentView: "platform-select" | "consent" | "connecting" | "dashboard" | "settings";

  // Actions
  initialize: () => Promise<void>;
  setConsent: (consent: ConsentData) => void;
  startAuth: (platforms: Platform[], historical: boolean, futureSync: boolean) => Promise<{ auth_urls: Record<Platform, string>; session_id: string }>;
  setAuthToken: (token: string, userId: string) => Promise<void>;
  addConnectedPlatform: (platform: Platform) => Promise<void>;
  fetchProfile: () => Promise<void>;
  triggerSync: (platform: Platform, historical?: boolean) => Promise<void>;
  disconnectPlatform: (platform: Platform) => Promise<void>;
  deleteAccount: () => Promise<void>;
  revokeConsent: () => Promise<void>;
  setView: (view: AppState["currentView"]) => void;
  setError: (error: string | null) => void;
  logout: () => Promise<void>;
}

export const useAppStore = create<AppState>((set, get) => ({
  userId: null,
  authToken: null,
  connectedPlatforms: [],
  consent: null,
  oceanScores: null,
  platformScores: {},
  lastUpdated: null,
  isLoading: false,
  error: null,
  currentView: "platform-select",

  initialize: async () => {
    set({ isLoading: true });
    try {
      const [token, userId, platforms, consent] = await Promise.all([
        loadAuthToken(),
        loadFromStorage<string>(STORAGE_KEYS.USER_ID),
        loadFromStorage<Platform[]>(STORAGE_KEYS.CONNECTED_PLATFORMS),
        loadFromStorage<ConsentData>(STORAGE_KEYS.CONSENT),
      ]);

      if (token && userId) {
        set({
          authToken: token,
          userId,
          connectedPlatforms: platforms || [],
          consent,
          currentView: "dashboard",
        });
      }
    } catch (err) {
      set({ error: "Failed to initialize" });
    } finally {
      set({ isLoading: false });
    }
  },

  setConsent: (consent) => {
    set({ consent });
    saveToStorage(STORAGE_KEYS.CONSENT, consent);
  },

  startAuth: async (platforms, historical, futureSync) => {
    set({ isLoading: true, error: null });
    try {
      const client = getApiClient();
      const response = await client.post("/auth/start", {
        platforms,
        historical_fetch: historical,
        future_sync: futureSync,
      });
      set({ userId: response.data.session_id });
      await saveToStorage(STORAGE_KEYS.USER_ID, response.data.session_id);
      return response.data;
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Failed to start authentication";
      set({ error: msg });
      throw err;
    } finally {
      set({ isLoading: false });
    }
  },

  setAuthToken: async (token, userId) => {
    await saveAuthToken(token);
    await saveToStorage(STORAGE_KEYS.USER_ID, userId);
    set({ authToken: token, userId });
  },

  addConnectedPlatform: async (platform) => {
    const current = get().connectedPlatforms;
    if (!current.includes(platform)) {
      const updated = [...current, platform];
      set({ connectedPlatforms: updated });
      await saveToStorage(STORAGE_KEYS.CONNECTED_PLATFORMS, updated);
    }
  },

  fetchProfile: async () => {
    set({ isLoading: true, error: null });
    try {
      const client = getApiClient();
      const response = await client.get("/user/profile");
      set({
        oceanScores: response.data.ocean,
        platformScores: response.data.platforms || {},
        lastUpdated: response.data.last_updated,
      });
    } catch (err: any) {
      set({ error: err.response?.data?.detail || "Failed to fetch profile" });
    } finally {
      set({ isLoading: false });
    }
  },

  triggerSync: async (platform, historical = false) => {
    set({ isLoading: true, error: null });
    try {
      const client = getApiClient();
      await client.post(`/sync/${platform}`, { historical });
    } catch (err: any) {
      set({ error: err.response?.data?.detail || `Failed to sync ${platform}` });
    } finally {
      set({ isLoading: false });
    }
  },

  disconnectPlatform: async (platform) => {
    set({ isLoading: true, error: null });
    try {
      const client = getApiClient();
      await client.post(`/user/disconnect/${platform}`);
      const updated = get().connectedPlatforms.filter((p) => p !== platform);
      set({ connectedPlatforms: updated });
      await saveToStorage(STORAGE_KEYS.CONNECTED_PLATFORMS, updated);
    } catch (err: any) {
      set({ error: err.response?.data?.detail || `Failed to disconnect ${platform}` });
    } finally {
      set({ isLoading: false });
    }
  },

  deleteAccount: async () => {
    set({ isLoading: true, error: null });
    try {
      const client = getApiClient();
      await client.post("/user/delete");
      await get().logout();
    } catch (err: any) {
      set({ error: err.response?.data?.detail || "Failed to delete account" });
    } finally {
      set({ isLoading: false });
    }
  },

  revokeConsent: async () => {
    set({ isLoading: true, error: null });
    try {
      const client = getApiClient();
      await client.post("/user/revoke-consent");
      await get().logout();
    } catch (err: any) {
      set({ error: err.response?.data?.detail || "Failed to revoke consent" });
    } finally {
      set({ isLoading: false });
    }
  },

  setView: (view) => set({ currentView: view }),
  setError: (error) => set({ error }),

  logout: async () => {
    const { clearAllStorage } = await import("../utils/storage");
    await clearAllStorage();
    set({
      userId: null,
      authToken: null,
      connectedPlatforms: [],
      consent: null,
      oceanScores: null,
      platformScores: {},
      lastUpdated: null,
      currentView: "platform-select",
    });
  },
}));
