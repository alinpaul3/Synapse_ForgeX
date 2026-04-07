import axios, { AxiosInstance } from "axios";
import { loadAuthToken } from "./storage";

const API_BASE_URL = "http://localhost:8000/api";

let _client: AxiosInstance | null = null;

export function getApiClient(): AxiosInstance {
  if (!_client) {
    _client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: { "Content-Type": "application/json" },
    });

    // Attach auth token to every request
    _client.interceptors.request.use(async (config) => {
      const token = await loadAuthToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle 401 responses
    _client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired - clear storage and redirect to popup
          const { clearAllStorage } = await import("./storage");
          await clearAllStorage();
          if (typeof chrome !== "undefined" && chrome.runtime) {
            chrome.runtime.sendMessage({ type: "AUTH_EXPIRED" });
          }
        }
        return Promise.reject(error);
      }
    );
  }
  return _client;
}

export default getApiClient;
